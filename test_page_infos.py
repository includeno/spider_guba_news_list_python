import pytest
from spider import get_page_info

@pytest.mark.parametrize("stock,max_page",
    [
    # ("uspdd",None),
    # ("ustlsa",None),
    # ("usmeta",None),
    # ("ussnap",None),
    # ("usgoog",None),
    # ("usvnet",None),
    # ("uswb",None),
    # ("usrenn",None),
    # ("usmsft",None),
    # ("usaapl",None),
    # ("usnflx",None),
    # ("usamzn",None),
    # ("usntes",None),
    # ("usnio",None),
    # ("usxpev",None),
    # ("usmf",None),
    # ("ustuya",None),
    # ("ustme",None),
    # ("usvips",None),
    # ("usbz",None),
    # ("ushuya",None),
    # ("usfutu",None),
    # ("usjd",None),
    # ("uscmcm",None),
    # ("usbaba",None),
    # ("usmomo",None),
    # ("uspins",None),
    # ("usmtch",None),
    # ("ustigr",None),
    # ("usnvda",None),
    # ("usjg",None),
    # ("usbzfd",None),
    # ("usms",None),
    # ("usgs",None),
    # ("ususb",None),
    ("usbac",None),
    ("usjpm",None),
    ]
)
def test_get_table(stock,max_page):
    path=get_page_info(stock)
    print("path:",path)

if __name__ == "__main__":
    pytest.main(["-s", __file__])