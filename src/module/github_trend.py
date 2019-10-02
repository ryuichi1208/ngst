#!/usr/local/bin/python3
# coding: utf-8

from bs4 import BeautifulSoup
import os
import pprint
import requests
import sys

BASE_URL = "https://github.com"
URL =BASE_URL + "/trending"

def send_to_slack(trends: list) -> int:
    pass

def run():
    r = requests.get(URL).text
    soup = BeautifulSoup(r, "html.parser")
    trends = soup.find_all("h1", attrs={"class", "h3 lh-condensed"})
    descript = soup.find_all("p", attrs={"class", "col-9 text-gray my-1 pr-4"})

    for i, trend in enumerate(trends):
        if i == 12:
            break
        repos = trend.a.get("href")
        desc = f"{descript[i].get_text()}"

        print(f"[{i+1}] {repos[1:]} : {BASE_URL + repos}")
        print(f"```\n {desc.strip()} \n```")

if __name__ == "__main__":
    run()

