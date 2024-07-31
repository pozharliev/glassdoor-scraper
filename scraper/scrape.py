import logging
import json
import re
import nodriver as uc
from bs4 import BeautifulSoup

logging.getLogger("uc.connection").setLevel(logging.CRITICAL)
logging.getLogger("websockets.client").setLevel(logging.CRITICAL)
logging.getLogger().setLevel(logging.DEBUG)


async def scrape_page():
    browser = await uc.start(sandbox=False, headless=False)

    logging.debug("Started browser")

    page = await browser.get("https://www.glassdoor.com/Interview/SAP-Interview-Questions-E10471.htm")

    logging.debug("Visiting url")

    await page.fullscreen()
    await page.wait(5)

    curr_height = prev_height = 0
    diff = -1

    while diff != 0:
        await page.scroll_down(300)

        logging.debug("Scrolling down")

        await page.wait(2)

        prev_height = curr_height
        curr_height = await page.evaluate("document.documentElement.scrollHeight")
        diff = curr_height - prev_height

    content = await page.get_content()
    soup = BeautifulSoup(content, "lxml")

    interview_list = soup.find("div", {"data-test": "InterviewList"}) \
        .find_all("div", {"data-test": lambda x: x and x.startswith("Interview")})

    for item in interview_list:
        title = item.find("h2", {
            "class": "header__header-module__h2"
        })

        print(title.text)


async def main():
    await scrape_page()


if __name__ == '__main__':
    uc.loop().run_until_complete(main())
