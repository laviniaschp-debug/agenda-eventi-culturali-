#!/usr/bin/env python3
"""Arricchisce events.json e genera i calendari per tema in cal/.

Uso (dalla cartella del sito):  python3 tools/enrich.py

Cosa fa, senza mai cancellare dati già presenti:
  - key      chiave stabile (data + titolo), utile per preferiti e link
  - cat      sposta in "scienza" gli eventi chiaramente scientifici
  - why      una riga editoriale "perché andarci": in tools/why.json, per chiave
             evento (es. "2026-11-28-filosofia-dell-amicizia") su qualsiasi evento,
             o per frammento del titolo sugli imperdibili. Scrivila come un bisogno
             o una domanda della vita, non come descrizione dell'evento.
  - moods    ridere / pensare / emozionarmi / gente / bambini
  - geo,zona coordinate indicative e quartiere, da tools/venues.json
  - status   lasciato com'è se presente (ultimi posti, esaurito)
Poi scrive cal/<tema>.ics e cal/tutto.ics.
"""
import json, re, os, unicodedata, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(ROOT, "events.json")
VEN = os.path.join(ROOT, "tools", "venues.json")
WHY = os.path.join(ROOT, "tools", "why.json")
CAL = os.path.join(ROOT, "cal")

CAT_NAMES = {
    "teatro": "Teatro", "comedy": "Stand-up comedy", "silent": "Silent reading", "talk": "Incontri e talk", "filosofia": "Filosofia",
    "storia": "Arte e storia", "geo": "Geopolitica", "salute": "Psiche e salute",
    "scienza": "Scienza", "classica": "Classica e chiese", "jazz": "Jazz e live",
    "cinema": "Cinema", "famiglie": "Famiglie", "tech": "Tech e digitale",
}

SCIENCE = re.compile(
    r"scienz|astronaut|astrofis|cristoforetti|ercoli finzi|biologic|neuroscien|"
    r"\bfisica|matematic|cervello|genetic|pievani|darwin|crisi climatica|"
    r"cambiamento climatico|intelligenza artificiale|cosmolog", re.I)

MOODS = {
    "ridere": re.compile(r"comic|commedia|cabaret|stand.?up|ironi|umoris|risat|"
                         r"bergonzoni|zerocalcare|satir|clown|improvvisaz", re.I),
    "gente": re.compile(r"laboratori|workshop|aperitiv|pratiche filosofiche|caff[eè] filosof|"
                        r"dibattito|discussione|festa|community|open day|swing|"
                        r"philo|cuccagna|base milano|jam|meetup|networking|coding night|aperitivo", re.I),
}
# "Guardarmi dentro": psicologia, filosofia, spiritualità, poesia, relazioni (calcolato sempre, anche su eventi già arricchiti)
DENTRO = re.compile(r"psicolog|psicoanal|psicoterap|filosof|spiritual|meditaz|mindful|anima\b|felicit|ansia|fragilit|"
                    r"identit|coscienza|introspez|autobiograf|confession|lutto|senso della vita|tempo che passa|"
                    r"poesia|poeti|amore|relazion|adolescen|crescita personale|recalcati|galimberti|lingiardi|vito mancuso|"
                    r"parola e musica|concerti? spirituali|avvento|quaresima", re.I)
MOOD_BY_CAT = {
    "pensare": {"talk", "filosofia", "geo", "storia", "scienza", "salute", "tech"},
    "emozionarmi": {"classica", "jazz", "teatro", "cinema"},
    "bambini": {"famiglie"},
    "ridere": {"comedy"},
    "gente": {"silent"},
}


KEYLIKE = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48]


def enrich(d, ven_path=VEN):
    venues = json.load(open(ven_path, encoding="utf-8"))
    why = json.load(open(WHY, encoding="utf-8")) if os.path.exists(WHY) else {}
    seen = {}
    for e in d["events"]:
        k = f'{e["date"]}-{slug(e["title"])}'
        if k in seen:
            seen[k] += 1
            k = f"{k}-{seen[k]}"
        else:
            seen[k] = 1
        e["key"] = k
        # BookCity Milano: tutti gli eventi sono a ingresso libero fino a esaurimento posti, salvo diverse indicazioni
        if e.get("free") is None and ("bookcity" in (e.get("tags") or []) or "bookcity" in f'{e["title"]} {e.get("desc","")} {e.get("url","")}'.lower()):
            e["free"] = True
            if "prenot" not in e.get("desc", "").lower():
                e["desc"] = (e.get("desc", "").rstrip() + " BookCity: ingresso libero fino a esaurimento posti, per alcuni incontri serve prenotare su bookcitymilano.it.").strip()
        text = f'{e["title"]} {e.get("desc","")} {e.get("venue","")}'
        stext = f'{e["title"]} {e.get("desc","")}'
        if e.get("cat") not in ("famiglie", "tech", "filosofia") and SCIENCE.search(stext) and "ideologic" not in stext.lower():
            e["cat"] = "scienza"
        # "perché andarci": chiave esatta dell'evento (qualsiasi evento) oppure frammento del titolo (solo imperdibili)
        if not e.get("why") and e["key"] in why:
            e["why"] = why[e["key"]]
        if not e.get("why") and "imperdibile" in e.get("tags", []):
            low = e["title"].lower()
            for frag, line in why.items():
                if KEYLIKE.match(frag):
                    continue
                if frag.lower() in low:
                    e["why"] = line
                    break
        if not e.get("moods"):
            m = [name for name, cats in MOOD_BY_CAT.items() if e.get("cat") in cats]
            for name, rx in MOODS.items():
                if rx.search(text):
                    m.append(name)
            e["moods"] = sorted(set(m))
        e["moods"] = [x for x in e["moods"] if x != "dentro"]
        if (e.get("cat") in ("filosofia", "salute") or DENTRO.search(stext)) and e.get("cat") not in ("famiglie", "tech", "jazz"):
            e["moods"] = sorted(set(e["moods"]) | {"dentro"})
        if not e.get("geo"):
            v = e.get("venue", "").lower()
            for row in venues:
                if row["match"].lower() in v:
                    e["geo"] = [row["lat"], row["lng"]]
                    e["zona"] = row["zona"]
                    break
    return d


