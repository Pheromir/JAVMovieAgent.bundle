from datetime import datetime
from difflib import SequenceMatcher
import io
import javhaven
import r18
import javland
import javlibrary
import imagesize


IMGPROXY_BASEURL = Prefs["ImgProxyBaseUrl"]
USE_IMGPROXY = Prefs["UseImgProxy"]
if IMGPROXY_BASEURL[-1] is not "/":
    IMGPROXY_BASEURL = IMGPROXY_BASEURL + "/"
IMGPROXY_OPTIONS = "resize:auto:0.47:0:0/crop:0.47:0:ea"
IMGPROXY_OPTIONS_SQUARE = "resize:fit/width:[W]/height:[H]/ex:1/bg:46:46:46"

def get_similarity(str1, str2):
    matcher = SequenceMatcher()
    matcher.set_seqs(str1, str2)
    pct = int(matcher.ratio() * 100)
    Log("Similarity between '" + str1 + "' and '" + str2 + "' = " + str(pct) + "%")
    return pct

def Start():
    HTTP.CacheTime = 60
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
    

class JAVMovieAgent(Agent.Movies):
    name, primary_provider, fallback_agent, contributes_to, languages, accepts_from = (
    'JAVMovie', True, False, None, [Locale.Language.English], ['com.plexapp.agents.localmedia'])

    def search(self, results, media, lang, manual=False):
        Log("".ljust(157, '-'))
        jav_id = media.name.replace(" ", "-").upper().strip()
        if "-" not in jav_id:
            index = 0
            for char in jav_id:
                if char.isnumeric():
                    break
                index += 1
            jav_id = jav_id[:index] + "-" + jav_id[index:]

        Log("Fetching infos for " + media.name + "('" + jav_id + "')")

        ######### R18.com ##########
        # results_found = r18.get_search_results(jav_id)
        # for vid in results_found:
        #     results.Append(MetadataSearchResult(
        #         id = "0" + vid.content_id,
        #         name = "[" + vid.jav_code + "] " + "[R18] " + vid.title,
        #         year = vid.release_date,
        #         lang = 'en',
        #         score = get_similarity(jav_id.lower(), vid.jav_code.lower())
        #     ))
        ############################

        ####### JavHaven.com #######
        vid = javhaven.get_by_jav_id(jav_id)
        if vid is not None:
            results.Append(MetadataSearchResult(
                id = "1" + vid.jav_code,
                name = "[" + vid.jav_code + "] " + "[JavHaven] " + vid.title,
                year = vid.release_date,
                lang = 'en',
                score = get_similarity(jav_id.lower(), vid.jav_code.lower())
            ))
        ############################

        ####### JavLand.com ########
        vid = javland.get_by_jav_id(jav_id)
        if vid is not None:
            results.Append(MetadataSearchResult(
                id = "2" + vid.jav_code,
                name = "[" + vid.jav_code + "] " + "[JavLand] " +vid.title,
                year = vid.release_date,
                lang = 'en',
                score = get_similarity(jav_id.lower(), vid.jav_code.lower())
            ))
        ############################

        ####### JavLibrary.com ########
        vid = javlibrary.get_by_jav_id(jav_id)
        if isinstance(vid, list):
            for vid in results_found:
                results.Append(MetadataSearchResult(
                    id = "3" + vid.content_id,
                    name = "[" + vid.jav_code + "] " + "[JavLib] " + vid.title,
                    year = vid.release_date,
                    lang = 'en',
                    score = get_similarity(jav_id.lower(), vid.jav_code.lower())
                ))
        elif vid is not None:
            results.Append(MetadataSearchResult(
                id = "3" + vid.jav_code,
                name = "[" + vid.jav_code + "] " + "[JavLib] " +vid.title,
                year = vid.release_date,
                lang = 'en',
                score = get_similarity(jav_id.lower(), vid.jav_code.lower())
            ))
        ############################

        results.Sort('score', descending=True)
        Log("Results for " + jav_id + ": " + str(results))


    def update(self, metadata, media, lang):
        Log("".ljust(157, '='))
        Log("update() - metadata.id: '%s', metadata.title: '%s'" % (metadata.id, metadata.title))


        if metadata.id[0] == "0":  # Metadata from r18.com
            Log(metadata.id + " Metadata from r18.com (" + metadata.id[1:] + ")")
            vid = r18.get_by_content_id(metadata.id[1:])

        elif metadata.id[0] == "1":  # Metadata from javhaven.com
            Log(metadata.id + " Metadata from javhaven.com (" + metadata.id[1:] + ")")
            vid = javhaven.get_by_jav_id(metadata.id[1:])

        elif metadata.id[0] == "2":  # Metadata from javland.com
            Log(metadata.id + " Metadata from jav.land (" + metadata.id[1:] + ")")
            vid = javland.get_by_jav_id(metadata.id[1:])
            
        elif metadata.id[0] == "3":  # Metadata from javland.com
            Log(metadata.id + " Metadata from javlibrary.com (" + metadata.id[1:] + ")")
            vid = javlibrary.get_by_jav_id(metadata.id[1:])
        else:
            Log("Cant match metadata.id " + metadata.id)
            return

        # Check if movie is uncensored (contains "[u]" or "[uncen")
        filename = media.items[0].parts[0].file.split("/")[-1].lower()
        if "[u]" in filename or "[uncen" in filename:
            metadata.title = "[" + vid.jav_code + "][U]" + vid.title
        else:
            metadata.title = "[" + vid.jav_code + "] " + vid.title
            
        if vid.studio_label is not None:
            metadata.studio = vid.studio_label
        if vid.tags is not None:
            metadata.genres = vid.tags
        if vid.jav_code is not None:
            metadata.original_title = vid.jav_code

        width, height = imagesize.get(io.BytesIO(HTTP.Request(vid.image_url, timeout=120).content))
        Log("COVER IMAGE SIZE: " + str(width) + ", " + str(height) + " (" + str(float(width) / float(height)) + ")")
        if (1.55 > (float(width) / float(height)) > 1.4) and USE_IMGPROXY:
            Log("Potentially full DVD Cover, cropping..")
            poster = HTTP.Request(IMGPROXY_BASEURL + IMGPROXY_OPTIONS + "/plain/" + vid.image_url, timeout=120, sleep=1.0).content
            url_suffix = "1"
        elif (width == height) and USE_IMGPROXY:
            Log("Square Image, resizing..")
            poster = HTTP.Request(IMGPROXY_BASEURL + IMGPROXY_OPTIONS_SQUARE.replace("[H]", str(int(height * 1.5))).replace("[W]", str(width)) + "/plain/" + vid.image_url, timeout=120, sleep=1.0).content
            url_suffix = "2"
        else:
            Log("Unknown Format or imgproxy disabled..")
            poster = HTTP.Request(vid.image_url, timeout=120, sleep=1.0).content
            url_suffix = "0"

        metadata.posters[vid.image_url + "?v=" + url_suffix] = Proxy.Media(poster)
        metadata.originally_available_at = vid.release_date
        Log('update() ended')
