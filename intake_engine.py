#!/usr/bin/env python3
import requests
import json

def fetch_global_knowledge(topic=None, lang="en", region="united_states"):
    data_packet = {
        "topic": topic,
        "trends": [],
        "rising_topics": [],
        "wiki_summary": "",
        "wiki_sections": {},
        "images": [],
        "references": []
    }

    # 1. Daily Google Trends Discovery
    try:
        from pytrends.request import TrendReq
        pt = TrendReq(hl="en-US", tz=360)
        trending_df = pt.trending_searches(pn=region)
        data_packet["trends"] = trending_df[0].head(10).tolist()
        if not topic and data_packet["trends"]:
            topic = data_packet["trends"][0]
            data_packet["topic"] = topic
        if topic:
            pt.build_payload([topic], timeframe="now 7-d")
            rel = pt.related_topics()
            if topic in rel and rel[topic]["rising"] is not None:
                data_packet["rising_topics"] = rel[topic]["rising"]["topic_title"].head(5).tolist()
    except Exception:
        pass

    # 2. Wikipedia-API Encyclopedic Extraction
    target_title = topic
    try:
        import wikipediaapi
        from wikipediaapi._enums import RedirectFilter
        wiki_api = wikipediaapi.Wikipedia(
            user_agent="AutonomousReelsAgent/2.0 (agent@autonomous.local)",
            language=lang,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            max_retries=5,
            retry_wait=2.0
        )

        if not topic:
            random_titles = wiki_api.random(filter_redirect=RedirectFilter.NONREDIRECTS, limit=3)
            topic = random_titles[0] if isinstance(random_titles, list) else str(random_titles)
            data_packet["topic"] = topic

        import wikipedia
        wikipedia.set_lang(lang)
        search_hits, suggestion = wikipedia.search(topic, results=5, suggestion=True)
        target_title = suggestion if suggestion else (search_hits[0] if search_hits else topic)
        data_packet["wiki_summary"] = wikipedia.summary(target_title, sentences=5)
        raw_page = wikipedia.page(target_title)
        data_packet["images"] = [img for img in raw_page.images if img.endswith(('.jpg', '.png'))][:10]
        data_packet["references"] = raw_page.references[:10]

        structured_page = wiki_api.page(target_title)
        if structured_page.exists():
            for sec in structured_page.sections[:5]:
                if sec.text:
                    data_packet["wiki_sections"][sec.title] = sec.text[:600]
    except Exception:
        pass

    # 3. Direct MediaWiki Action API Fallback
    if not data_packet["wiki_summary"] and target_title:
        try:
            resp = requests.get(
                f"https://{lang}.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "format": "json",
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True,
                    "redirects": 1,
                    "titles": target_title
                },
                headers={"User-Agent": "AutonomousReelsAgent/2.0"},
                timeout=10
            ).json()
            pages = resp.get("query", {}).get("pages", {})
            for pid in pages:
                data_packet["wiki_summary"] = pages[pid].get("extract", "")[:1000]
        except Exception:
            pass

    return data_packet

if __name__ == "__main__":
    import sys
    topic_arg = sys.argv[1] if len(sys.argv) > 1 else "Earth rotation"
    print(f"Fetching knowledge for: {topic_arg}...")
    res = fetch_global_knowledge(topic_arg)
    print("Summary:", res["wiki_summary"][:200])
    print("Sections:", list(res["wiki_sections"].keys()))
