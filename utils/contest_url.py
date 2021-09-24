from googlesearch import search


def contest_url(contest_name: str) -> str:
    """returns the url of contest"""
    for i in search(contest_name, tld="com", num=1, stop=1):
        return i


if __name__ == "__main__":
    pass
