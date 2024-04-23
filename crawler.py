import scrapy 
import os
import re
import pickle
from scrapy.linkextractors import LinkExtractor

class IRSSpider(scrapy.Spider):
    name = "InformationRetrievalSystemSpider"
    custom_settings = {
        "LOG_LEVEL": "INFO"
    }
    max_depth = 2
    max_pages = 50
    visited_links_counter = 0

    output_dir = os.path.curdir
    output_file = "all_documents.pkl"

    #scrapy crawl crawler.py -a start_url=https://www.iit.edu max_depth=3 -a max_pages=500

    def extract_domain(self, url):
        """
        Extracts the domain name from the given URL.
        """
        if not url:
            return None
        return re.findall(r'https?://(?:www\.)?(.*?)/', url)[0]

    def __init__(self, start_url=None, max_depth=4, max_pages=1000, *args, **kwargs):
        super(IRSSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []
        self.allowed_domains = [self.extract_domain(start_url)]
        self.max_depth = int(max_depth)
        self.max_pages = int(max_pages)
        self.visited_links_counter = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 1, 'visited_links': set(), 'documents': []})

    """def start_requests(self):    
        urls = ['https://www.iit.edu']  # replace with the URL you want to start crawling
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 1, 'visited_links': set(), 'documents': []})
    """

    def parse(self, response):
        depth = response.meta.get('depth')
        visited_links = response.meta['visited_links']
        documents = response.meta['documents']

        # Extract text from the page
        cleaned_text = re.sub(r'[\n\t]+', ' ', ''.join(response.xpath("//body//text()").extract()).strip())
        documents.append(response.url + "\n"+cleaned_text)

        # Extracting all the links from the page
        link_extractor = LinkExtractor()
        links = link_extractor.extract_links(response)

        # print(f"Links on page {response.url}: {len(links)}")
        # print(f"Depth: {depth}")

        for link in links:
            absolute_url = link.url.split('#')[0]
            if absolute_url not in visited_links:
                if self.max_depth >= depth and self.visited_links_counter <= self.max_pages:
                    visited_links.add(absolute_url)
                    self.visited_links_counter += 1
                    yield scrapy.Request(url=link.url, callback=self.parse, meta={'depth': depth+1, 'visited_links': visited_links, 'documents': documents})
                else:
                    # Save all documents to file
                    with open(os.path.join(self.output_dir, self.output_file), 'wb') as f:
                        pickle.dump(documents, f)
                    return
