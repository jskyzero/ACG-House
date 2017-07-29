"""yande.py
this is a python program that can auto download picture from yande.re
Thanks for yande website for such a lot great picture
"""

import os
import re
import urllib2

# set TAG in bellow, just copy url ...tags=? 's ?
# example: https://yande.re/post?tags=bike_shorts
# set:   TAG = "bike_shorts"
TAG = "little_witch_academia"


class Yande(object):
    """yande class"""

    def __init__(self, tag):
        """initial data"""
        self.tag = tag
        self.mkdir_and_chdir()
        if self.tag != "":
            self.tag = "&tags=" + self.tag
        self.yande_url = "https://yande.re/post?page="
        # some regex patton to searth key value
        self.regex_post = re.compile(
            r'(?<=<span class="plid">#pl )https://yande.re/post/show/\d+(?=</span>)')
        self.regex_show = re.compile(
            r'(?<=src\=")https://files.yande.re/\w+/\w+/yande\.re.+?\.\w+(?=")')
        self.regex_name = re.compile(r'(?<=/)\w{6,}')
        self.page, self.num = (1, 0)

    def mkdir_and_chdir(self):
        """Create Folder"""
        default_folder_name = "post"
        if self.tag != "":
            default_folder_name = self.tag
        if not os.path.exists(default_folder_name):
            os.mkdir(default_folder_name)
        os.chdir(default_folder_name)

    @classmethod
    def read_url_data(cls, url):
        """return the data can get from url"""
        request = urllib2.Request(url)
        request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; \
        Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/47.0.2526.106 Safari/537.36")
        response = urllib2.urlopen(request)
        return response.read()

    def show_url_to_file(self, show_url):
        """get picture from url and"""
        pic_url = re.findall(self.regex_show, self.read_url_data(show_url))[0]
        self.picture_to_file(self.read_url_data(pic_url), re.findall(
            self.regex_name, show_url)[0] + ".jpg")
        # print message
        print "page", self.page, "total num", self.num, "finished"
        self.num = self.num + 1

    @classmethod
    def picture_to_file(cls, data, name):
        """save picture to file"""
        pic_file = open(name, 'wb+')
        pic_file.write(data)
        pic_file.close()

    def post_url_to_file(self, post_url):
        """use post_url to save file"""
        data = self.read_url_data(post_url)
        show_url_list = re.findall(self.regex_post, data)
        for show_url in show_url_list:
            self.show_url_to_file(show_url)
        self.page = self.page + 1
        # end loop
        if len(show_url_list) == 0:
            self.page = 0

    def loop_seek_picture(self):
        """loop to find all picture"""
        while self.page:
            self.post_url_to_file(self.yande_url + str(self.page) + self.tag)


YANDE = Yande(TAG)
YANDE.loop_seek_picture()
