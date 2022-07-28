#Use requests browse
from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup

# craw key words
search_term = "Example"
# Page nember you need
rows_page = 1
# How many loop you needs
page_loop_num = 1

for page_no in range(page_loop_num):
    # Use json with Content-Type
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://ieeexplore.ieee.org",
        "Content-Type": "application/json",
    }

    # which payload you need
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

    # Do post
    r = requests.post(
            "https://ieeexplore.ieee.org/rest/search",
            json=payload,
            headers=headers
        )

    # response with json
    page_data = r.json()
    # print(page_data["records"])
    num_count = page_no * rows_page

    for idx, record in enumerate(page_data["records"]):
        paper_url = 'https://ieeexplore.ieee.org'+record["documentLink"]
        resp = requests.get(paper_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        text_title = soup.find("meta", property="og:title")
        text_data = soup.find("meta", property="og:description")
        if text_data is not None:
            file_name = 'test'+ str(idx+num_count) + '.txt'
            f = open(file_name,'w', encoding='UTF-8')
            f.write(text_title["content"])
            f.write('\n')
            f.write(text_data["content"])
            f.close()
        else:
            continue
        
