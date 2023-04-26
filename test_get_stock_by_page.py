import pytest
from spider import crawl_stock_list_by_page

def test_write_page_count():
    result=crawl_stock_list_by_page("usamzn",6,"usamzn")
    print("result:",result)

if __name__ == "__main__":
    pytest.main(["-s", __file__])