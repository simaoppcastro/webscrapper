# HTTP
import requests
# SCTP
# https://docs.python.org/3/library/email.examples.html
import smtplib
# https://pypi.org/project/beautifulsoup4/
from bs4 import BeautifulSoup
# for the header of the email message
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText

# from email.mime.multipart import MIMEMultipart
# from email.mime.multitext import MIMEText

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
# SMTP
# https://tools.ietf.org/html/rfc822.html

import csv
import numpy as np

def urlListInput(file_input):
    urlList = []
    with open(file_input, 'rt') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in file_reader:
            urlList.append(row)

    return urlList

# def parserPage(urlList, index_Input):
def parserPage(urlList):
    # this function recives a list with all of the URL
    # and return a string

    ListTag_words = []
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}

    for i in urlList:
        page = requests.get(i, headers=headers)

        pageParser = BeautifulSoup(page.content, 'html.parser')

        # TagWords = pageParser.find_all("title").get_text()
        # Tag_Words = pageParser.find(id="title").get_text().strip()
        Tag_Words = pageParser.find("title").get_text().strip()
        # Tag_Words = pageParser.find("title")

        print(Tag_Words)
        ListTag_words.append(Tag_Words)

    # return string contains title`s
    #return Tag_Words
    return ListTag_words

# for verify if exists what we want
def verifyPage(Tag_WordsList, word_Input):
    # this function verify if the pre determinated word_input exist`s in the page
    for i in Tag_WordsList:
        list = i.rsplit()
        for word in list:
            flag = False
            if (word == word_Input):
                flag = True
                break
            else:
                flag = False
            # debug
            print(flag)

    return flag

# SMTP protocol
def send_message(Tag_Words_Input, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # this password is generated with "google app passwords"
    from_mail = '@gmail.com'
    to_mail = '@gmail.com'
    password = ''
    server.login(from_mail, password)

    # message
    message = MIMEMultipart()
    message['From'] = from_mail
    message['To'] = to_mail
    message['Subject'] = 'Founded Tags: ' + str(url)
    body = 'Check the link: ' + str(url)
    # message = ("From: %s\r\nTo: %s\r\n\r\n"
    #       % (from_mail, to_mail))
    # message = message + subject + body
    message.attach(MIMEText(body, 'plain'))
    message = message.as_string()
    # https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.sendmail
    server.sendmail(from_mail, to_mail, message)
    # debug final message
    # print(message)
    print('Send Success!')

    # finnaly end server session
    server.quit()

# main
if __name__ == '__main__':

    # parserPage function
    urlList = urlListInput('urlList.csv')

    List1 = parserPage(urlList)
    # print(Tag_WordsList)

    # verify function
    # the string passed to the function need work
    # flag = verifyPage(Tag_WordsList, "que")
    # print(flag)

    #if flag:
        # email tests
        #(Tag_Words, urlList[3])

