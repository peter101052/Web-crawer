#使用requests模組模擬試用者瀏覽網站
from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup

# 選擇要爬取的關鍵字內容
search_term = "Deep learning"
# 選擇要爬取的葉面顯示數量
rows_page = 10

for page_no in range(2):
    #設定用json的方式解析網頁
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://ieeexplore.ieee.org",
        "Content-Type": "application/json",
    }

    #設定要請求的項目有哪些
    payload = {
        "newsearch": True,
        "queryText": search_term,
        "highlight": True,
        "returnFacets": ["ALL"],
        "returnType": "SEARCH",
        "matchPubs": True,
        "rowsPerPage": rows_page,
        "pageNumber": page_no
    }

    #實際執行Post請求
    r = requests.post(
            "https://ieeexplore.ieee.org/rest/search",
            json=payload,
            headers=headers
        )

    #回傳指定的json內容
    page_data = r.json()
    # print(page_data["records"])
    num_count = page_no * rows_page

    #透過標記的records擷取json檔案內容
    #idx是counter，計算爬取的數量
    for idx, record in enumerate(page_data["records"]):
        # print(record["articleTitle"])
        # print('https://ieeexplore.ieee.org'+record["documentLink"], end="\n----\n")
        paper_url = 'https://ieeexplore.ieee.org'+record["documentLink"]
        resp = requests.get(paper_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        text_title = soup.find("meta", property="og:title")
        text_data = soup.find("meta", property="og:description")
        # print(text_data)
        if text_data is not None:
            file_name = 'test'+ str(idx+num_count) + '.txt'
            f = open(file_name,'w', encoding='UTF-8')
            f.write(text_title["content"])
            f.write('\n')
            f.write(text_data["content"])
            f.close()
        else:
            continue
        

