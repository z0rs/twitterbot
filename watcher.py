import asyncio
from playwright.sync_api import sync_playwright
import time
import requests

# GANTI INI DULU
ACCOUNT_USERNAME = "LordEn0"
TELEGRAM_BOT_TOKEN = "7642048703C9Rr-Zge3dhrhHeeZLGs7aIaz-MD0"
TELEGRAM_CHAT_ID = "1811119074"

cookies = [  # ← PASTE cookies dari hasil konversi sebelumnya
    {"name": "auth_token", "value": "74d669327b3e5097f3fbc955cf618abf404b95ec", "domain": ".x.com", "path": "/"},
    {"name": "_ga_RJGMY4G45L", "value": "GS2.1.s1749136048$o4$g1$t1749137176$j60$l0$h0", "domain": ".x.com", "path": "/"},
    {"name": "ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog", "value": "%7B%22distinct_id%22%3A%2201970062-7eb6-732e-a496-a176fc7b29e1%22%2C%22%24sesid%22%3A%5B1748363153400%2C%2201971287-5523-7b01-9979-8d5fc7bce719%22%2C1748362548515%5D%7D", "domain": ".x.com", "path": "/"},
    {"name": "guest_id", "value": "v1%3A174913516985746511", "domain": ".x.com", "path": "/"},
    {"name": "ads_prefs", "value": "\"HBIRAAA=\"", "domain": ".x.com", "path": "/"},
    {"name": "_ga", "value": "GA1.2.276119402.1735115976", "domain": ".x.com", "path": "/"},
    {"name": "twid", "value": "u%3D2210253615", "domain": ".x.com", "path": "/"},
    {"name": "lang", "value": "en", "domain": "x.com", "path": "/"},
    {"name": "night_mode", "value": "1", "domain": ".x.com", "path": "/"},
    {"name": "des_opt_in", "value": "Y", "domain": ".x.com", "path": "/"},
    {"name": "__cf_bm", "value": "bJ0Pj.wid4Nc_HGJbBYVauIhNu524XWOS8v.lKsar4w-1749220565-1.0.1.1-K2ctWmDeOYPU7foR4NCAc3.40cj2U66KGATKEeCycEpeFMubZYwFE8UB4TBdvmmsLv8zc7Ls756flqoE.IO5fCw.iiKrK9ATaVjxnH1pgt8", "domain": ".x.com", "path": "/"},
    {"name": "_bl_uid", "value": "dRmj75tX7kzejskOIyF1nj9mvz2z", "domain": "x.com", "path": "/"},
    {"name": "_ga_BLY4P7T5KW", "value": "GS2.1.s1748798362$o5$g1$t1748798713$j43$l0$h0", "domain": ".x.com", "path": "/"},
    {"name": "_gid", "value": "GA1.2.1541834109.1749136072", "domain": ".x.com", "path": "/"},
    {"name": "ct0", "value": "a96020fd4099fda65c3399833b94353ee8b96879ab84649efa330903e7cc212086df500adaddd60557d05cfe9072b92fa6951099eeb8ba6c001a3df41158856b89952b377614361b9d459bafbb620153", "domain": ".x.com", "path": "/"},
    {"name": "guest_id_ads", "value": "v1%3A174913516985746511", "domain": ".x.com", "path": "/"},
    {"name": "guest_id_marketing", "value": "v1%3A174913516985746511", "domain": ".x.com", "path": "/"},
    {"name": "kdt", "value": "XVsbsBs7jKggk3MV5mRR4DKzA0OFhcF70QJI4quR", "domain": ".x.com", "path": "/"},
    {"name": "personalization_id", "value": "\"v1_xvYTyqFuGZ8aaneB7L9lhA==\"", "domain": ".x.com", "path": "/"}
]

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, data=data)

def get_latest_tweet_url(page):
    tweet = page.query_selector('article a time')
    if not tweet:
        return None
    parent = tweet.evaluate_handle("node => node.closest('a')")
    tweet_url = parent.get_attribute('href')
    return f"https://x.com{tweet_url}" if tweet_url else None

def main():
    last_tweet = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()

        while True:
            try:
                page.goto(f"https://x.com/{ACCOUNT_USERNAME}", timeout=60000)
                page.wait_for_timeout(5000)

                tweet_url = get_latest_tweet_url(page)
                if tweet_url and tweet_url != last_tweet:
                    last_tweet = tweet_url
                    print("New tweet detected:", tweet_url)
                    send_telegram(f"🚨 New tweet by @{ACCOUNT_USERNAME}:\n{tweet_url}")
                else:
                    print("No new tweet.")
            except Exception as e:
                print("Error:", e)

            time.sleep(60)

if __name__ == "__main__":
    main()