# ---------- ICS ----------
VTZ = """BEGIN:VTIMEZONE
TZID:Europe/Rome
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE"""


def esc(s):
    return (s or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    b = line.encode("utf-8")
    if len(b) <= 75:
        return line
    out, cur = [], b""
    for ch in line:
        c = ch.encode("utf-8")
        if len(cur) + len(c) > (75 if not out else 74):
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += c
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


def vevent(e, stamp):
    d = e["date"].replace("-", "")
    lines = ["BEGIN:VEVENT", f'UID:{e["key"]}@acculturiamoci.it', f"DTSTAMP:{stamp}"]
    if e.get("time"):
        h, m = e["time"].split(":")
        start = dt.datetime.strptime(e["date"] + e["time"], "%Y-%m-%d%H:%M")
        end = start + dt.timedelta(hours=2)
        lines += [f"DTSTART;TZID=Europe/Rome:{start:%Y%m%dT%H%M%S}",
                  f"DTEND;TZID=Europe/Rome:{end:%Y%m%dT%H%M%S}"]
    else:
        nxt = (dt.date.fromisoformat(e["date"]) + dt.timedelta(days=1)).strftime("%Y%m%d")
        lines += [f"DTSTART;VALUE=DATE:{d}", f"DTEND;VALUE=DATE:{nxt}"]
    desc = " ".join(x for x in [e.get("why"), e.get("desc")] if x)
    lines += [f'SUMMARY:{esc(e["title"])}', f'LOCATION:{esc(e.get("venue"))}',
              f'DESCRIPTION:{esc((desc + " ") if desc else "")}{esc(e.get("url"))}',
              f'URL:{e.get("url","")}', f'CATEGORIES:{esc(CAT_NAMES.get(e["cat"], e["cat"]))}',
              "END:VEVENT"]
    return lines


def write_ics(name, title, events):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//acculturiamoci.it//IT",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH", f"X-WR-CALNAME:{esc(title)}",
             "X-WR-TIMEZONE:Europe/Rome", "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
             "X-PUBLISHED-TTL:PT12H"]
    lines += VTZ.split("\n")
    for e in events:
        lines += vevent(e, stamp)
    lines.append("END:VCALENDAR")
    with open(os.path.join(CAL, name), "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(fold(l) for l in lines) + "\r\n")


CITIES = [  # file eventi, file luoghi, prefisso calendari, nome
    ("events.json", "venues.json", "", "Milano"),
    ("roma.json", "venues-roma.json", "roma-", "Roma"),
    ("firenze.json", "venues-firenze.json", "firenze-", "Firenze"),
    ("torino.json", "venues-torino.json", "torino-", "Torino"),
]


def main():
    from collections import Counter
    os.makedirs(CAL, exist_ok=True)
    for ev_file, ven_file, pre, city in CITIES:
        path = os.path.join(ROOT, ev_file)
        if not os.path.exists(path):
            continue
        d = json.load(open(path, encoding="utf-8"))
        enrich(d, os.path.join(ROOT, "tools", ven_file))
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        evs = sorted(d["events"], key=lambda e: (e["date"], e.get("time") or "99"))
        write_ics(f"{pre}tutto.ics", f"Acculturiamoci · {city}", evs)
        for cat, name in CAT_NAMES.items():
            write_ics(f"{pre}{cat}.ics", f"Acculturiamoci {city} · {name}", [e for e in evs if e["cat"] == cat])
        write_ics(f"{pre}musica.ics", f"Acculturiamoci {city} · Musica e concerti", [e for e in evs if e["cat"] in ("classica", "jazz")])
        write_ics(f"{pre}imperdibili.ics", f"Acculturiamoci {city} · Imperdibili", [e for e in evs if "imperdibile" in e.get("tags", [])])
        print(city, "eventi:", len(evs), dict(Counter(e["cat"] for e in evs)),
              "| con geo:", sum(1 for e in evs if e.get("geo")))


if __name__ == "__main__":
    main()
