import json
import requests
import hashlib
import os

''' Класс итератор поиск стран  из файла в системе WIKI '''
class Search_Wiki:
    def __init__(self, country_item):
        self.country_item = country_item
        self.i = 0

    def get_info_wiki(self, country_name):
        res_dic = {}
        r = requests.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + country_name)
        page = r.json()
        res_dic['Title'] = page['title']
        res_dic['Description'] = page['extract']
        res_dic['Link'] = page['content_urls']['desktop']['page']
        return res_dic

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        country_items = self.get_info_wiki(self.country_item[self.i]['name']['common'])
        self.i += 1
        if self.i > 5:
            raise StopIteration
        if country_items is None:
            raise StopIteration
        return str(list(country_items.values())).strip(",")

''' Генератор MD5 Хеш '''
def convert_md5(path_file):
    with open('countries_result.txt', 'r', encoding='utf-8') as myFile:
        for item in myFile.readlines():
            yield hashlib.md5(item.upper().encode('utf-8')).hexdigest()


with open('countries.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
 text = json.load(f)  # загнали все, что получилось в переменную
 f.close()
# Файл для записи
with open('countries_result.txt', 'w', encoding='utf-8') as myFile:

 for txt_ in Search_Wiki(text):
     myFile.write(txt_ + " \n")
 myFile.close()

for item in convert_md5(os.path.abspath('countries_result.txt')):
    print(f"md5: {item}")

