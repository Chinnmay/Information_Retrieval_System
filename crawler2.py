import scrapy 
from bs4 import BeautifulSoup
import os
import re
import uuid

from scrapy.linkextractors import LinkExtractor

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    '''start_urls = [
        #"https://en.wikipedia.org/wiki/Information_retrieval"
        "https://www.iit.edu"
    ]'''

    custom_settings = {
        "LOG_LEVEL": "INFO"
    }
    links_counter = 1
    max_depth = 2
    max_pages = 5
    visited_links_counter = 0

    output_dir = os.path.join(os.path.curdir, "Output")
    #print(output_dir)

    def start_requests(self):
        urls = ['https://www.iit.edu']  # replace with the URL you want to start crawling
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 1, 'visited_links': set()})


    def parse(self, response):
        # Create directory if it doesn't exist
        
        depth = response.meta.get('depth')
        visited_links = response.meta['visited_links']  

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # get all text from the html
        sel = scrapy.Selector(response)
        # Extracting all the links from the page
        link_extractor = LinkExtractor()
        links = link_extractor.extract_links(response)
        #self.links_counter += len(links)
        
        print(f"Links on page {response.url}: {len(links)}")
        print(f"Depth: {depth}")
        
        print(f"Visited links counter: {self.visited_links_counter}")
        for link in links:
            absolute_url = link.url.split('#')[0]
            if absolute_url not in visited_links:
                # print len of visited_links
                #absolute_url = response.urljoin(link)              
                # Visiting each fetched URL recursively
                if self.max_depth > depth and self.visited_links_counter < self.max_pages:                    
                    visited_links.add(absolute_url)
                    self.visited_links_counter += 1
                    self.links_counter += 1  
                    filename = f"{self.output_dir}/{str(uuid.uuid4())}.txt"
                    with open(filename, 'w') as f:
                        cleaned_text = re.sub(r'[\n\t]+', ' ', ''.join(sel.xpath("//body//text()").extract()).strip())
                        f.write(cleaned_text)
                    self.log(f'Saved file {filename}')  
                    print(f"Visiting link: {absolute_url}")        
                    yield scrapy.Request(url=link.url, callback=self.parse, meta={'depth': depth+1, 'visited_links': visited_links})
                else:
                    return
        #print(f"Visited links count: {len(visited_links)}")
        
