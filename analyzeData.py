import re  # use regex to make sure that certain format guidelines are followed

import bs4
from bs4 import BeautifulSoup

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
        else:
            print("Problem found when splitting fileName -> check name structure YYYY-MM-DD-TITLE.md: ", noticeObj.title)

def checkTypeOfNotice(noticeObj):
    fileName = noticeObj.title
    if any(requiredKeyword in fileName.lower() for requiredKeyword in ("counternotice", "counter-notice")):
        noticeObj.notice = False
    else:
        noticeObj.notice = True

def getURLs(noticeObj):
    #TODO implement regex expression to get only the repository link no direct links
    url_list = noticeObj.content.find_all("a", href=True)
    github_list = []
    copyright_list = []

    # print(url_list)
    for url in url_list:
        # if any(github_keyword in url.text for github_keyword in ("github.com", "https://gist.github.com")):
        if any(github_keyword in url.text for github_keyword in ("github.com", "githubusercontent.com")):
            if "help.github.com" not in url.text:
                if url.text not in github_list:    # Eliminate duplicates (however, this can be done faster)
                    github_list.append(url.text)
        else:
            if url.text not in copyright_list:    # Eliminate duplicates (however, this can be done faster)
                copyright_list.append(url.text)
    if len(github_list) != 0:
        noticeObj.github_url = github_list
    if len(copyright_list) != 0:
        noticeObj.copyright_url = copyright_list


