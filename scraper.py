import json
from bs4 import BeautifulSoup
import requests


def get_html_elements():
    name = []
    link = []
    price = []
    lot = []
    json_dict = {}
    url = 'https://exarid.uzex.uz/ru/ajax/filter?LotID=&PriceMin=&PriceMax=&RegionID=&DistrictID=&INN=305257404' \
          '&CategoryID=&TypeID=&EndDate=&PageSize=20&PageIndex=1&Type=BestOffer&Tnved= '
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Mobile Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    html = r.text
    with open("index.html", "w") as file:
        file.write(html)
    with open("index.html") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    offers = soup.find_all("tr")

    for item in offers[1:]:
        price_text = item.find_all("td", class_="right_text")
        names_dict = item.find_all("a", class_="table_link")
        for i in range(1, len(names_dict), 2):
            name.append(names_dict[i].text)
        for i in range(0, len(names_dict), 2):
            lot.append(names_dict[i].text)
            link.append('https://exarid.uzex.uz/' + names_dict[i].get("href"))
        for i in range(len(price_text)):
            price.append(price_text[i].text)
    for i in range(len(name)):
        json_dict[lot[-i]] = {
            "name": name[-i],
            "link": link[-i],
            "price": price[-i]
        }
    with open('dictionary.json', "w") as file:
        json.dump(json_dict, file, indent=4, ensure_ascii=False)


def get_new_offers():
    name = []
    link = []
    price = []
    lot = []
    fresh_offers = {}
    url = 'https://exarid.uzex.uz/ru/ajax/filter?LotID=&PriceMin=&PriceMax=&RegionID=&DistrictID=&INN=305257404' \
          '&CategoryID=&TypeID=&EndDate=&PageSize=20&PageIndex=1&Type=BestOffer&Tnved= '
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Mobile Safari/537.36 "
    }
    r = requests.get(url, headers=headers)
    html = r.text
    with open("index.html", "w") as file:
        file.write(html)
    with open("index.html") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    offers = soup.find_all("tr")
    with open("dictionary.json") as file:
        json_dict = json.load(file)

    for item in offers[1:]:
        names_dict = item.find_all("a", class_="table_link")
        for i in range(0, len(names_dict), 2):
            lot.append(names_dict[i].text)
        for num in range(len(lot)):
            if lot[num] in json_dict:
                continue
            else:
                price_text = item.find_all("td", class_="right_text")
                names_dict = item.find_all("a", class_="table_link")
                for i in range(1, len(names_dict), 2):
                    name.append(names_dict[i].text)
                for i in range(0, len(names_dict), 2):
                    link.append('https://exarid.uzex.uz/' + names_dict[i].get("href"))
                for i in range(len(price_text)):
                    price.append(price_text[i].text)
                for i in range(len(name)):
                    json_dict[lot[i]] = {
                        "name": name[i],
                        "link": link[i],
                        "price": price[i]
                    }
                for i in range(len(name)):
                    fresh_offers[lot[i]] = {
                        "name": name[i],
                        "link": link[i],
                        "price": price[i]
                    }
                with open('dictionary.json', "w") as file:
                    json.dump(json_dict, file, indent=4, ensure_ascii=False)

    return fresh_offers


if __name__ == "__main__":
    get_html_elements()
