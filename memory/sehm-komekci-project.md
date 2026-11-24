---
name: sehm-komekci-project
description: "Personal stock-learning app ~/sehm-komekci (Streamlit, $20-50 budget, Azerbaijani UI) — paused 2026-11-24 before first run"
metadata:
  node_type: memory
  type: project
  originSessionId: 64c11a52-b401-4055-8aea-1db3a6673a64
  modified: 2026-11-23T22:02:27.954Z
---

User wants a personal stock (not crypto) analysis helper; they only have $20–50, so keep it honest (no price predictions, no leverage).
Built 2026-11-24 in ~/sehm-komekci: app.py (Streamlit tabs: analysis, backtest, virtual $50 portfolio, Claude explanation), data.py, backtest.py, paper.py, ai.py, start.sh, README.md.

**Status:** `uv pip install --python .venv streamlit yfinance pandas plotly anthropic` was stopped midway (slow internet, ~100 KB/s); uv cache keeps the downloads. Code has NOT been run or tested yet.
**How to apply:** next session, rerun the install, start `./start.sh`, fix any errors, then show the user. Telegram alerts were proposed as a later step.
