import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from flask import render_template
from urllib import parse

def linkRequester(url):
    req = requests.get(url, headers = randomAgent())
    if req.status_code not in range(200, 299):
        # try again one more time
        req = requests.get(url, headers = randomAgent())
    # print(req.status_code, url)
    return BeautifulSoup(req.text, "html.parser")

def randomAgent():
    ua = UserAgent()
    header = {'User-Agent': str(ua.random)}
    return header

def resultsToHTML(resultsDict):
    outputHTML = "<div class='content'>"
    for r in resultsDict:
        buildHTML = render_template(
            "singleResult.html", title=r['title'], link=r['link'], source=r["source"], summary=r["summary"])
        outputHTML += buildHTML
    return outputHTML + "</div>"

def imgResultsToHTML(resultsDict):
    outputHTML = ""
    for r in resultsDict:
        outputHTML += render_template('imageResults.html', link = r['link'], source = r["source"])
    return outputHTML

def relevancyByOccurances(listOfResults):
    rankings = {}
    for result in listOfResults:
        if rankings.get(result.get('title')):
            rankings[result.get('title')] += 1
        else:
            rankings[result.get('title')] = 1
    rankedList = []
    while len(rankings) > 0:
        max = [0, '']
        for title in rankings.keys():
            if rankings[title] > max[0]:
                max[0] = rankings[title]
                max[1] = title
        for result in listOfResults:
            if result.get("title") == max[1]:
                rankedList.append(result)
                rankings.pop(result.get("title"))
                break
    return rankedList
    