"""Build a single self-contained preview page for one week: python3 tools/build_preview.py lessons/W01.yaml preview/week1.html"""
import base64, json, sys, yaml
src, out = sys.argv[1], sys.argv[2]
d = yaml.safe_load(open(src))
for L in d["lessons"]:
    for i, ln in enumerate(L.get("lines", []), 1):
        ln["audio"] = base64.b64encode(open(f"audio/{L['id']}/{i:02d}.mp3", "rb").read()).decode()
        ln["name"] = d["cast"][ln["who"]]["name"]
lines = {L["id"]: L.get("lines", []) for L in d["lessons"]}
nums = {L["id"]: L["n"] for L in d["lessons"]}
for L in d["lessons"]:
    for i, sd in enumerate(L.get("sides", []), 1):
        lid, k = sd["ref"]
        sd["sh"] = lines[lid][k - 1]
        sd["lesson"] = nums[lid]
        sd["msa"]["audio"] = base64.b64encode(open(f"audio/{L['id']}/m{i:02d}.mp3", "rb").read()).decode()
# lesson notes: one numbered badge per note, at the end of its line (Tsheh-tû style)
import re
for L in d["lessons"]:
    for ln in L.get("lines", []): ln["marks"] = []
    for k, n in enumerate(L.get("notes", [])):
        L["lines"][n["line"] - 1]["marks"].append([0, 0, k])

# bridge notes and rules: write each cited word as {Arabic|transcription}, like the lesson notes
CITE = {
 "iš-Šām": "الشّام", "Dimašq": "دِمَشْق", "fī": "في", "hādhā": "هٰذا", "hāda": "هادا", "bayt": "بَيْت", "bēt": "بَيْت",
 "hal-waqt": "هالوَقْت", "al-ʔāna": "الآن", "kīf": "كيف", "kayf": "كَيْف", "sitti": "سِتّي", "laysa": "لَيْسَ",
 "lākinna": "لٰكِنَّ", "lākin": "لٰكِن", "jiddan": "جِدًّا", "ʔanta": "أَنْتَ", "ʔinte": "اِنْتَ", "ʔanti": "أَنْتِ", "ʔinti": "اِنْتي",
 "ta3bān": "تَعْبان", "mut3ab": "مُتْعَب", "3andi": "عَنْدي", "kathīr": "كَثير", "ktīr": "كْتير", "jaw3ān": "جَوْعان",
 "jū3ān": "جوعان", "qahwa": "قَهْوة", "ʔahwe": "قَهْوة", "yawm": "يَوْم", "yōm": "يوم", "il-Qurʔān": "القُرْآن",
 "šū": "شو", "mā": "ما", "hōn": "هَوْن", "hunā": "هُنا", "hunāka": "هُناك", "hnīk": "هْنيك", "mū": "مو", "bass": "بَسّ",
 "wēn": "وَيْن", "ʔayna": "أَيْنَ", "rāḥ": "راح", "dhahaba": "ذَهَبَ", "ištaɣal": "اِشْتَغَل", "ištaɣala": "اِشْتَغَلَ",
 "3amila": "عَمِلَ", "3imil": "عِمِل", "fa3ala": "فَعَلَ", "ʔarāda": "أَرادَ", "katab": "كَتَب", "kataba": "كَتَبَ",
 "ḥabb": "حَبّ", "ʔaḥabba": "أَحَبَّ", "ʔakal": "أَكَل", "ʔakala": "أَكَلَ", "ʔan": "أَنْ", "lam": "لَمْ", "lan": "لَنْ",
 "lā": "لا", "hal": "هَلْ", "šayʔ": "شَيْء", "šī": "شي", "laḥm": "لَحْم", "laḥme": "لَحْمة", "xuḍār": "خُضار",
 "xuḍra": "خُضْرة", "širke": "شِرْكة", "šarika": "شَرِكة", "taʔkul": "تَأْكُل", "tākul": "تاكُل", "katabt": "كَتَبْت",
 "katabat": "كَتَبَتْ", "katbit": "كَتْبِت", "katabtum": "كَتَبْتُم", "katabta": "كَتَبْتَ", "biḥibb": "بيحِبّ",
 "bḥibb": "بْحِبّ", "btḥibb": "بْتْحِبّ", "minḥibb": "مِنْحِبّ", "yaktubu": "يَكْتُبُ", "ʔan yaktuba": "أَنْ يَكْتُبَ",
 "lam yaktub": "لَمْ يَكْتُبْ", "al-bāriḥa": "البارِحة", "ʔilā": "إِلى", "riḥt": "رِحْت", "biddi": "بِدّي",
 "biddi ʔiktub": "بِدّي اِكْتُب", "lastu": "لَسْتُ", "bunayya": "بُنَيَّ", "ʔuḥibbu": "أُحِبُّ", "tuḥibbu": "تُحِبُّ",
 "yuḥibbu": "يُحِبُّ", "ʔahla": "أَهْلا", "mnīḥa": "مْنيحة", "ta3bāne": "تَعْبانة", "mut3abatan": "مُتْعَبَةً",
 "ʔixt": "إخْت", "ʔuxt": "أُخْت", "maṭar": "مَطَر", "hallaʔ": "هَلَّق", "3ammo": "عَمّو", "lahu": "لَهُ",
}
def cite(text, extra):
    keys = {**CITE, **extra}
    taken = [(m.start(), m.end()) for m in re.finditer(r"\{[^{}]*\}", text)]
    for k in sorted(keys, key=len, reverse=True):
        for m in re.finditer(r"(?<![\w-])" + re.escape(k) + r"(?![\w])", text):
            if any(a < m.end() and m.start() < b for a, b in taken): continue
            rep = "{" + keys[k] + "|" + k + "}"
            text = text[:m.start()] + rep + text[m.end():]
            d_ = len(rep) - (m.end() - m.start())
            taken = [(a + d_ if a >= m.end() else a, b + d_ if b >= m.end() else b) for a, b in taken] + [(m.start(), m.start() + len(rep))]
            break
    return text
for L in d["lessons"]:
    if not L.get("sides"): continue
    extra = {}
    for sd in L["sides"]:
        for h in sd["hl"]:
            extra[h[1]] = h[0]; extra[h[3]] = h[2]
    for sd in L["sides"]:
        for h in sd["hl"]:
            if len(h) > 5: h[5] = cite(h[5], extra)
    for r in L.get("rules", []): r["text"] = cite(r["text"], extra)
data = json.dumps(d["lessons"], ensure_ascii=False).replace("</", "<\\/")
open(out, "w").write(open("tools/preview_template.html").read().replace("/*DATA*/[]", data).replace("{{WEEK}}", str(d["week"])))
print(out, len(data) // 1024, "KB")
