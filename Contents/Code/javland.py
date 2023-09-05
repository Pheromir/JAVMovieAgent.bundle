from wordfilter import censored_words
from lxml import etree
import datetime
import javmovie

BASEURL="https://jav.land/en/id_search.php?keys="
xpath_title = "/html/body/div/div/div[2]/div[1]/div[1]/div/strong/text()"
xpath_javcode = "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/table/tr[2]/td[2]"
xpath_tags = "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/table/tr[9]/td[2]"
xpath_studiolabel = "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/table/tr[8]/td[2]/span/a"
xpath_releasedate = "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/table/tr[3]/td[2]"
xpath_image = "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[1]/img"
xpath_notfound = "/html/body/div/div/div[2]/div[1]/div[2]/div"
xpath_content_id = "/html/body/div[1]/div/div[2]/div[1]/div[2]/div[2]/table/tr[1]/td[2]"
releasedate_format = "%Y-%m-%d"


def get_by_jav_id(jav_id):
    try:
        html = HTTP.Request(BASEURL + jav_id).content
    except Exception as e:
        return None
    tree = etree.HTML(html)
    args = {}
    if "Not Found" in tree.xpath(xpath_notfound)[0].text:
        return None
    args["jav_code"] = tree.xpath(xpath_javcode)[0].text
    title = str(tree.xpath(xpath_title)[0]).replace("[" + args["jav_code"] + "]", "").replace(args["jav_code"], "").lower()
    for word, replacement in censored_words.items():
        title = title.replace(word.lower(), replacement)
    args["title"] = title.title().strip()
    tags = []
    for a in tree.xpath(xpath_tags)[0]:
        tags.append(a[0].text.title())
    args["tags"] = tags
    if len(tree.xpath(xpath_studiolabel)) > 0:
        args["studio_label"] = tree.xpath(xpath_studiolabel)[0].text
    date = tree.xpath(xpath_releasedate)[0].text
    if date is None:
        args["release_date"] = datetime.datetime(1900, 1, 1, 00, 00) # placeholder date
    else:
        args["release_date"] = datetime.datetime.strptime(date, releasedate_format)
    args["image_url"] = tree.xpath(xpath_image)[0].attrib["src"]

    return javmovie.JAVMovie(args)
