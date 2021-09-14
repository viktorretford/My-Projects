import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import csv
from random import randint
from time import sleep
import requests

def checkNone(var):
    return var[0] if var is not None else ""

def checkNone_2(var):
    return var[1] if var is not None else ""

#url = input('Enter Url: ')

csv_file = open('project.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Days', 'Price_hr', 'Price_range_Min', 'Price_range_Max', 'Price', 'Bid', 'Rating', 'Country'])

number_pages = int(input('How many pages:' ))
page = 0
count = 0
for i in range(0, number_pages):
    page = page + i
    url = 'https://www.freelancer.com/jobs/python/'
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    url = url + str(page)
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    job_cards = soup.findAll('div', {'class': 'JobSearchCard-item-inner'})

    for job in job_cards:
        price_raw = None
        pp_range = None
        pp_hr = None
        pp_normal = None

        title = job.find('a', attrs={'class': 'JobSearchCard-primary-heading-link'})
        title = title.text.strip().replace('\n', '')
        days = job.find('span', attrs={'class': 'JobSearchCard-primary-heading-days'})
        days = days.text.strip().replace('\n', '')
        try:
            price_raw = job.find('div', attrs={'class': 'JobSearchCard-primary-price'}).text.strip()
            if price_raw is not None and '/ hr' in price_raw:
                pp_hr = re.findall(r'\S\d+',price_raw)
            elif '-' in price_raw:
                pp_range = re.findall(r'\S\d+',price_raw)
            else:
                pp_normal = re.findall(r'\S\d+',price_raw)
        except:
            pp_hr = ''
            pp_range = ''
            pp_normal = ''
        try:
            bid = job.find('div', attrs={'class': 'JobSearchCard-secondary-entry'})
            bid = bid.text.strip().replace('\n', '')
        except:
            bid = ''

        tag = job.find('a', {'class': 'JobSearchCard-primary-heading-link'})
        link = tag.get('href', None)
        link = 'https://www.freelancer.com' + str(link)
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
        html = requests.get(link, headers=headers)
        soup_1 = BeautifulSoup(html.content, 'html.parser')
        print("Retrieving:",link)
        job_info = soup_1.find('div', {'class': 'Card'})
        try:
            rating = job_info.find('span', {'class': 'Rating Rating--labeled profile-user-rating PageProjectViewLogout-detail-reputation-item'})['data-star_rating']
            country = job_info.find('span', {'itemprop': 'location'})
            country = country.find('span')['aria-label']
        except:
            rating = ''
            country = ''
        sleep(randint(1,2))
        info = [title, days, checkNone(pp_normal), checkNone(pp_range), checkNone(pp_hr), bid, rating, country]
        print(info)
        count += 1
        csv_writer.writerow([title, days, checkNone(pp_hr), checkNone(pp_range), checkNone_2(pp_range), checkNone(pp_normal), bid, rating, country])


csv_file.close()
print('Jobs:', count)
print('Pages:', page)
