#!/usr/bin/env python3
# coding=utf-8


import os
import sys
import datetime
import shutil

def main():
  for str in sys.argv[1:]:
    process(str)


def process(path):
  if os.name == 'nt':
    SHELL = "powershell.exe"
    PYTHON = "py -3"
  else:
    SHELL = "/bin/bash"
    PYTHON = "python3.6"

  with open(path + "/main.md", mode='r', encoding="utf8") as md_file:
    title = md_file.readline().rstrip()
    head = md_file.readline().rstrip()
    content = md_file.read()
    title = "_".join(title.title().split(" "))

    img_path = "./assets/img/img.auto/{0}".format(title)
    if not os.path.exists(img_path):
      os.mkdir(img_path)
    if os.name == 'nt':
     os.system(SHELL + ' -c ' + "mv {0}/*.jpg {1}".format(path, img_path))
     os.system(SHELL + ' -c ' + "mv {0}/*.png {1}".format(path, img_path))
    else:
     print("mv {2}/{0}/*.jpg {2}/{1}/".format(path, img_path, os.getcwd()))
     os.system(SHELL + ' -c ' + "mv {2}/{0}/*.jpg {2}/{1}/".format(path, img_path, os.getcwd()))
     os.system(SHELL + ' -c ' + "mv {2}/{0}/*.png {2}/{1}/".format(path, img_path, os.getcwd()))
      
    os.system(PYTHON + " ./tinypng.py -r {0}".format(img_path))

    imgs = [f for f in os.listdir(img_path)]
    article = """---
layout: post
title:  "{0}"
date:   "{1}"
thumbnail: "{2}"
---
""".format(head, datetime.datetime.now().strftime("%Y/%m/%d"), "/img.auto/{0}/{1}".format(title, imgs[0]))
    article += (content + "\n\n")
    article += "\n".join(map(
        lambda img: "![]({{site.baseurl}}"+"/{0}/{1})".format(img_path[2:], img), imgs[1:]))

    with open("_posts/{0}-{1}.md".format(datetime.datetime.now().strftime("%Y-%m-%d"), title), "w", encoding="utf8") as md_out:
      md_out.write(article)
    
  shutil.rmtree(path) 

if __name__ == "__main__":
  main()
