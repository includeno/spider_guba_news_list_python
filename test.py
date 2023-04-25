import pytest
from spider import get_list_url_by_page

# 股吧测试用例
@pytest.mark.parametrize("stock, page, expected", [
    ("usaapl", 2, "http://guba.eastmoney.com/list,usaapl_2.html"),
    ("usaapl", 1, "http://guba.eastmoney.com/list,usaapl.html"),
    ("usgoog", 2, "http://guba.eastmoney.com/list,usgoog_2.html"),
    ("usaapl", 3, "http://guba.eastmoney.com/list,usaapl_3.html"),
    ("usmsft", 1, "http://guba.eastmoney.com/list,usmsft.html"),
    ("usmsft", 2, "http://guba.eastmoney.com/list,usmsft_2.html"),
    ("usamzn", 1, "http://guba.eastmoney.com/list,usamzn.html"),
    ("usamzn", 3, "http://guba.eastmoney.com/list,usamzn_3.html"),
    ("usfb", 2, "http://guba.eastmoney.com/list,usfb_2.html"),
    ("usnflx", 1, "http://guba.eastmoney.com/list,usnflx.html"),
    ("usnflx", 2, "http://guba.eastmoney.com/list,usnflx_2.html"),
    ("usnflx", 3, "http://guba.eastmoney.com/list,usnflx_3.html"),
    ("usgoog", 1, "http://guba.eastmoney.com/list,usgoog.html"),
    ("usfb", 1, "http://guba.eastmoney.com/list,usfb.html"),
    ("usaapl", 4, "http://guba.eastmoney.com/list,usaapl_4.html"),
    ("usamzn", 2, "http://guba.eastmoney.com/list,usamzn_2.html"),
    ("usmsft", 3, "http://guba.eastmoney.com/list,usmsft_3.html"),
    ("usgoogl", 1, "http://guba.eastmoney.com/list,usgoogl.html"),
    ("usnke", 2, "http://guba.eastmoney.com/list,usnke_2.html"),
    ("usbrk", 1, "http://guba.eastmoney.com/list,usbrk.html"),
    ("usbaba", 2, "http://guba.eastmoney.com/list,usbaba_2.html"),
])
def test_get_list_url_by_page(stock, page, expected):
    result = get_list_url_by_page(stock, page)
    assert result == expected

if __name__ == "__main__":
    pytest.main(["-s", "test.py"])