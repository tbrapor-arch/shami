"""Build a single self-contained preview page for one week: python3 tools/build_preview.py lessons/W01.yaml preview/week1.html"""
import base64, json, sys, yaml
src, out = sys.argv[1], sys.argv[2]
d = yaml.safe_load(open(src))
for L in d["lessons"]:
    for i, ln in enumerate(L.get("lines", []), 1):
        ln["audio"] = base64.b64encode(open(f"audio/{L['id']}/{i:02d}.mp3", "rb").read()).decode()
        ln["name"] = d["cast"][ln["who"]]["name"]
data = json.dumps(d["lessons"], ensure_ascii=False).replace("</", "<\\/")
open(out, "w").write(open("tools/preview_template.html").read().replace("/*DATA*/[]", data).replace("{{WEEK}}", str(d["week"])))
print(out, len(data) // 1024, "KB")
