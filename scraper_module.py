import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.text
    raise Exception(f"Failed to fetch {url} - Status Code: {res.status_code}")

def clean_text(text):
    return ' '.join(text.strip().split())

def extract_all_data(soup, base_url=""):
    records = []
    for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "span", "a", "div", "section", "article"]):
        text = clean_text(tag.get_text())
        if not text:
            continue

        href = tag.get("href") or tag.get("src") or ""
        if href and not href.startswith("http"):
            href = base_url + href

        record = {
            "tag": tag.name,
            "class": " ".join(tag.get("class", [])),
            "id": tag.get("id", ""),
            "text": text,
            "link": href if tag.name == "a" else ""
        }
        records.append(record)
    
    return records

def auto_scrape_full(url):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    base_url = "/".join(url.split("/")[:3])
    return extract_all_data(soup, base_url=base_url)
