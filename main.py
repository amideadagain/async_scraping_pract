import aiohttp
import asyncio
from bs4 import BeautifulSoup
# from time import monotonic


head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Connection": "keep-alive"
}


async def get_page(session, url):
    # print(f'getting {url}')
    try:
        async with session.get(f"https://{url}", headers=head) as response:
            # print(f'async {url}')
            html = await response.text()
            return {"html": html, "url": url}
    except aiohttp.ClientConnectorError:
        # print(f'Connection error to {url}, invalid url')
        pass
    except aiohttp.ClientResponseError:
        # print(f'Client response error to {url}')
        pass


async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    return await asyncio.gather(*tasks)


async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
        return data


def parse(results):
    for result in results:
        if result:
            soup = BeautifulSoup(result["html"], features="html.parser")
            title = soup.find('title')
            if title:
                print(f"{result['url']} - {title.text.strip()}")


if __name__ == "__main__":
    with open('news_sites.txt') as file:
        content = file.read().split('\n')
    all_urls = content

    # start = monotonic()

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    html_results = asyncio.run(main(all_urls))

    # end = monotonic()

    parse(html_results)

    # print(end - start)
