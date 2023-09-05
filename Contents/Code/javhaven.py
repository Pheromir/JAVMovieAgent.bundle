from wordfilter import censored_words
from lxml import etree
import datetime
import javmovie

BASEURL="https://javhaven.com/"
xpath_title = "/html/body/div/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/h2"
xpath_javcode = "/html/body/div/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]/p"
xpath_tags = "/html/body/div/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[5]/td[2]"
xpath_studiolabel = "/html/body/div/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[7]/td[2]/a"
xpath_releasedate = "/html/body/div/div[3]/div/div[1]/div/div[1]/div[2]/div[2]/div/table/tbody/tr[3]/td[2]/p"
xpath_image = "/html/body/div/div[2]/div[1]/div[2]/div/img"
releasedate_format = "%Y-%m-%d"


def get_by_jav_id(jav_id):
    try:
        html = HTTP.Request(BASEURL + jav_id).content
    except Exception as e:
        return None
    tree = etree.HTML(html)
    args = {}
    args["jav_code"] = tree.xpath(xpath_javcode)[0].text
    title = str(tree.xpath(xpath_title)[0].text).replace("[" + args["jav_code"] + "]", "").replace(args["jav_code"], "").lower()
    for word, replacement in censored_words.items():
        title = title.replace(word.lower(), replacement)
    args["title"] = title.title().strip()
    tags = []
    for a in tree.xpath(xpath_tags)[0]:
        tags.append(a.text.title())
    args["tags"] = tags
    args["studio_label"] = tree.xpath(xpath_studiolabel)[0].text
    date = tree.xpath(xpath_releasedate)[0].text
    if date is None:
        args["release_date"] = datetime.datetime(1900, 1, 1, 00, 00) # placeholder date
    else:
        args["release_date"] = datetime.datetime.strptime(date, releasedate_format)
    args["image_url"] = tree.xpath(xpath_image)[0].attrib["src"]

    return javmovie.JAVMovie(args)