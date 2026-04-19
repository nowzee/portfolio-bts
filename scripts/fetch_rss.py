"""
Fetch cybersecurity RSS feeds and generate assets/data/news.json.
Auto-categorizes by keywords. Run via GitHub Actions every 6h.
"""
import json
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

FEEDS = [
    ("BleepingComputer",   "https://www.bleepingcomputer.com/feed/"),
    ("The Hacker News",    "https://feeds.feedburner.com/TheHackersNews"),
    ("Krebs on Security",  "https://krebsonsecurity.com/feed/"),
    ("CERT-FR (Avis)",     "https://www.cert.ssi.gouv.fr/avis/feed/"),
    ("CERT-FR (Alertes)",  "https://www.cert.ssi.gouv.fr/alerte/feed/"),
    ("SANS ISC",           "https://isc.sans.edu/rssfeed.xml"),
    ("Dark Reading",       "https://www.darkreading.com/rss.xml"),
]

MAX_PER_FEED = 8
MAX_TOTAL    = 40
USER_AGENT   = "Mozilla/5.0 (compatible; PortfolioBTS-Veille/1.0)"

NS = {"atom": "http://www.w3.org/2005/Atom"}

CATEGORY_RULES = [
    ("cve",        r"\b(cve-\d{4}-\d{3,7}|zero[- ]?day|0-?day|vulnerability|vulnérabilit|patch|advisory|critical flaw)\b"),
    ("ransomware", r"\b(ransomware|lockbit|blackcat|alphv|cl0p|royal|akira|rançongiciel|extortion)\b"),
    ("apt",        r"\b(apt[- ]?\d+|lazarus|fancy bear|cozy bear|kimsuky|sandworm|state[- ]sponsored|nation[- ]state|threat actor|chinese hackers|russian hackers)\b"),
    ("malware",    r"\b(malware|trojan|loader|stealer|infostealer|backdoor|rat|botnet|spyware|wiper|dropper|emotet|qakbot|raccoon|lumma)\b"),
    ("outil",      r"\b(open[- ]source|github|new tool|released|wireshark|nmap|burp|metasploit|sigma|yara|misp|opencti)\b"),
]

def categorize(text: str) -> str:
    t = text.lower()
    for cat, pattern in CATEGORY_RULES:
        if re.search(pattern, t):
            return cat
    return "actualite"

def strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s or "")
    s = unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def truncate(s: str, n: int = 240) -> str:
    if len(s) <= n:
        return s
    cut = s[: n - 1]
    cut = cut.rsplit(" ", 1)[0]
    return cut + "…"

def parse_date(raw: str):
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw)
    except Exception:
        pass
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except Exception:
        return None

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")

def parse_rss(xml_text: str, source_name: str):
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"  [parse error] {source_name}: {e}", file=sys.stderr)
        return items

    # RSS 2.0
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link  = (it.findtext("link") or "").strip()
        desc  = strip_html(it.findtext("description") or "")
        date  = parse_date(it.findtext("pubDate") or "")
        if title and link:
            items.append((title, link, desc, date))

    # Atom
    if not items:
        for it in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title = (it.findtext("atom:title", namespaces=NS) or "").strip()
            link_el = it.find("atom:link", namespaces=NS)
            link = link_el.get("href") if link_el is not None else ""
            desc = strip_html(it.findtext("atom:summary", namespaces=NS) or "")
            date = parse_date(it.findtext("atom:updated", namespaces=NS) or "")
            if title and link:
                items.append((title, link, desc, date))

    return items[:MAX_PER_FEED]

def main():
    out_root = Path(__file__).resolve().parent.parent
    out_dir  = out_root / "assets" / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "news.json"

    all_items = []
    for source, url in FEEDS:
        print(f"[fetch] {source}")
        try:
            xml_text = fetch(url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            print(f"  [skip] {source}: {e}", file=sys.stderr)
            continue
        for title, link, desc, date in parse_rss(xml_text, source):
            text_for_cat = f"{title} {desc}"
            all_items.append({
                "title":    title,
                "url":      link,
                "summary":  truncate(desc, 240) if desc else "",
                "date":     (date.astimezone(timezone.utc).strftime("%Y-%m-%d") if date else ""),
                "date_iso": (date.astimezone(timezone.utc).isoformat() if date else ""),
                "source":   source,
                "category": categorize(text_for_cat),
            })

    all_items.sort(key=lambda x: x["date_iso"], reverse=True)
    all_items = all_items[:MAX_TOTAL]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count":        len(all_items),
        "items":        all_items,
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] wrote {len(all_items)} items -> {out_path}")

if __name__ == "__main__":
    main()
