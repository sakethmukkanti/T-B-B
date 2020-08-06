import os
import re
from collections import deque
from sys import argv

import requests
from bs4 import BeautifulSoup

from colorama import init, Fore
init()

BLUE = '\033[34m'  # colorama foreground
RESET = '\033[39m'  # colorama foreground reset


def create_dir(dir_name_):
    if not os.path.exists(dir_name_):
        os.mkdir(dir_name_)


def load_tab(dir_name_, file_name_):
    with open(f"{dir_name_}/{file_name_}.txt") as f:
        return parse_html(f.read())


def write_tab(dir_name_, file_name_, content_):
    with open(f"{dir_name_}/{file_name_}.txt", "w") as f:
        f.write(content_)


def input_is_correct(value_):
    return "." in value_


def get_domain_name(url):
    return url[:url.rindex(".")]


def prepare_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    return url


def load_url_content(url):
    url = prepare_url(url)
    content_ = requests.get(url).text
    # UnicodeEncodeError: 'cp932' codec can't encode character https://qiita.com/butada/items/33db39ced989c2ebf644
    # for s in ["\xf1", "\u2014", "\xe2", "\x99"]:
    #     content_ = content_.replace(s, "")
    return content_


def go_back(history_):
    if len(history_) > 1:
        history_.pop()
        print(load_url_content(history_[-1]))
    return history_


def parse_html(html_):
    soup = BeautifulSoup(html_, 'html.parser')
    content = ""
    for tag in soup.find_all(["p", re.compile("^h"), "a", "ul", "li", "ol", "span"]):
        if tag.name == "a":
            content += BLUE + str(tag.string) + RESET
        else:
            content += str(tag.string)
    return content


dir_name = argv[1]

create_dir(dir_name)

value = input()
tabs = []
history = deque()

while value != "exit":
    if value in tabs:
        print(load_tab(dir_name, value))
    elif value == "back":
        history = go_back(history)
    elif not input_is_correct(value):
        print("Error: Incorrect URL")
    else:
        history.append(value)

        domain_name = get_domain_name(value)
        html = load_url_content(value)

        tabs.append(domain_name)
        parsed_content = parse_html(html)
        write_tab(dir_name, domain_name, parsed_content)
        print(parsed_content)
    value = input()
