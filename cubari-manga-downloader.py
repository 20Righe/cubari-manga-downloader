# Script Name: cubari-manga-downloader.py
# Created Date: 2021-10-11
# Description: A Python script to download manga from Cubari.

import requests
import os
from pathlib import Path
import argparse
import time

class CubariDowlonader:

    site_url = "https://cubari.moe{}"
    manga_url = "https://cubari.moe/read/api/gist/series/{}/"

    def list_chapter(self, url):

        manga_id = self.get_manga_id_by_url(url)

        resp = requests.get(self.manga_url.format(manga_id))
        data = resp.json()

        print("{}\nAuthor:{}\nArtist:{}".format(
            data["title"], data["author"], data["artist"]))

        for chapter_number, chapter in data["chapters"].items():
            volume_number = chapter["volume"]
            chapter_title = chapter["title"]

            for group_id, chapter_link in chapter["groups"].items():

                group_name = data["groups"][group_id]
                print("{} - V{}C{} - {} - [{}]".format(chapter_number,
                      volume_number, chapter_number, chapter_title, group_name))

    def download_chapters(self, url, chapters_list=[]):

        manga_id = self.get_manga_id_by_url(url)

        resp = requests.get(self.manga_url.format(manga_id))
        data = resp.json()

        # format title and groups
        title = "_".join(data["title"].split())
        groups = {}
        for k, v in data["groups"].items():
            v = "_".join(v.split())
            groups[k] = v

        # create folder manga
        Path(title).mkdir(parents=True, exist_ok=True)

        for chapter_number, chapter in data["chapters"].items():
            if (len(chapters_list) != 0 and
                    chapter_number not in chapters_list):
                continue

            volume_number = chapter["volume"]

            for group_id, chapter_link in chapter["groups"].items():

                # list of pages link
                if (type(chapter_link) is list):
                    d = self.get_data_from_list(chapter_link)
                # /proxy/api/imgur/chapter/wCvC1lw/
                else:
                    d = self.get_data_from_proxy(chapter_link)
                
                print("[START] download C{}".format(chapter_number))

                group_name = groups[group_id]

                # create folder chapter
                chapter_name_foleder = "{}_v{}_c{}_[{}]".format(
                    title, volume_number, chapter_number, group_name)
                print("folder: {}".format(chapter_name_foleder))

                Path(title, chapter_name_foleder).mkdir(
                    parents=True, exist_ok=True)

                for i in range(len(d)):
                    ext = os.path.splitext(d[i]["src"].replace("?_w.", ""))[-1]
                    pathfile = Path(title, chapter_name_foleder,
                                    "{}{}".format(i, ext))

                    # check file already downloaded
                    if (not pathfile.exists()):
                        print("Download page {}. Link: {}".format(
                            i, d[i]["src"]))
                        r_content = self.download_img(d[i]["src"])
                        pathfile.write_bytes(r_content)
                        time.sleep(1)
                    else:
                        print("Page {} already exist. Link:{}".format(
                            i, d[i]["src"]))

                print("[END] download C{}".format(chapter_number))
    
    def get_manga_id_by_url(self, url):
        try:
            url_split = url.split("/")
            manga_id = url_split[-1]
            if (url_split[-1] == ''):
                manga_id = url_split[-2]

            return manga_id
        except Exception as e:
            print("Missing or invalid link:", str(e))
            exit()

    def download_img(self, url):
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                print("Failed to download page {}. Status code: {}".format(url, r.status_code))
            else:
                return r.content
        except requests.exceptions.RequestException as e:
            print("Error downloading page {}: {}".format(url, str(e)))
    
    def get_data_from_proxy(self, chapter_link):
        r = requests.get(self.site_url.format(chapter_link))
        d = r.json()
        return d
    
    def get_data_from_list(self, chapter_list):
        d = [{"src": link} for link in chapter_list]
        return d


if __name__ == '__main__':

    # CubariDowlonader().list_chapter("https://cubari.moe/read/gist/JECbu/")
    # CubariDowlonader().download_chapters("https://cubari.moe/read/gist/JECbu/", ['1','4'])
    # CubariDowlonader().download_chapters("https://cubari.moe/read/gist/cmF3L2NoaWNrbi1ub29kbGUvU2VyaWVzLS9tYWluL0hhcmFwZWtvLmpzb24/", ['13'])
    # CubariDowlonader().download_chapters("https://cubari.moe/read/gist/JECbu/")

    parser = argparse.ArgumentParser(description='Cubari Manga Downloader.')

    parser.add_argument('link', type=str, nargs='?',
                        help='Manga page link')
    parser.add_argument('--chapters-list', '--C', dest='available_chapters',
                        action='store_true', help='List available chapters')
    parser.add_argument('--chapters', '-c',
                        dest='chapters',
                        nargs='+', default=[],
                        help='Chapters to download (if omitted, download all chapters)')

    args = parser.parse_args()

    if not args.link:
        parser.print_help()
        exit()

    if args.available_chapters:
        CubariDowlonader().list_chapter(args.link)
    else:
        CubariDowlonader().download_chapters(args.link, args.chapters)
