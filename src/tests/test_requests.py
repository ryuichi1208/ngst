import requests

URLS = [
    "https://github.com/ryuichi1208",
    "https://github.com/ryuichi1208?tab=repositories",
    "https://githuuaaaaaa.com/"
]

def test_requests_func():
    for url in URLS:
        try:
            resp = requests.get(url)
            assert resp.status_code == 200
            print(resp.url, " : ", resp.headers["Content-type"])
        except requests.exceptions.HTTPError as nf:
            print("Not Found : ", nf)
        except requests.exceptions.ConnectionError as ce:
            print("Connection Error : ")

test_requests_func()
