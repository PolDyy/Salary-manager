# Запуск проекта

1) Создаем директорию для проекта и переходим в него  

2) Клонируем репозиторий с gitlab:  

`git init`  

`git clone https://gitlab.com/Pol_Dy/tast_for_cpht.git`

3) Создаем и активируем виртуальное окружение в корне проекта:  

`python -m venv venv`

`source venv/bin/activate`

4) Установим зависимотси: 

`python -m pip --upgrade pip`

`pip install -r requirements.txt`

5) Переходим директорию main:  

`cd main`

6)Создаем файл .env на основе env_example

7) Запускаем файл-раннер:

`python runner.py`

Все готово!

## Запуск с помощью Docker

1) Создаем директорию для проекта и переходим в него  

2) Клонируем репозиторий с gitlab:  

`git init`  

`git clone https://gitlab.com/Pol_Dy/tast_for_cpht.git`

3)Создаем файл .env на основе env_example

4)  Проверяем установлен ли докер, если нет, то устанавливаем его  
(обратитесь к документации Docker)

5)  Собираем образ по Dockerfile

`sudo docker build -t test_task .`

6)  Запускаем приложение:

`docker run -p 8080:8080 test_task python ./main/runner.py`

Все готово!

