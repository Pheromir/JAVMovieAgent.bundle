from lxml import etree
import datetime
import json
from wordfilter import censored_words
import javmovie

BASEURL="https://www.r18.com/api/v4f/contents/[id]?lang=en&unit=USD"
SEARCH_URL = "https://www.r18.com/common/search/searchword="
xpath_searchresults = "/html/body/div[6]/div/div[2]/section/ul[2]"
RESULT_LIMIT = 10


def get_by_content_id(content_id):
    try:
        json_response = JSON.ObjectFromURL(
        BASEURL.replace("[id]", content_id),
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
        }
    )
    except Exception as e:
        return None
    if json_response["status"] != "OK":
        return None
    args = {}
    args["content_id"] = content_id
    args["jav_code"] = json_response["data"]["dvd_id"]
    title = json_response["data"]["title"].lower()
    for word, replacement in censored_words.items():
        title = title.replace(word.lower(), replacement)
    args["title"] = title.title().strip()
    tags = []
    for tag in json_response["data"]["categories"]:
        tagtemp = tag["name"]
        to_remove = ["Featured Actress", "Hi-Def", "2021 Winter Sale", "Sale (limited time)", "Digital Mosaic", "AV OPEN 2017 Y********l Category"]
        if tagtemp in to_remove:
            continue
        for word, replacement in censored_words.items():
            tagtemp = tagtemp.lower().replace(word.lower(), replacement)
        tags.append(tagtemp.title())
    args["tags"] = tags
    if json_response["data"]["maker"] is not None and json_response["data"]["maker"]["name"] is not None:
        args["studio_label"] = json_response["data"]["maker"]["name"]
    else:
        args["studio_label"] = None
    date = json_response["data"]["release_date"]
    if date is None:
        args["release_date"] = None
    else:
        args["release_date"] = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    args["image_url"] = json_response["data"]["images"]["jacket_image"]["large"]

    return javmovie.JAVMovie(args)


def __str__(self):
    print("<R18Movie " + self.jav_code + ">")


def get_search_results(keyword):
    try:
        html = HTTP.Request(SEARCH_URL + keyword).content
    except Exception as e:
        raise e
    tree = etree.HTML(html)
    result_elements = tree.xpath(xpath_searchresults)
    if len(result_elements) == 0:
        return []
    result_urls = result_elements[0]
    if len(result_urls) == 0:
        return []
    results_checked = 0
    results = []
    for result in result_urls:
        mov_result = get_by_content_id(result[0].attrib["href"].split("id=")[1].replace("/", ""))
        results.append(mov_result)
        results_checked += 1
        if results_checked >= RESULT_LIMIT:
            break
    return results
