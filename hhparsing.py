import requests
import pprint
from functions import *
import json
import time

database = []


for page in range(0, 50):
    vacancies_search = request(page)
    time.sleep(0.25)
    database.append(vacancies_search)

av_zp = average_salary(database)
count_vacancies = vacancies_search['found']

print("1. Количество вакансий, удовлетворяющих критериям поиска: ", count_vacancies)
print("2. Средняя заработная плата :", round(av_zp))

vacancies_url = []
skills = []

for page in database:
    items = page['items']
    for vacancie in items:
        url = vacancie['url']
        result1 = requests.get(url).json()
        vacancies_url.append(result1)

for i in vacancies_url:
    skill = i['key_skills']
    if skill != None:
        skills.append(skill)

skills2 = []
for skill in skills:
    for i in skill:
        for key, value in i.items():
            skills2.append(value)

key_skills_list = []
for skill in skills2:
    if skill not in key_skills_list:
        key_skills_list.append(skill)
print("3. Требования к соискателям: \n", key_skills_list)

key_skills = {}
for item in skills2:
    # если он уже там есть
    if item in key_skills:
        # то мы его увеличиваем на 1
        key_skills[item] += 1
    else:
        # а если еще там нет
        # то мы его записываем со значением 1
        key_skills[item] = 1
result = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)

print("4. Требования к соискателям (количественное выражение): \n", result)

sum_of_values = sum(key_skills.values())
key_skills2 = dict(map(lambda v:[v[0], round(v[1] / sum_of_values * 100, 1)], key_skills.items()))
key_skills2_sort = dict(sorted(key_skills2.items(), key=lambda x: x[1], reverse=True))
key_skills_persent = dict(map(lambda v:[v[0], str(v[1]) + "%"], key_skills2_sort.items()))

print("5. Частота требования к соискателю в процентах: \n", key_skills_persent)

result_file = {"1. Количество вакансий, удовлетворяющих критериям поиска: ": count_vacancies,
               "2. Средняя заработная плата :": round(av_zp),
               "3. Требования к соискателям: \n": key_skills_list,
               "4. Требования к соискателям (количественное выражение): \n": result,
               "5. Частота требования к соискателю в процентах: \n": key_skills_persent}

FILE_NAME = "hhparsing.json"
with open(FILE_NAME, 'w') as f:
    json.dump(result_file, f)