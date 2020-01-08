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
            print("Problem found when splitting fileName -> check name structure YYYY-MM-DD-TITLE.md: ",
                  noticeObj.title)


def checkTypeOfNotice(noticeObj):
    fileName = noticeObj.title
    if any(requiredKeyword in fileName.lower() for requiredKeyword in ("counternotice", "counter-notice")):
        noticeObj.notice = "counternotice"
    elif any(requiredKeyword in fileName.lower() for requiredKeyword in ("retraction", "retractions")):
        noticeObj.notice = "retraction"
    elif any(requiredKeyword in fileName.lower() for requiredKeyword in ("reversal", "reversals")):
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
            if all(github_keyword_2 not in url.text.lower() for github_keyword_2 in ("help.github.com", "copyright@github.com")):
                if url.text not in github_list:  # Eliminate duplicates (however, this can be done faster)
                    # Filter out plain github profile URLs, github plain URL (github.com)
                    regex_profile_url = r"(?:http[s]?://(?:www\.)?github\.com/[\w]+[-]?[\w]*[\/]?$)"
                    regex_github_url_plain = r"(?:http[s]?://(?:www\.)?github\.com[\/]?$)"
                    regex_total = r""+regex_profile_url+"|"+regex_github_url_plain

                    result_of_search = re.search(regex_total, url.text, flags=re.IGNORECASE)
                    if result_of_search is None:
                        github_list.append(url.text)
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

    # if len(github_list) == 0 and len(other_list) == 0:
    # if len(github_list) == 0 and noticeObj.notice:
    # credits for regex: https://urlregex.com/
    #     raw_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', noticeObj.content.get_text())
    #     print("Liste in raw string gefunden bei: ", noticeObj.filePath)
    #     print(raw_list)
    #     for raw_url in raw_list:
    #         if any(github_raw_keyword in raw_url for github_raw_keyword in ("github.com", "githubusercontent.com")):
    #             if "help.github.com" not in raw_url:
    #                 if url.text not in github_list:    # Eliminate duplicates (however, this can be done faster)
    #                     print("Found correct URL")
    #                     github_list.append(raw_url)
    # if any(github_keyword in url.text for github_keyword in ("github.com", "githubusercontent.com")):
    #     if "help.github.com" not in url.text:
    #         if url.text not in github_list:  # Eliminate duplicates (however, this can be done faster)
    #             github_list.append(url.text)
    # else:
    #     if url.text not in other_list:  # Eliminate duplicates (however, this can be done faster)
    #         other_list.append(url.text)
    # print("Analysierte Liste: ", github_list)
