# Shami · شامي

A free, progressive 100-lesson course in **Syrian (Damascene) Arabic**, in the spirit of the classic
"one lesson a day" method, with **bridge lessons to Modern Standard Arabic** after every revision.

- Explanations in English; Arabic script with partial vowels, plus a transcription line.
- One continuing story: Adam, who grew up in Paris, comes to Damascus to meet his family and learn to speak.
- Synthetic Syrian voices (Microsoft neural, ar-SY) as a guide to rhythm and melody, not a native speaker.

The plan is in [SYLLABUS.md](SYLLABUS.md). The course text is written from scratch for this project.

## Layout

| Path | What |
|---|---|
| `lessons/W01.yaml` | week 1: lessons 1–7 and bridge B1 (dialogue, notes, words, practice) |
| `audio/<lesson>/<line>.mp3` | synthetic voice for each dialogue line |
| `tools/make_audio.py` | generates the audio (`pip install edge-tts pyyaml`) |
| `tools/build_preview.py` | builds a single-file preview page of one week |
