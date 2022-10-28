![Foodgram workflow](https://github.com/MrBrus/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# FOODGRAM - Незаменимый продуктовый помощник для любой хозяйки.
[http://mrbrusfoodgramproject.hapto.org/signin/](http://84.201.155.223/signin)

Сервис для обмена вашимих любимых рецептов на любимые рецепты других пользователей.

Использовать сервис можно и анонимно, но так невозмоно познать всех его прелестей, а именно:

 - Удобная и интуитивно понятная регистрация с использованием токена для аутентификации на странице.

 - Легкий, но в то же время гибкий интерфейс создания/редактирования для ваших рецептов. Скорее поделитесь ими со всем миром!
 
 - Не хотите потерять рецепты? Скорее подпишитесь на любимого автора! Кто 
   знает, возможно он будущий повар в ресторане со звездой Мишлен?
 
 - Понравился только один рецепт? Не беда! Можно одним кликом добавить его в избранное и уж тогда его точно не упустите в море других разнообразных рецептов!
 
 - Но что делать, если рецепт понравился, а записать его негде? Скриншот? Банально. Три легких клика (Добавить в список покупок - Списко покупок - Скачать) отделяют Вас от замечательного PDF файла, в котором сохранится даже маленькая щепотка перца чили, чтобы вы были уверенны, что получите именно то, что описал автор.


## Используемые технологии

- Django
- Django Rest Framework
- Docker
- Docker-compose
- Gunicorn
- Nginx
- PostgreSQL



    


## Workflow

- **tests:** Проверка кода на соответствие PEP8.
- **push Docker image to Docker Hub:** Сборка и публикация образа на DockerHub.
- **deploy:** Автоматический деплой на боевой сервер при пуше в главную ветку main.
- **send_massage:** Отправка уведомления в телеграм-чат.



## Запуск проекта


- Склонируйте репозиторий с проектом:

```bash
  git clone https://github.com/MrBrus/foodgram-project-react
```

### ЛОКАЛЬНЫЙ ЗАПУСК ПРОЕКТА

- Перейдите в папку с настройками бэкенда проекта:

```
  \foodgram-project-react\backend\foodgram
```
- Замените в файле settings.py пункт DATABASES следующим содержанием:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

- Установите и активируйте виртуальное окружение.
```bash
python -m venv venv

source venv/Scripts/activate
```
- Перейдите в папку с проектом 

```bash
  cd \foodgram-project-react\backend
```
- Установите зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```
- Выполните последовательно следующие команды:
```bash
python manage.py makemigrations

python manage.py migrate

python manage.py import_csv

python manage.py collectstatic

python manage.py createsuperuser
"следуйте инструкции по созданию суперпользователя"
```
### YOU ARE BREATHTAKING!

- Перейдите в папку с настройками фронтенда проекта:

```
  \foodgram-project-react\backend\frontend
```
- Замените в файле package.json пункт proxy следующим содержанием:
```
"proxy": "http://127.0.0.1:8000/"
```
- Установите программу [NodeJS](https://nodejs.org/en/download/) для вашей системы.

- В GIT перейдите в папку фронтенда:
```
cd \foodgram-project-react\frontend
```
- Выполните последовательно следующие команды:
```bash
npm install --legacy-peer-deps

npm run build

npm start
```
## YOU ARE BREATHTAKING TWICE!

Откроется окно браузера с вкладкой
```
http://127.0.0.1:8000/ (после "/" введите recipe и нажмите enter.)
```
_________________________________________________________________________________________



### ЗАПУСК НА СОБСТВЕННОЙ ВИРТУАЛЬНОЙ МАШИНЕ

Зарегистрируйтесь на [Docker Hub](https://hub.docker.com/).

- Выполните вход на удаленный сервер
- Установите docker на сервер:
```bash
sudo apt install docker.io 
```
- Установите docker-compose на сервер:
```bash
sudo apt-get update
sudo apt install docker-compose
```
На локальной машине:

- Перейдите в папку \foodgram-project-react\backend и выполните команды:
```bash
sudo docker build -t <логин на DockerHub>/<название образа для бэкенда> .
sudo docker login
sudo docker push <логин на DockerHub>/<название образа для бэкенда> 
```
- Перейти в папку \foodgram-project-react\frontend и выполнить команды:
```bash
sudo docker build -t <логин на DockerHub>/<название образа для фронтэнда> .
sudo docker login
sudo docker push <логин на DockerHub>/<название образа для фронтэнда> 
```
- Перейдите в директорию:
```
 \foodgram-project-react\infra\deploy\
```
- Измените следующие строки в файле docker-compose.yml:
```
backend:
  image: <логин на DockerHub>/<название образа для бэкенда, которое написали>
  
frontend:
  image: <логин на DockerHub>/<название образа для фронтэнда, которое написали>
```
- Перейдите в директорию:
``` 
 \foodgram-project-react\.github\workflows\
```
- Измените следующие строки в файле foodgram_workflow.yml:
```
build_and_push_to_docker_hub:
.......
    tags: ${{ secrets.DOCKER_USERNAME }}/<название образа для бэкенда, которое написали>
    
deploy:
.......
    sudo docker pull ${{ secrets.DOCKER_USERNAME }}/<название образа для бэкенда, которое написали>
```
- Перейдите в директорию:
```
\foodgram-project-react\infra\
```
- Скопируйте файл docker-compose.yml и nginx.conf из директории на сервер:
```bash
scp docker-compose.yml <username>@<host>:/home/<username>/
scp nginx.conf <username>@<host>:/home/<username>/
```
### WORKFLOW

- Для работы с Workflow добавить в Secrets GitHub переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```
- После деплоя изменений в git, дождитесь выполнения всех Actions.
- Зайдите на боевой сервер и выполните следующие команды:
  * Создание и применение миграций
    ```bash
    sudo docker-compose exec backend python manage.py migrate
    ```
  * Загрузка статики
    ```bash
    sudo docker-compose exec backend python manage.py collectstatic --no-input 
    ```
  * Создание суперпользователя Django
    ```bash
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
  * Загрузка подготовленного списка ингредиентов
    ```bash
    sudo docker-compose exec backend python manage.py import_csv
    ```

- Проект будет доступен по вашему IP-адресу.

#### REST API
Документация API доступна по адресу - http://<IP-адрес вашего сервера>/api/docs/

#### Автор:
[Владислав Брусенский](https://github.com/MrBrus/)
