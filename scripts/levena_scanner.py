import requests
import json
import os

# Credenciais Integradas
EXA_API_KEY = "85b465a0-5b38-4f87-b5b4-0244d1b36ad5"
FIRECRAWL_API_KEY = "fc-cc16271ba2f84059b5fc0cf67d26d9a3"

def search_news():
    print("🔍 [Exa] Buscando tendências institucionais...")
    url = "https://api.exa.ai/search"
    headers = {"x-api-key": EXA_API_KEY, "Content-Type": "application/json"}
    payload = {
        "query": "most critical crypto market news for BTC, ETH and smart money flows",
        "category": "news",
        "num_results": 2,
        "type": "auto"
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json().get('results', [])

def crawl_content(target_url):
    print(f"🕸️ [Firecrawl] Extraindo dados de: {target_url}")
    url = "https://api.firecrawl.dev/v1/scrape"
    headers = {"Authorization": f"Bearer {FIRECRAWL_API_KEY}", "Content-Type": "application/json"}
    payload = {"url": target_url, "formats": ["markdown"]}
    res = requests.post(url, headers=headers, json=payload)
    return res.json().get('data', {}).get('markdown', '')

if __name__ == "__main__":
    news_items = search_news()
    for item in news_items:
        print(f"\n📰 Notícia encontrada: {item['title']}")
        # content = crawl_content(item['url']) # Ativar quando precisarmos do texto completo
        # print(content[:500] + "...")
