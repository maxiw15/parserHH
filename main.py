import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

result = []


def conn():
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    headers = Headers().generate()
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    town = soup.find("button", class_='bloko-link bloko-link_kind-tertiary bloko-link_pseudo').text
    headers = soup.find_all(class_='serp-item')
    for data in headers:
        found = data.find(class_='g-user-content').text
        if "Django" in found or "Flask" in found:
            title = data.find(class_='serp-item__title').text
            href = data.find(class_="serp-item__title").get("href")
            company = data.find(class_='bloko-v-spacing-container bloko-v-spacing-container_base-2').text
            price = data.find("span", class_='bloko-header-section-3')
            if price is not None:
                price = price.text
            else:
                price = "Зарплатная вилка не указана"
            result.append({"title": title, "href": href, "company": company.replace('\xa0', ' '), "price": price, "town": town})
    return result


if __name__ == '__main__':
    with open("data_file.json", "w") as write_file:
        json.dump(conn(), write_file, ensure_ascii=False)
