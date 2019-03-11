# coding = UTF-8

import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url, timeout=60 * 60) as response:
        return await response.text()

async def fetch_all_urls(session, urls):
    results = await asyncio.gather(*[fetch_url(session, url) for url in urls], return_exceptions=True)
    return results

async def session_fetch(urls):
    async with aiohttp.ClientSession() as session:
        html = await fetch_all_urls(session, urls)
    return html

def get_htmls(urls):
    loop = asyncio.get_event_loop()
    htmls = loop.run_until_complete(session_fetch(urls))
    raw_result = dict(zip(urls, htmls))

    return raw_result

result_dict = get_htmls(['http://college.gaokao.com/','http://college.gaokao.com/schpoint/a100/b100/?'])
print(len(result_dict))