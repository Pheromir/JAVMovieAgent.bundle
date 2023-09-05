from wordfilter import censored_words
from lxml import etree
import datetime
import javmovie

BASEURL="https://www.javlibrary.com/en/vl_searchbyid.php?keyword="
DIRECTURL="https://www.javlibrary.com/en/?v="
xpath_title = "/html/body/div[3]/div[2]/div[1]/h3/a"
xpath_javcode = "/html/body/div[3]/div[2]/table/tr/td[2]/div/div[1]/table/tr/td[2]"
xpath_tags = "/html/body/div[3]/div[2]/table/tr/td[2]/div/div[8]/table/tr/td[2]"
xpath_tags_no_rating = "/html/body/div[3]/div[2]/table/tr/td[2]/div/div[7]/table/tr/td[2]"
xpath_actress = "/html/body/div[3]/div[2]/table/tr/td[2]/div/div[9]/table/tr/td[2]"
xpath_studiolabel = "/html/body/div[3]/div[2]/table/tr/td[2]/div/div[6]/table/tr/td[2]/span/a"
xpath_releasedate = "/html/body/div[3]/div[2]/table/tr/td[2]/div/div[2]/table/tr/td[2]"
xpath_image = "/html/body/div[3]/div[2]/table/tr/td[1]/div/img"
xpath_notfound = "/html/body/div[3]/div[2]/p/em"

xpath_multiple_found = "/html/body/div[3]/div[2]/div[1]"
xpath_multiple_list = "/html/body/div[3]/div[2]/div[2]/div"

releasedate_format = "%Y-%m-%d"


def get_by_jav_id(jav_id, BASEURL=BASEURL):
    try:
        html = HTTP.Request(BASEURL + jav_id).content
    except Exception as e:
        return None
    tree = etree.HTML(html)
    args = {}

    if len(tree.xpath(xpath_notfound)) > 0 and "Search returned no result." in tree.xpath(xpath_notfound)[0].text:
        return None
    
    if BASEURL != DIRECTURL and len(tree.xpath(xpath_multiple_found)) > 0 and tree.xpath(xpath_multiple_found)[0].text is not None:
        if "ID Search Result" in tree.xpath(xpath_multiple_found)[0].text:
            if len(tree.xpath(xpath_multiple_list)[0]) > 0:
                results = []
                for videolink in tree.xpath(xpath_multiple_list)[0]:
                    vid = get_by_jav_id(videolink[0].attrib["href"].replace("./?v=", ""), DIRECTURL)
                    results.append(vid[0])
                return results
            

    args["jav_code"] = tree.xpath(xpath_javcode)[0].text
    title = str(tree.xpath(xpath_title)[0].text).replace("[" + args["jav_code"] + "]", "").replace(args["jav_code"], "").lower()
    for word, replacement in censored_words.items():
        title = title.replace(word.lower(), replacement)
    args["title"] = title.title().strip()
    tags = []
    try:
        for a in tree.xpath(xpath_tags)[0]:
            tags.append(a[0].text.title())
    except AttributeError:
        for a in tree.xpath(xpath_tags_no_rating)[0]:
            tags.append(a[0].text.title())
    args["tags"] = tags
    if len(tree.xpath(xpath_studiolabel)) > 0:
        args["studio_label"] = tree.xpath(xpath_studiolabel)[0].text
    date = tree.xpath(xpath_releasedate)[0].text
    if date is None:
        args["release_date"] = datetime.datetime(1900, 1, 1, 00, 00) # placeholder date
    else:
        args["release_date"] = datetime.datetime.strptime(date, releasedate_format)
    args["image_url"] = ("https:" + tree.xpath(xpath_image)[0].attrib["src"]) if tree.xpath(xpath_image)[0].attrib["src"].startswith("//") else tree.xpath(xpath_image)[0].attrib["src"]


    return [javmovie.JAVMovie(args)]
