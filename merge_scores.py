#!/usr/bin/env python3
"""merge scores.json back into data.json"""
import json

BASE = "/home/ubuntu/investment"
with open(f"{BASE}/data/scores.json", "r", encoding="utf-8") as f:
    scores = json.load(f)

with open(f"{BASE}/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

score_map = {r["code"]: r for r in scores.get("stocks", [])}

updated = 0
for s in data.get("stocks", []):
    code = s.get("code", "")
    r = score_map.get(code)
    if not r:
        continue
    s["tier"] = r.get("tier", s.get("tier", "D"))
    s["tier_label"] = r.get("tier_label", "")
    s["tier_cls"] = r.get("tier_cls", "tier-t4")
    s["score"] = r.get("s1_raw") if r.get("track_assigned") == "S1" else r.get("s2_raw")
    s["s1_raw"] = r.get("s1_raw")
    s["s2_raw"] = r.get("s2_raw")
    s["dimensions"] = r.get("dimensions", {})
    s["action"] = r.get("action", {})
    s["track_assigned"] = r.get("track_assigned")
    updated += 1

data["updated"] = scores.get("generated", data.get("updated"))
data["scoring_rules_version"] = scores.get("rules_version", "")

with open(f"{BASE}/data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"[merge] updated {updated} stocks in data.json")
