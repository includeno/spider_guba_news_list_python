import pytest
from spider import get_table

def test_get_table():
    path=get_table("usamzn",max_page=None)
    print("path:",path)

if __name__ == "__main__":
    pytest.main(["-s", __file__])