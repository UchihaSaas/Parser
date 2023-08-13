import requests
from bs4 import BeautifulSoup
import csv

phone_name = input()
url = f"https://indexiq.ru/catalog/{phone_name}/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

try:
    page_count = soup.find('div', class_='pagination').text
    count = int(page_count.split()[-1])
except:
    count = 1

with open(f'{phone_name}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Price'])

    for page_number in range(1, count + 1):
        url_ = f"https://indexiq.ru/catalog/{phone_name}/?p={page_number}"
        response = requests.get(url_)
        soup = BeautifulSoup(response.text, "lxml")
        all_names = soup.find_all('a', class_='product-item__link')
        all_prices = soup.find_all('div', class_='product-item__price-visible')
        for name_, price_ in zip(all_names, all_prices):
            name = name_.find('span').text.strip()
            price = price_.find('span').text.strip().replace(' ', '').replace('\n', '')
            writer.writerow([name,price])
