from urllib.request import urlopen
from bs4 import BeautifulSoup

import os
import nltk

html = urlopen('https://gist.githubusercontent.com/nzhukov/b66c831ea88b4e5c4a044c952fb3e1ae/raw/7935e52297e2e85933e41d1fd16ed529f1e689f5/A%2520Brief%2520History%2520of%2520the%2520Web.txt')

bs = BeautifulSoup(html.read(), 'html.parser')

new_file = 'task.txt'
dir = './'
current_folder = 'TASK 2 Part of speech tagging/'

name_tag_group_map = {
    #Существительное
    "Nouns": ['NN', 'NNS', 'NNP', 'NNPS'],
    #Прилагательное
    "Adjectives": ['JJ', 'JJR', 'JJS'],
    #Глаголы
    "Verbs": ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
    #Наречия
    "Adverbs": ['RB', 'RBR', 'RBS'],
    #Междометия
    "Interjections": ['IN'],
    #Предлоги
    "Prepositions": ['PRP', 'PRPS', 'PRP$'],
}

res = {
    #Существительное
    "Nouns": 0,
    #Прилагательное
    "Adjectives": 0,
    #Глаголы
    "Verbs": 0,
    #Наречия
    "Adverbs": 0,
    #Междометия
    "Interjections": 0,
    #Предлоги
    "Prepositions": 0,
}

def txt_writer(data, new_file, dir, current_folder):
    file_name = check_file(new_file, dir, current_folder)
    path = dir + current_folder + file_name

    with open(path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(data.get_text())

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
            if file_name in dir_file_name and len(dir_file_name) - len(file_name) in range(-3, 3) and dir_file.split('.')[1] == file_expansion:
                file_count += 1

    return f"{file_name}_{file_count}.{file_expansion}"


def word_tokenize(file_name, dir, current_folder):
    path = dir + current_folder + file_name

    with open(path, encoding='utf-8') as txt_file:
        tokens = nltk.word_tokenize(txt_file.read())
        tagged = nltk.pos_tag(tokens)

    return tagged

def word_type_calculate(name_tag_group_map, tagged, res):
    for tag in tagged:
        for key in name_tag_group_map:
            for tag_arr in name_tag_group_map[key]:
                if tag[1] == tag_arr:
                   res[key] += 1
    return res


def write_output_file(dir, current_folder, res):
    new_file = 'task_output.txt'
    new_file_name = check_file(new_file, dir, current_folder)

    path = dir + current_folder + new_file_name

    with open(path, 'w', encoding='utf-8') as txt_file:
        for key in res:
            txt_file.write(f'{key}: {res[key]}\n')


file_name = txt_writer(bs, new_file, dir, current_folder)

tagged = word_tokenize(file_name, dir, current_folder)
word_type_calculate(name_tag_group_map, tagged, res)
write_output_file(dir, current_folder, res)
