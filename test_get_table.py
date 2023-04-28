import pytest
from spider import get_table

@pytest.mark.parametrize("stock,max_page",
    [
    # ("uspdd",None),# page_count: 263 count: 20966
    # ("ustlsa",None),# page_count: 5 count: 355
    # ("usmeta",None),# page_count: 49 count: 3897
    # ("ussnap",None),# page_count: 12 count: 906
    # ("usgoog",None),# page_count: 51 count: 4034
    # ("usvnet",None),# page_count: 7 count: 514
    # ("uswb",None),# page_count: 38 count: 3023
    # ("usrenn",None),# page_count: 8 count: 635
    # ("usmsft",None),# page_count: 93 count: 7389
    # ("usaapl",None),# page_count: 443 count: 35436
    # ("usnflx",None),# page_count: 53 count: 4214
    # ("usamzn",None),# X
    ("usntes",None),# page_count: 120 count: 9593 90962
    ("usnio",None),# page_count: 120 count: 9593 90962
    ("usxpev",None),# page_count: 120 count: 9593 90962
    ("usmf",None),# page_count: 120 count: 9593 90962
    ("ustuya",None),# page_count: 120 count: 9593 90962
    ("ustme",None),# page_count: 120 count: 9593 90962
    
    ]
)
def test_get_table(stock,max_page):
    path=get_table(stock,max_page=max_page)
    print("path:",path)

if __name__ == "__main__":
    pytest.main(["-s", __file__])