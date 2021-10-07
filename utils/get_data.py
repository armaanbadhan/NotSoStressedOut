import requests
from datetime import datetime


URLS = {
    "codechef": "https://kontests.net/api/v1/code_chef",
    "codeforces": "https://kontests.net/api/v1/codeforces",
    "kickstart": "https://kontests.net/api/v1/kick_start",
    "topcoder": "https://kontests.net/api/v1/top_coder",
    "atcoder": "https://kontests.net/api/v1/at_coder",
    "hackerrank": "https://kontests.net/api/v1/hacker_rank",
    "hackerearth": "https://kontests.net/api/v1/hacker_earth",
    "leetcode": "https://kontests.net/api/v1/leet_code"
}


def get_contests(online_judge: str) -> (list, list):
    """
    fetches the contests of the given online judge and returns a (list, list) of (running, upcoming) contests
    [oj, name, url, start_time, duration]
    """
    running, upcoming = [], []
    response = requests.get(URLS[online_judge])
    for contest in response.json():
        if contest["status"] == "BEFORE":
            if datetime.strptime(contest["start_time"][:-5], '%Y-%m-%dT%H:%M:%S') > datetime.now():
                upcoming.append(
                    [online_judge, contest["name"], contest["url"], contest["start_time"], contest["duration"]]
                )
        else:
            if datetime.strptime(contest["end_time"][:-5], '%Y-%m-%dT%H:%M:%S') > datetime.now():
                running.append(
                    [online_judge, contest["name"], contest["url"], contest["end_time"], -1]
                )
    return running, upcoming


def in_24_hours() -> list:
    """
    fetches the contests which start in next 24 hours
    [oj, name, url, start_time, duration]
    """
    res = []
    response = requests.get("https://kontests.net/api/v1/all")
    for contest in response.json():
        if contest["in_24_hours"] == "Yes":
            if datetime.strptime(contest["start_time"][:-5], '%Y-%m-%dT%H:%M:%S') > datetime.now():
                res.append(
                    [contest["site"], contest["name"], contest["url"], contest["start_time"], contest["duration"]]
                )
    return res
