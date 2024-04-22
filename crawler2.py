import scrapy 
import os
import re
import uuid
import pickle

from scrapy.linkextractors import LinkExtractor

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    custom_settings = {
        "LOG_LEVEL": "INFO"
    }
    max_depth = 2
    max_pages = 50
    visited_links_counter = 0

    output_dir = os.path.curdir
    output_file = "all_documents.pkl"

    def start_requests(self):
        urls = ['https://www.iit.edu']  # replace with the URL you want to start crawling
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 1, 'visited_links': set(), 'documents': []})

    def parse(self, response):
        depth = response.meta.get('depth')
        visited_links = response.meta['visited_links']
        documents = response.meta['documents']

        #if not os.path.exists(self.output_dir):
        #    os.makedirs(self.output_dir)

        # Extract text from the page
        cleaned_text = re.sub(r'[\n\t]+', ' ', ''.join(response.xpath("//body//text()").extract()).strip())
        documents.append(response.url + "\n"+cleaned_text)

        # Extracting all the links from the page
        link_extractor = LinkExtractor()
        links = link_extractor.extract_links(response)

        print(f"Links on page {response.url}: {len(links)}")
        print(f"Depth: {depth}")

        for link in links:
            absolute_url = link.url.split('#')[0]
            if absolute_url not in visited_links:
                if self.max_depth > depth and self.visited_links_counter < self.max_pages:
                    visited_links.add(absolute_url)
                    self.visited_links_counter += 1
                    yield scrapy.Request(url=link.url, callback=self.parse, meta={'depth': depth+1, 'visited_links': visited_links, 'documents': documents})
                else:
                    # Save all documents to file
                    with open(os.path.join(self.output_dir, self.output_file), 'wb') as f:
                        pickle.dump(documents, f)
                    return
