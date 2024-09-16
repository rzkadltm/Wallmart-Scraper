import time
import asyncio
from fake_useragent import UserAgent
from playwright.async_api import async_playwright

ua = UserAgent(os=["macos", "linux"], browsers="safari")
user_agent = ua.random

accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

headers={"Referer":"https://www.google.com","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Accept":accept,"User-Agent":user_agent}

async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = await browser_type.launch(headless=False)
            page = await browser.new_page()
            page.set_extra_http_headers(headers)
            await page.goto('https://www.walmart.com/search?q=laptop')
            import pdb
            pdb.set_trace()
            await browser.close()
            break

asyncio.run(main())