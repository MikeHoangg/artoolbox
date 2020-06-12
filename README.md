# Тема: Програмна система аналізу зображень для рекомендацій інструментів образотворчого мистецтва 
### Студент: Хоанг В'єт Ха, ПЗПІ-16-2
### Керівник: Доцент кафедри ПІ Груздо Ірина Володимірівна
Рік: 2020

Файли:
- Папка .git - зберігає дані про систему контролю версій
- Файл .gitignore - використовується системою контролю версій для виключення зайвих файлів
- Папки apps, artoolbox - зберігають проекти серверної та веб частин системи
- Папки static, templates - зберігають статичні файли та шаблони HTML для веб-частини додатку
- Файли Dockerfile, compose-local.yml, compose-tensor.yml - файли для розгортання системи за допомогою Docker
- Файли requirements.txt, tensorflow_requirements.txt - файли з переліком необхідних бібліотек
- Файл manage.py - основний файл контролю додатком
- Файл Makefile - файл контролю додатком за допомогою команд

Порядок розгортання:
1. склонувати репозиторій
2. у папці проекту `artoolbox/artoolbox/settings/` використовуючи приклад `artoolbox/artoolbox/settings/settings.example.py` створити файл `artoolbox/artoolbox/settings/settings.py`
3. за допомогою команд `make` запустити проект: `make run`
 
