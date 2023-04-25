import pytest
from spider import get_list_url_by_page,write_html,parse_html_js_data
from selenium_driver import get_driver_by_system
from utils import write_json,write_json_data

def test_write_page_count():
    stock="usmsft"
    page=3
    url=get_list_url_by_page(stock,page)
    driver = get_driver_by_system()
    write_html(url,driver=driver)
    html=""
    # 读取文件
    with open('html.txt', 'r', encoding='utf-8') as f:
        html = f.read()
    js=parse_html_js_data(html)
    print("js:",js)
    print("count:",js["count"])
    print("bar_name:",js["bar_name"])
    assert js["bar_name"]=='微软'
    write_json_data(js,"page_count.json")
    

if __name__ == "__main__":
    pytest.main(["-s", __file__])