from pathlib import Path
import json
from tqdm import tqdm

# -----------------------
# PATHS
# -----------------------

BASE = Path("animegamedata2")

TEXTMAP_MEDIUM_EN = BASE / "TextMap" / "TextMap_MediumEN.json"
TEXTMAP_MEDIUM_CHS = BASE / "TextMap" / "TextMap_MediumCHS.json"
TEXTMAP_EN = BASE / "TextMap" / "TextMapEN.json"
TEXTMAP_CHS = BASE / "TextMap" / "TextMapCHS.json"

SUBTITLES_EN = BASE / "Subtitle" / "EN"
SUBTITLES_CHS = BASE / "Subtitle" / "CHS"

READABLE_EN = BASE / "Readable" / "EN"
READABLE_CHS = BASE / "Readable" / "CHS"

# -----------------------
# PARSERS
# -----------------------

def parse_subtitle(subtitles):
    return {
        file.stem: file.read_text(encoding="utf-8")
        for file in subtitles.glob("*.srt")
    }
def parse_readable(readable):
    return {
        file.stem: file.read_text(encoding="utf-8")
        for file in readable.glob("*.txt")
    }
def parse_textmap(textmap):
    with textmap.open("r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------
# LOADERS
# -----------------------

def normalize(d):
    return {str(k): v for k, v in d.items()}

def load_textmap():
    en = normalize(parse_textmap(TEXTMAP_EN))
    en.update(normalize(parse_textmap(TEXTMAP_MEDIUM_EN)))

    chs = normalize(parse_textmap(TEXTMAP_CHS))
    chs.update(normalize(parse_textmap(TEXTMAP_MEDIUM_CHS)))

    rows = []
    all_ids = set(en.keys()) | set(chs.keys())

    for text_id in tqdm(sorted(all_ids, key=int), desc="TextMaps"):
        if not en.get(text_id):
            continue

        rows.append({
            "id": text_id,
            "en": en.get(text_id),
            "chs": chs.get(text_id),
            "source": "textmap",
        })
    return rows
def load_subtitle():
    en = {
        k.removesuffix("_EN"): v
        for k, v in parse_subtitle(SUBTITLES_EN).items()
    }

    chs = {
        k.removesuffix("_CHS"): v
        for k, v in parse_subtitle(SUBTITLES_CHS).items()
    }

    rows = []
    all_ids = set(en) | set(chs)

    for subtitle_id in tqdm(sorted(all_ids), desc="Subtitles"):
        rows.append({
            "id": subtitle_id,
            "en": en.get(subtitle_id),
            "chs": chs.get(subtitle_id),
            "source": "subtitle",
        })

    return rows
def load_readable():
    en = {
        k.removesuffix("_EN"): v
        for k, v in parse_readable(READABLE_EN).items()
    }

    chs = parse_readable(READABLE_CHS)

    rows = []
    all_ids = set(en) | set(chs)

    for readable_id in tqdm(sorted(all_ids), desc="Readables"):
        rows.append({
            "id": readable_id,
            "en": en.get(readable_id),
            "chs": chs.get(readable_id),
            "source": "readable",
        })

    return rows

# -----------------------
# RUN PIPELINE
# -----------------------

def combine_textmap():
    combined_textmap = load_textmap()
    combined_readable = load_readable()
    combined_subtitle = load_subtitle()

    final_textmap = []
    final_textmap.extend(combined_textmap)
    final_textmap.extend(combined_readable)
    final_textmap.extend(combined_subtitle)

    return final_textmap

