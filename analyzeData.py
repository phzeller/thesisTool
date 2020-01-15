import re  # use regex to make sure that certain format guidelines are followed

import bs4
from bs4 import BeautifulSoup

from main import profile


def analyzeTitle(noticeObj):
    # Split fileName to get title, year, month and day
    fileNameSplitted = noticeObj.title.split("-", 3)
    # Check if format of splitted file name is correct
    if len(fileNameSplitted) < 4:
        print("Problem found when splitting fileName -> check name structure YYYY-MM-DD-TITLE.md: ", noticeObj.title)
        return -1
    elif len(fileNameSplitted) > 4:
        print("Problem found when splitting fileName -> check name structure YYYY-MM-DD-TITLE.md: ", noticeObj.title)
        return -1
    else:  # validate exact expressions
        if re.match("[2][0][0-9][0-9]", fileNameSplitted[0]) and re.match("[0-12]", fileNameSplitted[1]) and re.match(
                "[0-31]", fileNameSplitted[2]):
            noticeObj.year = fileNameSplitted[0]
            noticeObj.month = fileNameSplitted[1]
            noticeObj.day = fileNameSplitted[2]
            noticeObj.header = fileNameSplitted[3]
            noticeObj.description = fileNameSplitted[3].replace(".md", "").replace(".markdown", "")
        else:
            print("Problem found when splitting fileName -> check name structure YYYY-MM-DD-TITLE.md: ",
                  noticeObj.title)


def checkTypeOfNotice(noticeObj):
    fileName = noticeObj.title
    if any(requiredKeyword in fileName for requiredKeyword in ("counternotice", "counter-notice")):
        noticeObj.notice = "counternotice"
    elif any(requiredKeyword in fileName for requiredKeyword in ("retraction", "retractions")):
        noticeObj.notice = "retraction"
    elif any(requiredKeyword in fileName for requiredKeyword in ("reversal", "reversals")):
        noticeObj.notice = "reversal"
    else:
        noticeObj.notice = "notice"


def getURLs(noticeObj):
    # TODO Content removed by repository owner search or [User was notified and removed the repository] or [already removed by user]
    url_list = noticeObj.content.find_all("a", href=True)
    github_list = []
    other_list = []

    for url in url_list:
        if any(github_keyword in url.text.lower() for github_keyword in
               ("github.com", "githubusercontent.com", "github.io")):
            if all(github_keyword_2 not in url.text.lower() for github_keyword_2 in
                   ("help.github.com", "copyright@github.com")):
                if url.text.lower() not in github_list:  # Eliminate duplicates (however, this can be done faster)
                    # Filter out plain github profile URLs, github plain URL (github.com)
                    regex_profile_url = r"(?:http[s]?://(?:www\.)?github\.com/[\w]+[-]?[\w]*[\/]?$)"
                    regex_github_url_plain = r"(?:http[s]?://(?:www\.)?(?:gist\.)?github\.com[\/]?$)"
                    regex_total = r"" + regex_profile_url + "|" + regex_github_url_plain

                    result_of_search = re.search(regex_total, url.text, flags=re.IGNORECASE)
                    if result_of_search is None:
                        github_list.append(url.text.lower())
        else:
            if url.text not in other_list:  # Eliminate duplicates (however, this can be done faster)
                other_list.append(url.text)

    if len(github_list) != 0:
        noticeObj.github_url = github_list
    if len(other_list) != 0:
        noticeObj.other_url = other_list

    if len(github_list) == 0 and len(other_list) == 0:
        print("Did not find any URLs: ", noticeObj.filePath)

    # Problem: some notices do not include formatted URLs -> therefore, we can not rely on the HTML href tag
    # Attempt: if no single URL was found, it might be possible, that the format is not correct -> search manual


@profile
def getKeywords(noticeObj):
    with open(noticeObj.filePath) as file:
        content = file.read().lower()

        pattern_copyright_holder = r"are you the copyright owner or authorized to act on the copyright owner's behalf"
        keyword_list = re.findall(pattern_copyright_holder, content)
        if len(keyword_list) != 0:
            print("found something in:", noticeObj.title)

        # for keyword in keyword_list:
        #     test = None
