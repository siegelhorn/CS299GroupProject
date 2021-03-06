from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from os import path
from wordcloud import WordCloud
import re
import string
import numpy as np
from PIL import Image


pronouns = ['I', 'me', 'we', 'us', 'you',
            'she', 'he', 'her', 'him', 'it', 'they', 'them',
            'this', 'that', 'those', 'these']

def concatStrings(strings):
    result = ""
    for strng in strings:
        result += " " + strng
    return result

def filterString(strng, filterList):
    result = ""
    for word in strng.split():
        keep = True
        for filt in filterList:
            if word.lower() == filt.lower():
                keep = False
                break
        if keep:
            result += " " + word
    return result

regex = re.compile('[%s]' % re.escape(string.punctuation))
def removePunctuation(strng):
    return regex.sub('', strng)

def openPage(url):
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def getComments(soup):
    usertexts = soup.find_all("div", class_="usertext-body")
    divs = list(map(lambda x: x.find( class_="md"), usertexts))

    listOfPs = []
    for md in divs:
        oneCommentPs = md.find_all('p')
        for p in oneCommentPs:
            listOfPs.append(p.getText())

    listOfComments = listOfPs[32:]
    return listOfComments

def driver():

    url = input('copy/pasta reddit url:')


    testURL = "https://www.reddit.com/r/worldnews/comments/459bpr/gravitational_waves_from_black_holes_detected/?limit=500"


    url += '?limit=500'
    
    soup = openPage(url)

    print('Beginning to work. Please ignore the warning that pops up')

    comments = getComments(soup)
    text = removePunctuation(concatStrings(comments))

    maskIMG = np.array(Image.open('reddit-mask.png'))
    wordcloud = WordCloud(background_color='white', mask=maskIMG).generate(text)
    
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud)
    plt.axis("off")

    
    plt.show()
    return 'done'

print(driver())
















