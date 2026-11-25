"""long-form outliers: search queries → channels → their latest long videos → views vs the channel median + views/day when dated"""
import subprocess, json, sys, statistics as st, concurrent.futures as cf, re, os
Y=os.path.expanduser("~/.local/bin/yt-dlp")
Q=["what if animated story","what if you could animation","what if everyone science animation","what would happen if animated","stick figure what if","what if 24 hours animated","what if superpower animation story","what if humans could animated explained","what if the world suddenly animation","survive what if animation","what if your brain animation","what if you woke up animation story"]
def flat(url,n):
    r=subprocess.run([Y,"--flat-playlist","--playlist-end",str(n),"-J",url],capture_output=True,text=True,timeout=150)
    try: return json.loads(r.stdout)
    except Exception: return {}
chs={}
def sq(q):
    out=[]
    for e in flat(f"ytsearch22:{q}",22).get("entries",[]) or []:
        if e and (e.get("duration") or 0)>150 and e.get("channel_id"): out.append((e["channel_id"],e.get("channel"),e.get("view_count") or 0))
    return out
with cf.ThreadPoolExecutor(6) as ex:
    for L in ex.map(sq,Q):
        for c,n,v in L: chs.setdefault(c,[n,0]); chs[c][1]=max(chs[c][1],v)
top=sorted(chs.items(),key=lambda x:-x[1][1])[:70]; print(len(chs),"channels, scanning",len(top),file=sys.stderr)
def scan(x):
    c,(n,_)=x; E=[e for e in (flat(f"https://www.youtube.com/channel/{c}/videos",45).get("entries") or []) if e and e.get("view_count") and (e.get("duration") or 0)>150]
    if len(E)<8: return []
    med=st.median(e["view_count"] for e in E); return [(e["view_count"]/max(med,1),e["view_count"],med,k,len(E),n,e["title"],int(e["duration"]),e["id"]) for k,e in enumerate(E)]
R=[]
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(scan,top): R+=r
json.dump(R,open(sys.argv[1],"w"))
W=[r for r in R if re.search(r"what if|what would|if you|if everyone|if humans|every time|suddenly|for (a|24|one|\d+)|woke up|survive",r[6],re.I)]
for r in sorted(W,key=lambda r:-r[0])[:70]:
    if r[1]>=40000 and r[0]>=2.2: print(f"{r[0]:5.1f}x {r[1]/1e3:8.0f}k (median {r[2]/1e3:.0f}k, #{r[3]+1}/{r[4]}) {r[7]//60}:{r[7]%60:02d} | {r[5][:22]} | {r[6][:95]} | {r[8]}")
