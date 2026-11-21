import json, re, html, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

# Ochiq o‘zbekcha RSS lenta. Sayt faqat o‘zbek tilidagi xabarlarni saralashga mo‘ljallangan.
FEEDS = [
    ("UzNet Press — o‘zbekcha RSS", "https://uznet.press/rss/today_uz.xml"),
]
KEYWORDS = {
    "Sun’iy intellekt": ["sun'iy intellekt", "sun’iy intellekt", "suniy intellekt", "sun'iy aql", "neyron", "chatgpt", "generativ ai", "machine learning"],
    "Dasturlash": ["dasturlash", "dasturchi", "python", "javascript", "java", "c++", "kod yozish", "open source", "ochiq kod"],
    "Kiberxavfsizlik": ["kiberxavfsizlik", "kiber hujum", "xaker", "firibgarlik", "ma'lumotlar xavfsizligi", "virus", "zararli dastur"],
    "Kompyuter va gadjetlar": ["kompyuter", "noutbuk", "smartfon", "telefon", "protsessor", "chip", "gadjet", "robot", "planshet"],
    "Telekommunikatsiya": ["internet", "5g", "aloqa", "telekommunikatsiya", "mobil tarmoq", "operator", "sun'iy yo'ldosh"],
    "Startap va biznes": ["startap", "texnopark", "it park", "raqamli iqtisodiyot", "raqamlashtirish", "fintech", "texnologik kompaniya"],
}
GENERAL = ["texnologiya", "raqamli", "axborot texnologiyalari", "it sohasi", "dasturiy ta'minot", "platforma", "ma'lumotlar bazasi"]
HEADERS = {"User-Agent": "ITNewsHub/1.0 (educational news aggregator)"}

def clean(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()

def child_text(node, names):
    for name in names:
        el = node.find(name)
        if el is not None and el.text:
            return el.text.strip()
    # RSS/Atom namespace bilan kelgan teglarni ham tekshirish
    for el in node.iter():
        if el.tag.split("}")[-1] in names and el.text:
            return el.text.strip()
    return ""

def parse_date(value):
    if not value:
        return ""
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except Exception:
        try:
            return datetime.fromisoformat(value.replace("Z","+00:00")).astimezone(timezone.utc).isoformat()
        except Exception:
            return ""

def categorize(text):
    t = text.casefold()
    best, score = None, 0
    for category, words in KEYWORDS.items():
        points = sum(1 for word in words if word.casefold() in t)
        if points > score:
            best, score = category, points
    general_hits = sum(1 for word in GENERAL if word in t)
    if best is None and general_hits:
        best, score = "IT va texnologiya", general_hits
    if best is None:
        return None, 0
    # Ball — faqat mavzuga moslik indikatori, fakt ishonchliligi emas.
    return best, min(99, 60 + score * 12 + min(general_hits, 2) * 4)

def parse_feed(source, url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as response:
        raw = response.read()
    root = ET.fromstring(raw)
    entries = [e for e in root.iter() if e.tag.split("}")[-1] in ("item", "entry")]
    results = []
    for entry in entries:
        title = clean(child_text(entry, ["title"]))
        if not title:
            continue
        summary = clean(child_text(entry, ["description", "summary", "content"]))
        link = child_text(entry, ["link"])
        if not link:
            for el in entry.iter():
                if el.tag.split("}")[-1] == "link":
                    link = el.attrib.get("href", "") or (el.text or "")
                    if link: break
        if link and link.startswith("/"):
            from urllib.parse import urljoin
            link = urljoin(url, link)
        date = parse_date(child_text(entry, ["pubDate", "published", "updated", "date"]))
        category, score = categorize(title + " " + summary)
        if not category or not link.startswith(("http://","https://")):
            continue
        results.append({
            "title": title[:240], "summary": summary[:650],
            "url": link, "date": date, "source": source,
            "category": category, "score": score
        })
    return results

def main():
    all_items = []
    errors = []
    for source, url in FEEDS:
        try:
            all_items.extend(parse_feed(source, url))
            print(f"{source}: feed o‘qildi")
        except Exception as exc:
            errors.append(f"{source}: {type(exc).__name__}: {exc}")
            print(errors[-1])
    # Sarlavha bo‘yicha takrorlarni olib tashlash
    unique, seen = [], set()
    for item in all_items:
        key = re.sub(r"[^a-z0-9а-яўқғҳё]+", "", item["title"].casefold())
        if key and key not in seen:
            seen.add(key)
            item["id"] = str(abs(hash(key)))
            unique.append(item)
    unique.sort(key=lambda x: x.get("date",""), reverse=True)
    payload = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "articles": unique[:100],
        "source_errors": errors
    }
    Path("news.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Jami {len(unique)} ta ITga oid xabar yozildi.")

if __name__ == "__main__":
    main()
