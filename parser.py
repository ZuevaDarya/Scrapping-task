from urllib.request import urlopen
from bs4 import BeautifulSoup

import os

html = urlopen('https://habr.com/ru/search/?q=webgl')
# html = urlopen('https://habr.com/ru/search/?q=web') output_1.txt
# html = urlopen('https://habr.com/ru/search/?q=python') output_2.txt

bs = BeautifulSoup(html.read(), 'html.parser')

titleList = bs.find_all('h2', {'class': 'tm-article-snippet__title_h2'})
authorList = bs.find_all('span', {'class': 'tm-user-info'})
keywordList = bs.find_all('div', {'class': 'tm-article-snippet__hubs'})
descriptionList = bs.find_all('div', {'class': 'article-formatted-body'})

dataArr = [titleList, authorList, keywordList, descriptionList]

new_file = 'output.txt'
dir = './'


def txt_writer(data, new_file, dir):
    file_name = check_file(new_file, dir)
    path = dir + file_name

    with open(path, 'w', encoding='utf-8') as txt_file:
        for i in range(20):
            txt_file.write(f'Сатья: {data[0][i].get_text()}\n')

            author = data[1][i].get_text().replace("\n", "").replace(" ", "")
            txt_file.write(f'Автор: {author}\n')

            keyword = data[2][i].get_text().replace("*", "")
            txt_file.write(f'Ключевые слова: {keyword}\n')

            description = data[3][i].get_text().replace("\n", "")
            txt_file.write(f'Описание: {description}\n\n')


def check_file(new_file, dir):
    file_name = new_file.split('.')[0]
    file_expansion = new_file.split('.')[1]

    file_count = 0
    dir_files = []

    for dir_file in os.walk(dir):
        dir_files.append(dir_file)

    for files in dir_files:
        for dir_file in files[2]:
            dir_file_name = dir_file.split('.')[0]
            if file_name in dir_file_name and dir_file.split('.')[1] == file_expansion:
                file_count += 1

    return f"{file_name}_{file_count}.{file_expansion}"


txt_writer(dataArr, new_file, dir)
