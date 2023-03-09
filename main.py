import csv
from bs4 import BeautifulSoup
import requests


base = 'https://catalogue.ite-expo.ru/'
links = []

for i in range(480, 516):

    response = requests.get(f'https://catalogue.ite-expo.ru/ru-RU/exhibitorlist.aspx?project_id={i}')

    yc_webpage = response.text
    soup = BeautifulSoup(yc_webpage, 'html.parser')

    score = soup.select(selector='#form > section > div > div.exhibitor_list > a')

    for i in score:
        links.append(i.attrs['href'])

contacts_arr = []

for link in links:
    try:
        res = requests.get(f'{base}{link}').text
        soup3 = BeautifulSoup(res, 'html.parser')
        organization = soup3.select(selector='#frameContent > div > div:nth-child(1) > h2')
        tel = soup3.select(selector='#frameContent > div > div:nth-child(5) > div > p')
        site = soup3.select(selector='#frameContent > div > div:nth-child(6) > div > p')
        email = soup3.select(selector='#frameContent > div > div:nth-child(7) > div > p > a')
        contacts_arr.append({
            'Organization': organization[0].text.strip() if organization else '',
            'Tel': tel[0].text.strip() if tel else '',
            'Site': site[0].text.strip() if site else '',
            'Email': email[0].text.strip() if email else ''
        })
    except Exception as e:
        print(f"An error occurred while processing the link {link}: {e}")


with open('contacts.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Organization', 'Tel', 'Site', 'Email']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for contact in contacts_arr:
        writer.writerow(contact)