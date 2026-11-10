"""Generate one MP3 per dialogue line with Microsoft neural voices (edge-tts).
Usage: python3 tools/make_audio.py lessons/W01.yaml
Shami lines are sent without vowel marks (tested: the ar-SY voices read plain text best);
MSA lines (lang: msa) keep their vowels."""
import asyncio, os, re, ssl, sys, yaml, edge_tts
import edge_tts.communicate as _c
ca = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
if os.path.exists(ca): _c._SSL_CTX = ssl.create_default_context(cafile=ca)
MSA_MALE, MSA_FEMALE = "ar-SA-HamedNeural", "ar-SA-ZariyahNeural"
TASHKIL = re.compile(r"[ً-ْٰ]")
async def one(text, cast, path):
    if os.path.exists(path) and os.path.getsize(path) > 0: return
    kw = {k: cast[k] for k in ("pitch", "rate") if k in cast}
    await edge_tts.Communicate(text, cast["voice"], **kw).save(path)
async def main(src):
    d = yaml.safe_load(open(src)); jobs = []
    for L in d["lessons"]:
        os.makedirs(f"audio/{L['id']}", exist_ok=True)
        for i, ln in enumerate(L.get("lines", []), 1):
            t = ln["ar"] if ln.get("lang") == "msa" else TASHKIL.sub("", ln["ar"])
            t = t.replace("«", "").replace("»", "").replace("ٰ", "")
            jobs.append(one(t, d["cast"][ln["who"]], f"audio/{L['id']}/{i:02d}.mp3"))
        # bridge side-by-side: the MSA half, read by a standard-Arabic voice of the speaker's gender
        lines = {x["id"]: x.get("lines", []) for x in d["lessons"]}
        for i, sd in enumerate(L.get("sides", []), 1):
            who = lines[sd["ref"][0]][sd["ref"][1] - 1]["who"]
            male = d["cast"][who]["voice"] == "ar-SY-LaithNeural"
            msa = {"voice": MSA_MALE if male else MSA_FEMALE}
            jobs.append(one(sd["msa"]["ar"].replace("ٰ", "ا"), msa, f"audio/{L['id']}/m{i:02d}.mp3"))
    for k in range(0, len(jobs), 6): await asyncio.gather(*jobs[k:k+6])
    print(len(jobs), "lines")
asyncio.run(main(sys.argv[1]))
