import requests
from bs4 import BeautifulSoup

def crawl_site(start_url):
    print(f"[*] بدأ الزحف على: {start_url}")
    visited = set()
    urls_to_visit = [start_url]

    while urls_to_visit:
        url = urls_to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        try:
            res = requests.get(url, timeout=5)
            print(f"[+] تم زيارة: {url}")
            soup = BeautifulSoup(res.text, "html.parser")
            for link in soup.find_all("a", href=True):
                link_url = link['href']
                if link_url.startswith("http") and link_url not in visited:
                    urls_to_visit.append(link_url)
        except:
            pass

if __name__ == "__main__":
    # ✅ ضع هنا الرابط المستهدف مباشرة
    target = "https://testphp.vulnweb.com"
    crawl_site(target)
