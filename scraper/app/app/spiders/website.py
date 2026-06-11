import requests
import scrapy
from urllib.parse import urlparse
import os

API_URL = os.getenv("API_URL")

if not API_URL:
    raise RuntimeError("API_URL is not set")


class WebsiteSpider(scrapy.Spider):
    name = "website"
    allowed_domains = ["tipsbymoh.tech"]
    start_urls = ["https://tipsbymoh.tech"]

    visited_urls = set()

    def parse(self, response):
        if response.url in self.visited_urls:
            return

        self.visited_urls.add(response.url)

        text_parts = response.css(
            "main ::text, article ::text, section ::text, p::text, h1::text, h2::text, h3::text, li::text"
        ).getall()

        page_text = " ".join(text_parts)
        page_text = " ".join(page_text.split())

        if page_text:
            requests.post(
                API_URL,
                json={
                    "url": response.url,
                    "chunk_text": page_text,
                },
                timeout=30,
            )

        for link in response.css("a::attr(href)").getall():
            next_url = response.urljoin(link)

            if self.is_internal_url(next_url):
                yield scrapy.Request(next_url, callback=self.parse)

    def is_internal_url(self, url: str) -> bool:
        parsed = urlparse(url)
        return parsed.netloc in ["tipsbymoh.tech", "www.tipsbymoh.tech"]