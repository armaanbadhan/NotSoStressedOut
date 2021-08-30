import requests


URLS = {
    "codechef": "https://kontests.net/api/v1/code_chef",
    "codeforces": "https://kontests.net/api/v1/codeforces",
    "kickstart": "https://kontests.net/api/v1/kick_start"
}


def get_contests(online_judge: str) -> list:
    """
    fetches the contests of the given online judge and returns a list of upcoming contests
    [oj, name, url, start_time, duration]
    """
    res = []
    response = requests.get(URLS[online_judge])
    for contest in response.json():
        if contest["status"] == "BEFORE":
            res.append([online_judge, contest["name"], contest["url"], contest["start_time"], contest["duration"]])
    return res


def in_24_hours() -> list:
    """
    fetches the contests which start in next 24 hours
    [oj, name, url, start_time, duration]
    """
    res = []
    response = requests.get("https://kontests.net/api/v1/all")
    for contest in response.json():
        if contest["in_24_hours"] == "Yes":
            res.append([contest["site"], contest["name"], contest["url"], contest["start_time"], contest["duration"]])
    return res
