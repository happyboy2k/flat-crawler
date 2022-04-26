#!/usr/bin/python3

import urllib.request as ur
import lxml.html as html
import datetime as dtd
import csv
import time
import random


url = 'https://www.immonet.de/nordrhein-westfalen/duisburg-wohnung-mieten.html'
csvFileName = "/home/pi/test.csv"

def http_get_content(url):
    req = ur.Request(url,
                     data = None,
                     headers = {
                         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
	             })
    content = ur.urlopen(req).read().decode('utf-8')
    return content

def get_address(htmlAddress):
    street = htmlAddress[0].strip().replace("\n", '').replace("\t", '')
    city = htmlAddress[1].strip().replace("\n", '').replace("\t", '')
    print(street)
    print(city)
    return (street, city)


def get_offer_link(offer):
    return 'https://www.immonet.de/'+offer

def check_for_link_occurance(link):
    try:
        fd = open(csvFileName, "r")
    except(FileNotFoundError):
        return False
    reader = csv.reader(fd)
    while True:
        try:
            fields = next(reader)
        except(StopIteration):
            return False
        if link == fields[-1]:
            return True



def write_offer_csv(offer):
    if check_for_link_occurance(offer):
        return
    url = get_offer_link(offer)
    content = http_get_content(url)
    tree = html.fromstring(content)
    date = dtd.date.today()
    street, city = get_address(tree.xpath('//p[@class="text-100 pull-left"]/text()'))
    try:
        title = tree.xpath('//title/text()')[0].strip()
    except(IndexError):
        title = "N/A"
    try:
        rooms = tree.xpath('//div[@id="equipmentid_1"]/text()')[0].strip()
    except(IndexError):
        rooms = "N/A"
    try:
        space = tree.xpath('//div[@id="areaid_1"]/text()')[0].strip()
    except(IndexError):
        space = "N/A"
    try:
        contactName = tree.xpath('//p[@id="bdContactName"]/text()')[0].strip()
    except(IndexError):
        contactName = "N/A"
    try:
        contactStreet = tree.xpath('//p[@id="bdContactStreet"]/text()')[0].strip()
    except(IndexError):
        contactStreet = "N/A"
    try:
        contactZipCity = tree.xpath('//p[@id="bdContactZipCity"]/text()')[0].strip()
    except(IndexError):
        contactZipCity = "N/A"
    try:
        contactPhone = tree.xpath('//p[@id="bdContactPhone"]/text()')[0].strip().replace('\t', '').replace('\n', '').replace('"', '')
    except(IndexError):
        contactPhone = "N/A"
    try:
        brokerFirmname = tree.xpath('//span[@id="bdBrokerFirmname"]/text()')[0].strip()
    except(IndexError):
        brokerFirmname = "N/A"
    try:
        brokerName = tree.xpath('//p[@id="bdBrokerNam"]/text()')[0].strip()
    except(IndexError):
        brokerName = "N/A"
    try:
        brokerStreet = tree.xpath('//p[@id="bdBrokerStreet"]/text()')[0].strip()
    except(IndexError):
        brokerStreet = "N/A"
    try:
        brokerZipCity = tree.xpath('//p[@id="bdBrokerZipCity"]/text()')[0].strip()
    except(IndexError):
        brokerZipCity = "N/A"
    try:
        brokerPhone = tree.xpath('//p[@id="bdBrokerPhone"]/text()')[0].strip().replace('\t', '').replace('\n', '').replace('"', '')
    except(IndexError):
        brokerPhone = "N/A"
    try:
        price = tree.xpath('//div[@id="priceid_2"]/text()')[0].strip()
    except(IndexError):
        price = "N/A"
    try:
        incidentals = tree.xpath('//div[@id="priceid_20"]/text()')[0].strip()
    except(IndexError):
        incidentals = "N/A"
    link = offer
    try:
        fd = open(csvFileName, "r")
        fd.close()
    except(FileNotFoundError):
        fd = open(csvFileName, "w+")
        fd.write("date,street,city,rooms,space,contactName,contactStreet,contactZipCity,contactPhone,brokerFirmname,brokerName,brokerStreet,brokerZipCity,brokerPhone,price,incidentals,link\n")
        fd.close()
    print (title)
    csvLine = [date, street, city, rooms, space, contactName, contactStreet, contactZipCity, contactPhone,\
               brokerFirmname, brokerName, brokerStreet, brokerZipCity, brokerPhone, price, incidentals, title, link]
    with open(csvFileName, "a+") as csvFd:
        csvWriter = csv.writer(csvFd)
        csvWriter.writerow(csvLine)
    time.sleep(random.randint(1, 10))



    
content = http_get_content(url)
tree = html.fromstring(content)
links = tree.xpath('//div[@class="flex-grow-1 overflow-hidden box-25"]/a/@href')

while True:
    nextPage = tree.xpath('//a[@class="col-sm-3 col-xs-1 pull-right text-right"]/@href')

    for l in links:
        print(l)
        write_offer_csv(l)

    try:
        nextPage = nextPage[0]
    except(IndexError):
        quit()
    nextPage = get_offer_link(nextPage)
    content = http_get_content(nextPage)
    tree = html.fromstring(content)
    links = tree.xpath('//div[@class="flex-grow-1 overflow-hidden box-25"]/a/@href')


