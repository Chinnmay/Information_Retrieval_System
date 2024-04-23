import pytest
from crawler import IRSSpider
import os

# Test case for IRSSpider class
class TestIRSSpider:

    
    # Test case to check if IRSSpider can be initialized with default parameters
    def test_init_default_parameters(self):
        spider = IRSSpider()
        assert spider.max_depth == 4
        assert spider.max_pages == 1000
        assert spider.visited_links_counter == 0

    # Test case to check if IRSSpider can be initialized with custom parameters
    def test_init_custom_parameters(self):
        start_url = "https://www.iit.edu/"
        max_depth = 2
        max_pages = 50
        spider = IRSSpider(start_url=start_url, max_depth=max_depth, max_pages=max_pages)
        assert spider.start_urls == [start_url]
        assert spider.max_depth == max_depth
        assert spider.max_pages == max_pages
        assert spider.visited_links_counter == 0

    # Test case to check if extract_domain method extracts the domain correctly
    def test_extract_domain(self):
        spider = IRSSpider()
        url = "https://www.iit.edu/"
        assert spider.extract_domain(url) == "iit.edu"

