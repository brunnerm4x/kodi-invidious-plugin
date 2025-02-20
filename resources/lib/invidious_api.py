import time
from collections import namedtuple

import requests
import xbmc
import xbmcaddon
import json

VideoListItem = namedtuple("VideoSearchResult",
    [
        "video_id",
        "title",
        "author",
        "description",
        "thumbnail_url",
        "view_count",
        "published",
        "type"
    ]
)
ChannelListItem = namedtuple("ChannelSearchResult",
    [
        "channel_id",
        "thumbnail_url",
        "name",
        "description",
        "verified",
        "sub_count",
        "type"
    ]
)


class InvidiousAPIClient:
    def __init__(self, instance_url):
        self.instance_url = instance_url.rstrip("/")
        self.addon = xbmcaddon.Addon()

    def make_get_request(self, *path, **params):
        base_url = self.instance_url + "/api/v1/"

        url_path = "/".join(path)

        while "//" in url_path:
            url_path = url_path.replace("//", "/")

        assembled_url = base_url + url_path

        xbmc.log("========== request started ==========", xbmc.LOGDEBUG)
        start = time.time()
        response = requests.get(assembled_url, params=params, timeout=5)
        end = time.time()
        xbmc.log("========== request finished in" + str(end - start) + "s ==========", xbmc.LOGDEBUG)

        response.raise_for_status()

        return response

    def parse_video_list_response(self, response):
        data = response.json()
        for video in data:
            if video["type"] == "video":
                for thumb in video["videoThumbnails"]:
                    # high appears to be ~480x360, which is a reasonable trade-off
                    # works well on 1080p
                    if thumb["quality"] == "high":
                        thumbnail_url = thumb["url"]
                        break

                # as a fallback, we just use the last one in the list (which is usually the lowest quality)
                else:
                    thumbnail_url = video["videoThumbnails"][-1]["url"]
            
                yield VideoListItem(
                    video["videoId"],
                    video["title"],
                    video["author"],
                    video.get("description", self.addon.getLocalizedString(30000)),
                    thumbnail_url,
                    video["viewCount"],
                    video["published"],
                )
            # elif video["type"] == "channel":

    def parse_response(self, response):
        data = response.json()
        
        # If a channel is opened, the videos are packaged in a dict entry "videos"
        if "videos" in data:
            data = data["videos"]

        for item in data:
            if item["type"] == "video":
                for thumb in item["videoThumbnails"]:
                    # high appears to be ~480x360, which is a reasonable trade-off
                    # works well on 1080p
                    if thumb["quality"] == "high":
                        thumbnail_url = thumb["url"]
                        break
                else:
                    thumbnail_url = item["videoThumbnails"][-1]["url"]

                yield VideoListItem(
                    item["videoId"],
                    item["title"],
                    item["author"],
                    item.get("description", self.addon.getLocalizedString(30000)),
                    thumbnail_url,
                    item["viewCount"],
                    item["published"],
                    "video"
                )

            elif item["type"] == "channel":
                # Grab the highest resolution avatar image
                # Usually isn't more than 512x512
                thumbnail = sorted(item["authorThumbnails"], key=lambda thumb: thumb["height"], reverse=True)[0]

                yield ChannelListItem(
                    item["authorId"],
                    "https:" + thumbnail["url"],
                    item["author"],
                    item["description"],
                    item["authorVerified"],
                    item["subCount"],
                    "channel"
                )

    def search(self, *terms):
        params = {
            "q": " ".join(terms),
            "sort_by": "upload_date",
        }

        response = self.make_get_request("search", **params)

        return self.parse_response(response)

    def fetch_video_information(self, video_id):
        response = self.make_get_request("videos/", video_id)

        data = response.json()

        return data

    def fetch_channel_list(self, channel_id):
        response = self.make_get_request("channels/videos/" + channel_id)

        return self.parse_response(response)

    def fetch_special_list(self, special_list_name):
        response = self.make_get_request(special_list_name)

        return self.parse_response(response)
