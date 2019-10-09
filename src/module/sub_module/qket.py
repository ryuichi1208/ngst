import requests
import pprint

file_name = "tbd.txt"

with open(file_name) as f:
    qiita_access_token = f.read().strip()

headers = {"Authorization": "Bearer {}".format(qiita_access_token)}
