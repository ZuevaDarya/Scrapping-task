from urllib.request import urlopen
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from urllib.parse import quote

import os
import json
import matplotlib.pyplot as plt
import string

import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist

import pymorphy2

full_source_link = 'https://habr.com/ru/search/?q=' + format(quote("NFT"))
base_link = full_source_link.split( '/')[0] + '//' + full_source_link.split('/')[2]

html = urlopen(full_source_link)
bs = BeautifulSoup(html.read(), 'html.parser')

search_class = 'tm-article-snippet__title-link'
search_tag = 'a'

new_file = 'articles.json'
new_file_links = 'article_links.txt'
new_file_content = 'content.txt'

news_link = 'https://habr.com/ru/news/'
new_file_authors = 'authors.txt'
new_file_authors_statistic = 'authors_statistic.txt'

dir = './'
current_folder = 'TASK 3 Text processing and analysis/'


# Получаем список ссылок для собранных статей
def get_articles_link(data, base_link, search_tag, search_class):
    articles_tag_link = data.find_all(
        f'{search_tag}', {'class': f'{search_class}'})
    link_arr = []

    for link in articles_tag_link:
        link_arr.append(base_link + link.get('href'))

    return link_arr


# переходим по каждой ссылке и парсим в json название и контент статьи
def get_link_content(link_arr):
    links_content = {}

    for i in range(len(link_arr)):
        html = urlopen(link_arr[i])
        bs = BeautifulSoup(html.read(), 'html.parser')

        article_link = link_arr[i]
        article_title = bs.find('h1', {'class': 'tm-article-snippet__title_h1'}).get_text()
        article_content = bs.find('div', {'class': 'tm-article-body'}).get_text()

        link_content = {}
        link_content['href'] = article_link
        link_content['content'] = article_content

        links_content[article_title] = link_content

    return links_content


def json_writer(data, new_file, dir, current_folder):
    file_name = check_file(new_file, dir, current_folder)
    path = dir + current_folder + file_name

    with open(path.format(1), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    return file_name


# Нормализируем текст
def normalize_text(links_content, new_file, dir, current_folder):
    for key in links_content:
        file_name = check_file(new_file, dir, current_folder)
        path = dir + current_folder + file_name

        spec_chars = string.punctuation + '\n\xa0«»\t—…'

        content = f'\n{links_content[key]["content"].lower()}'
        content = remove_chars_from_text(content, spec_chars)
        content = remove_chars_from_text(content, string.digits)

        with open(path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(content)


# Убираем специальные символы из текста
def remove_chars_from_text(text, chars):
    return ''.join([ch for ch in text if ch not in chars])


# Токенизация
def word_tokenize(file_name, dir, current_folder):
    path = dir + current_folder + file_name
    new_text = ''

    with open(path, 'r', encoding='utf-8') as txt_file:
        text = txt_file.read()

    tokens = nltk.word_tokenize(text)
    lemmatizer = pymorphy2.MorphAnalyzer()

    for word in tokens:
        word = lemmatizer.parse(word)
        new_text = f'{new_text} {word[0].normal_form}'

    return new_text


# Создаем облако тегов
def create_word_cloud(new_file, text, dir, current_folder):
    path = dir + current_folder + new_file

    russian_stopwords = stopwords.words('russian')
    english_stopwords = stopwords.words('english')

    stopwords_extend = generate_stopwords_extend(
        'stopwords_extend.txt', dir, current_folder)
    russian_stopwords.extend(stopwords_extend)
    russian_stopwords.extend(english_stopwords)

    wordcloud = WordCloud(stopwords=russian_stopwords, width=1000, height=500, background_color='#272d3b', colormap='Set2').generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    wordcloud.to_file(path)


def generate_stopwords_extend(file_name, dir, current_folder):
    path = dir + current_folder + file_name

    with open(path, 'r', encoding='utf-8') as txt_file:
        stopwords_extend = txt_file.read().split(' ')

    return stopwords_extend


def txt_writer(data, new_file, dir, current_folder):
    file_name = check_file(new_file, dir, current_folder)
    path = dir + current_folder + file_name

    with open(path, 'w', encoding='utf-8') as txt_file:
        for i in range(len(data)):
            txt_file.write(f'{data[i]}\n')

    return file_name


def check_file(new_file, dir, current_folder):
    file_name = new_file.split('.')[0]
    file_expansion = new_file.split('.')[1]

    file_count = 1
    dir_files = []

    for dir_file in os.walk(dir + current_folder):
        dir_files.append(dir_file)

    for files in dir_files:
        for dir_file in files[2]:
            dir_file_name = dir_file.split('.')[0]
            if file_name in dir_file_name and dir_file.split('.')[1] == file_expansion:
                file_count += 1

    return f"{file_name}_{file_count}.{file_expansion}"


def search_file_for_read(search_file, dir, current_folder):
    file_name = search_file.split('.')[0]
    file_expansion = search_file.split('.')[1]

    dir_files = []
    search_files = []

    for dir_file in os.walk(dir + current_folder):
        dir_files.append(dir_file)

    for files in dir_files:
        for dir_file in files[2]:
            dir_file_name = dir_file.split('.')[0]
            if file_name in dir_file_name and dir_file.split('.')[1] == file_expansion:
                search_files.append(dir_file)

    return search_files


# Получаем список ссылок для собранных статей
def get_authors_name(link, new_file, dir, current_folder):
    article_authors_arr = []
    spec_chars = string.punctuation + '\n\xa0\t'

    # Собираем авторов новостей с последних 200 страниц (по 20 публикаций на странице)
    for i in range(200):
        next_page = 'page'
        next_link = f'{link}{next_page}{i + 1}/'

        html = urlopen(next_link)
        bs = BeautifulSoup(html.read(), 'html.parser')
            
        article_authors = bs.find_all("a", {"class": "tm-user-info__username"})
    
        for key in article_authors:
            author_name = remove_chars_from_text(key.get_text(), spec_chars)
            article_authors_arr.append(author_name)


    file_name = txt_writer(article_authors_arr, new_file, dir, current_folder)

    return file_name

# Подсчитываем количество публикаций для каждого автора
def calculate_authors_name(file_name, new_file, dir, current_folder):
    path = dir + current_folder + file_name
    authors = ''

    with open(path, 'r', encoding='utf-8') as txt_file:
        authors = txt_file.read()

    authors = nltk.word_tokenize(authors)
    authors = nltk.Text(authors)
    fdist = FreqDist(authors).most_common()

    txt_writer(fdist, new_file, dir, current_folder) 

# получаем количество публикаций для авторорв с последних 200 страниц из раздела Новости 
authors_file_name = get_authors_name(news_link, new_file_authors, dir, current_folder)
calculate_authors_name(authors_file_name, new_file_authors_statistic, dir, current_folder)

# Записываем ссылки на статьи в txt файл
articles_link_arr = get_articles_link(bs, base_link, search_tag, search_class)
txt_writer(articles_link_arr, new_file_links, dir, current_folder)

# Записываем информацию о всех статьях в json файл
links_content = get_link_content(articles_link_arr)
json_file_name = json_writer(links_content, new_file, dir, current_folder)

normalize_text(links_content, new_file_content, dir, current_folder)

search_files = search_file_for_read('content.txt', dir, current_folder)
for content_file in search_files:
    file_number = content_file.split('_')[1].split('.')[0]

    new_file_cloud = f'word_cloud_{file_number}.png'

    new_text = word_tokenize(content_file, dir, current_folder)
    create_word_cloud(new_file_cloud, new_text, dir, current_folder)
