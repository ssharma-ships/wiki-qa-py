import json
import time
import urllib.request
import urllib.parse
import urllib.error

MEDIAWIKI_API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "ClaudeWikiQA/0.1 (prompt-eng-takehome; contact@example.com)"
EXTRACT_LIMIT = 1500
RATE_LIMIT_SLEEP = 0.1
RETRY_SLEEP = 1.0


def search_wikipedia(query: str, k: int = 3) -> dict:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": str(k),
        "prop": "extracts|pageprops|info",
        "exintro": "1",
        "explaintext": "1",
        "exlimit": str(k),
        "ppprop": "disambiguation",
        "inprop": "url",
        "redirects": "1",
    }
    url = MEDIAWIKI_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    def fetch() -> bytes:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read()

    raw = None
    for attempt in range(2):
        try:
            raw = fetch()
        except Exception as exc:
            if attempt == 0:
                time.sleep(RETRY_SLEEP)
            else:
                return {"query": query, "results": [], "error": str(exc)}

    time.sleep(RATE_LIMIT_SLEEP)

    data = json.loads(raw)
    pages = data.get("query", {}).get("pages", {})

    if not pages:
        return {"query": query, "results": []}

    sorted_pages = sorted(pages.values(), key=lambda p: p.get("index", 9999))

    results = []
    for page in sorted_pages:
        extract = page.get("extract") or ""
        if len(extract) > EXTRACT_LIMIT:
            extract = extract[:EXTRACT_LIMIT] + "... [truncated]"
        results.append({
            "title": page.get("title", ""),
            "extract": extract,
            "url": page.get("fullurl", ""),
            "is_disambiguation": "disambiguation" in page.get("pageprops", {}),
        })

    return {"query": query, "results": results}


if __name__ == "__main__":
    result = search_wikipedia("Marie Curie Nobel Prize")
    print(json.dumps(result, indent=2)[:2000])
