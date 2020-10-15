#! /usr/bin/python python3

import os
import sys
import shutil
import time

# ==========================================
# окрашивание строки в цвет
def green(str):
    return "{startcolor}%s{endcolor}".format(startcolor='\033[32m', endcolor='\033[0m') %(str)

def yellow(str):
    return "{startcolor}%s{endcolor}".format(startcolor='\033[93m', endcolor='\033[0m') %(str)

def red(str):
    return "{startcolor}%s{endcolor}".format(startcolor='\033[31m', endcolor='\033[0m') %(str)

def changeIp(str):
  arr = str.split('.')
  arr[len(arr) - 1] = '0/24'
  return '.'.join(arr)  	
# ==========================================
# метод для обычного вопроса
def ask (title, default_value = False):

    if default_value == False:
        return input( "[*] %s - " %title)

    value = input( "[*] %s [%s] - " %(title, yellow(default_value)))

    if not value:
        value = default_value

    return value

# метод для выборы
def choice(data):

    print("---------------------------------------")
    print(data["title"])

    for key in data['versions']:
        print("[%s] %s" %(key, data['versions'][key]))

    default_element = data["default"]
    choice_element = input( "[*] %s [%s] - " %(data["title_choice"], yellow(default_element)))
    choice_element = choice_element or default_element

    if choice_element in data['versions']:
        return choice_element

    print(red("Данное значение \"%s\" некорректно, повторите ввод" %choice_element))
    choice(data)

def save_file(path_to_file, file):
    f = open(path_to_file, 'w')
    f.write(file)
    f.close()
#-------------------------------------------------
# ПЕРЕМЕНЫЕ ДЛЯ ДЕФОЛТНОЙ КОНФИГУРАЦИИ
# для основы
IS_LARAVEL_PROJECT = True
BASE_PROJECT_NAME = 'Laravel'
BASE_PROJECT_VERSION = 7

# для базы данных
DB_DRIVER_MYSQL = 'mysql'
DB_DRIVER_PGSQL = 'pgsql'
DB_DRIVER = DB_DRIVER_MYSQL
DB_VERSION = '5.7'
DB_NAME = 'db'
DB_USER = 'root'
DB_PASSWORD = 'root'

IS_MIGRATE = True
IS_DUMP = False
IS_DUMP_PATH =False

# для php
PHP_VERSION = '7.4'

# для сервера
SERVER_NGINX = 'Nginx'
SERVER_APACHE = 'Apache'
SERVER = SERVER_NGINX

# домен
DOMAIN = '192.168.150.1'

# git
IS_GIT_INIT = True

# путь к проекту
DEFAULT_NAME_PROJECT = 'project'
CURRENT_PATH = f"{os.path.abspath(os.curdir)}/"

# nodejs
NODE_VERSION = '13'

# redis
IS_REDIS = True
REDIS_PASSWORD = 'secret'

# mailer
IS_MAILER = True
#-------------------------------------------------
#------------------------------- данные для выбора
DATA_SERVER = {'versions': {'1': SERVER_NGINX,'2': SERVER_APACHE,},'default': '1','title': 'Сервер','title_choice': 'Выбор сервера'}
DATA_PHP_VERSION = {'versions': {'1': '7.2','2': '7.3','3': PHP_VERSION,},'default': '3','title': 'Версия php','title_choice': 'Выбор версия php'}
DATA_DB = {'versions': {'1': DB_DRIVER_MYSQL,'2': DB_DRIVER_PGSQL,},'default': '1','title': 'База данных','title_choice': 'Выбор базы данных'}
DATA_NODE_VERSION = {'versions': {'1': '8','2': '12','3': NODE_VERSION,},'default': '3','title': 'NodeJs','title_choice': 'Выбор версии nodejs'}
DATA_REDIS_CHOICE = {'versions': {'1': 'Да','2': 'Нет',},'default': '1','title': 'Redis','title_choice': 'Ваш выбор'}
DATA_MAILER_CHOICE = {'versions': {'1': 'Да','2': 'Нет',},'default': '1','title': 'Локальный Mailer','title_choice': 'Ваш выбор'}
DATA_BASE_PROJECT = {'versions': {'1': 'Laravel (новый)','2': 'Laravel (из репозитория)','3': 'не устанавливать',},'default': '1','title': 'Проект','title_choice': 'Ваш выбор проект'}
DATA_LARAVEL = {'versions': {'1': '6','2': '7','3': '8',},'default': '2','title': 'Версия Laravel','title_choice': 'Ваш выбор версии'}
DATA_MYSQL_VERSION = {'versions': {'1': '5.6','2': '5.7','3': '8',},'default': '2','title': 'Версия MySQL','title_choice': 'Ваш выбор версии'}
DATA_POSTGRES_VERSION = {'versions': {'1': '10','2': '11','3': '12',},'default': '3','title': 'Версия PostgreSQL','title_choice': 'Ваш выбор версии'}
DATA_DB_DATA = {'versions': {'1': 'Запустить миграции','2': 'Не запускать миграции','3': 'Накатить dump (в разработке)',},'default': '1','title': 'Запустить миграции или дамп базы','title_choice': 'Ваш вариант'}
DATA_GIT_INIT = {'versions': {'1': 'Да','2': 'Нет',},'default': '1','title': 'Инициализировать git в проекте','title_choice': 'Ваш вариант'}
run_build_data = {'versions': {'1': 'Да','2': 'Нет',},'default': '1','title': 'Запустить сборку','title_choice': 'Ваш вариант'}
settings_data = {'versions': {'1': 'Да','2': 'Нет (за основу буду взяты значения по дефолту)',},'default': '1','title': 'Детальная настройка проекта','title_choice': 'Ваш вариант'}
settings_default_data = {
    'db_user': DB_USER,
    'db_password': DB_PASSWORD,
    'db_name': DB_NAME,
    'ip': DOMAIN
}

os.system('sudo echo ${USER}')

#------------------------------------------------------
#-------------------------- получение данных по проекту

NAME_PROJECT = ask('Название проекта', DEFAULT_NAME_PROJECT)
CURRENT_PATH += NAME_PROJECT

# получаем путь к проекту
PATH_TO_PROJECT = input("[*] Путь к проекту [%s] - " %(yellow(CURRENT_PATH)))

if not PATH_TO_PROJECT:
    PATH_TO_PROJECT = CURRENT_PATH

print(green("Проект будет инициализирован в каталоге - %s" %(PATH_TO_PROJECT)))


# проверка на наличие папки для проекта
if os.path.exists(PATH_TO_PROJECT):
    print(red("Каталог уже существует по заданому пути - %s" %(PATH_TO_PROJECT)))

    default = 'yes'
    delete = input("[*] Удалить каталог [%s] - " %(yellow(default)))
    delete = delete or default

    if delete == default:
        shutil.rmtree(PATH_TO_PROJECT)
        print(green("Старый каталог удален"))
    else:
        print(red("Нет возможности создать проект (есть существующий каталог)"))
        sys.exit()


# #детальный настройки
settings = True if choice(settings_data) == '1' else False
if settings:
  print(green('Настройка сервисов для докера'))

  DOMAIN = ask('IP адрес (будет использован локально)', settings_default_data['ip'])

  SERVER = DATA_SERVER['versions'][choice(DATA_SERVER)]

  PHP_VERSION = DATA_PHP_VERSION['versions'][choice(DATA_PHP_VERSION)]

    # настройки бд
  DB_DRIVER = DATA_DB['versions'][choice(DATA_DB)]
  if DB_DRIVER == DB_DRIVER_MYSQL:
    DB_VERSION = DATA_MYSQL_VERSION['versions'][choice(DATA_MYSQL_VERSION)]
  elif DB_DRIVER == DB_DRIVER_PGSQL:
    DB_VERSION = DATA_POSTGRES_VERSION['versions'][choice(DATA_POSTGRES_VERSION)]

  print("---------------------------------------")
  print("Настройки подключения к базе данных")

  DB_USER = ask('Пользователь', settings_default_data['db_user'])
  DB_PASSWORD = ask('Пароль', settings_default_data['db_password'])
  DB_NAME = ask('Название бд', settings_default_data['db_name'])

  NODE_VERSION = DATA_NODE_VERSION['versions'][choice(DATA_NODE_VERSION)]

  IS_REDIS = True if choice(DATA_REDIS_CHOICE) == '1' else False
  if IS_REDIS:
      REDIS_PASSWORD = ask('Пароль для redis', REDIS_PASSWORD)

  IS_MAILER = True if choice(DATA_MAILER_CHOICE) == '1' else False

  # ВЫБОР ОСНОВЫ ДЛЯ ПРОЕКТА
  project = DATA_BASE_PROJECT['versions'][choice(DATA_BASE_PROJECT)]
  if project == DATA_BASE_PROJECT['versions']['1']:

    BASE_PROJECT_VERSION = DATA_LARAVEL['versions'][choice(DATA_LARAVEL)]

    # использование миграций или dump
    run_data = DATA_DB_DATA['versions'][choice(DATA_DB_DATA)]
    if run_data == DATA_DB_DATA['versions']['2']:
      IS_MIGRATE = False
    elif run_data == DATA_DB_DATA['versions']['3']:
      IS_MIGRATE = False
      IS_DUMP = True
      print("---------------------------------------")
      IS_DUMP_PATH = ask('Введите полный путь к dump.sql')

        # инициализация git
    git_init = DATA_GIT_INIT['versions'][choice(DATA_GIT_INIT)]
    if git_init == DATA_GIT_INIT['versions']['2']:
      IS_GIT_INIT = False

  elif project == DATA_BASE_PROJECT['versions']['2']:
    IS_LARAVEL_PROJECT = False
    BASE_PROJECT_NAME = 'Проект из репозитория'
    BASE_PROJECT_VERSION = None

    print("---------------------------------------")
    project_from_git = ask('Введите ссылку на репозитрорий')


    # использование миграций или dump
    run_data = DATA_DB_DATA['versions'][choice(DATA_DB_DATA)]
    if run_data == DATA_DB_DATA['versions']['2']:
      IS_MIGRATE = False
    elif run_data == DATA_DB_DATA['versions']['3']:
      IS_MIGRATE = False
      IS_DUMP = True
      print("---------------------------------------")
      IS_DUMP_PATH = ask('Введите полный путь к dump.sql')

    # инициализация git
    git_init = DATA_GIT_INIT['versions'][choice(DATA_GIT_INIT)]
    if git_init == DATA_GIT_INIT['versions']['2']:
      IS_GIT_INIT = False

  elif project == DATA_BASE_PROJECT['versions']['3']:    
    IS_LARAVEL_PROJECT = False
    BASE_PROJECT_NAME = 'Без проекта'
    BASE_PROJECT_VERSION = None
    IS_MIGRATE = False

# вывод настроек
print("===============================================")
print(green("Настройки заданы"))
print(f"Название проекта --- {green(NAME_PROJECT)}")
print(f"Путь к проекту ----- {green(PATH_TO_PROJECT)}")
print(f"IP адрес ----------- {green(DOMAIN)}")
print(f"Версия php --------- {green(PHP_VERSION)}")
print(f"Сервер ------------- {green(SERVER)}")
print(f"База данных -------- {green(DB_DRIVER)}:{green(DB_VERSION)}")
print(f"    user ----------- {green(DB_USER)}")
print(f"    password ------- {green(DB_PASSWORD)}")
print(f"     db ------------ {green(DB_NAME)}")
print(f"Версия Nodejs ------ {green(NODE_VERSION)}")
print(f"Redis -------------- {green(IS_REDIS)}")
print(f"    password ------- {green(REDIS_PASSWORD)}")
print(f"Основа проекта ----- {green(BASE_PROJECT_NAME)}-{green(BASE_PROJECT_VERSION)}")
print(f"Создание данных ------------------------------")
print(f"    миграции ------- {green(IS_MIGRATE)}")
print(f"    dump ----------- {green(IS_DUMP)}")
print(f"    путь к dump ---- {green(IS_DUMP_PATH)}")
print(f"Git init ----------- {green(IS_GIT_INIT)}")
print(f"mailer ------------- {green(IS_MAILER)}")
print("===============================================")

# sys.exit()

run_build = True if choice(run_build_data) == '1' else False

if run_build:
  print('Сборка запущена')
  os.mkdir(PATH_TO_PROJECT)
  start_time = time.time()
else:
  print('Сборка отменена')
  sys.exit()

# сборка
# ==============================================================
# создаем сервер
def create_server(server_driver, project_name, domain):
    os.makedirs(f"{PATH_TO_PROJECT}/docker/storage/logs")
    if server_driver == SERVER_NGINX:
        return create_nginx(project_name, domain)
    elif server_driver == SERVER_APACHE:
        return create_apache(project_name, domain)

# nginx for build
# создает конфигурацию для nginx и Dockerfile
def nginx_file_for_build(path_to_nginx, path_to_nginx_conf):

    os.makedirs(path_to_nginx_conf)

    # создаем файл конфигурации
    conf_file = '''server {
    listen 80;
    charset utf-8;
    server_tokens off;
    index index.php;
    root /app/public;
    
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;

    location / {
        try_files $uri /index.php?$args;
    }

    location ~ \\.php$ {
        fastcgi_split_path_info ^(.+\\.php)(/.+)$;
        fastcgi_pass php-fpm:9000;
        fastcgi_index index.php;
        fastcgi_read_timeout 300;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
}
'''
    docker_file = '''FROM nginx:1.17-alpine

COPY ./dev/nginx/conf.d /etc/nginx/conf.d

WORKDIR /app
'''
    save_file(f"{path_to_nginx_conf}/default.conf", conf_file)
    save_file(f"{path_to_nginx}/Dockerfile", docker_file)

# возвращает сервис для docker-compose
def docker_service_nginx(project_name, domain, path_to_docker_file):
    return (f'''
  nginx:
    build:
      context: docker
      dockerfile: {path_to_docker_file}
    container_name: {project_name}__nginx
    hostname: {project_name}__nginx
    volumes:
      - ./:/app
      - ./docker/storage/logs:/var/log/nginx
    ports:
      - {domain}:80:80
    restart: always
''')

def create_nginx(project_name, domain):

    path_to_nginx = (f"{PATH_TO_PROJECT}/docker/dev/nginx")
    path_to_nginx_conf = (f"{path_to_nginx}/conf.d")
    path_to_docker_file_for_context = 'dev/nginx/Dockerfile'

    nginx_file_for_build(path_to_nginx, path_to_nginx_conf)

    return docker_service_nginx(project_name, domain, path_to_docker_file_for_context)

def docker_service_apache(project_name, domain):
    return (f'''
  apache:
    image: webdevops/apache:alpine
    container_name: {project_name}__apache
    hostname: {project_name}__apache
    environment:
      WEB_DOCUMENT_ROOT: /app/public
      WEB_PHP_SOCKET: php-fpm:9000
      LOG_STDOUT: /app/docker/storage/logs/web.access.log
      LOG_STDERR: /app/docker/storage/logs/web.errors.log
    volumes:
      - ./:/app:rw,cached
    ports:
      - {domain}:80:80
    working_dir: /app
    restart: always
    depends_on:
      - php-fpm
''')

def create_apache(project_name, domain):

    return docker_service_apache(project_name, domain)

# =======================================================
# php-fpm for build

def php_fpm_file_for_build (path_conf, path_php, path_php_fpm, php_version):
    os.makedirs(path_conf)
    os.makedirs(path_php_fpm)

    # создаем php.ini
    php_ini_file = '''max_execution_time = 1000
max_input_time = 1000
memory_limit = 2048M
    '''

    docker_file = (f'''FROM php:{php_version}-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    curl \\
    nano \\
    mc \\
    wget \\
    bash \\
    libpng-dev \\
    libonig-dev \\
    libxml2-dev \\
    zip \\
    unzip \\
    postgresql \\
    libpq-dev \\     
    libfreetype6-dev \\
    libjpeg62-turbo-dev \\
    libwebp-dev \\
    libvpx-dev \\
    zlib1g-dev \\
    libicu-dev \\
    libxpm-dev \\
    libzip-dev \\
    libmemcached-dev \\
    g++

# Clear cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Install PHP extensions
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd
RUN docker-php-ext-install pdo pdo_pgsql opcache zip intl

# Redis
RUN pecl install -o -f redis \\
    && rm -rf /tmp/pear \\
    && docker-php-ext-enable redis

# Change TimeZone
RUN echo "Set default timezone - Europe/Kiev"
RUN echo "Europe/Kiev" > /etc/timezone

COPY ./dev/php/conf.d /usr/local/etc/php/conf.d

ENV COMPOSER_ALLOW_SUPERUSER 1

# устанавливаем пает hirak/prestissimo - чтоб ускорить работу composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/bin --filename=composer --quiet \\
    && composer global require hirak/prestissimo --no-plugins --no-scripts \\
    && rm -rf /root/.composer/cache

WORKDIR /app
''')

    bashrc_file = '''
case $- in
    *i*) ;;
      *) return;;
esac

HISTCONTROL=ignoreboth

shopt -s histappend

HISTSIZE=1000
HISTFILESIZE=2000

shopt -s checkwinsize

[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
  color_prompt=yes
    else
  color_prompt=
    fi
fi

if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
'''
    save_file(f"{path_conf}/php.ini", php_ini_file)
    save_file(f"{path_php_fpm}/Dockerfile", docker_file)
    save_file(f"{path_php}/.bashrc", bashrc_file)

def docker_service_php_fpm(projects_name, path_to_docker_file):
    return (f'''
  php-fpm:
    build:
      context: docker
      dockerfile: {path_to_docker_file}
    container_name: {projects_name}__php-fpm
    hostname: {projects_name}__php-fpm
    environment:
      TERM: xterm-256color
    volumes:
      - ./:/app
      - ./docker/dev/php/.bashrc:/root/.bashrc
''')

def create_php_fpm(projects_name, php_version):

    path_to_php_fpm = (f"{PATH_TO_PROJECT}/docker/dev/php-fpm")
    path_to_php = (f"{PATH_TO_PROJECT}/docker/dev/php")
    path_to_php_conf = (f"{path_to_php}/conf.d")
    path_to_docker_file_for_context = 'dev/php-fpm/Dockerfile'

    php_fpm_file_for_build(path_to_php_conf, path_to_php, path_to_php_fpm, php_version)

    return docker_service_php_fpm(projects_name, path_to_docker_file_for_context)
#=====================================================
# mysql for build

def docker_service_mysql(project_name, domain, db_version, db_user, db_password, db_name):
    return (f'''
  db:
    image: mysql:{db_version}
    container_name: {project_name}__db
    hostname: {project_name}__db
    restart: always
    environment:
      MYSQL_USER: {db_user}
      MYSQL_PASSWORD: {db_password}
      MYSQL_ROOT_USER: {db_user}
      MYSQL_ROOT_PASSWORD: {db_password}
      MYSQL_DATABASE: {db_name}
    ports:
      - {domain}:3306:3306
    volumes:
      - ./docker/storage/db:/var/lib/mysql  
''')

def create_mysql(projects_name, domain, db_version, db_user, db_passowrd, db_name):

    return docker_service_mysql(projects_name, domain, db_version, db_user, db_passowrd, db_name)
#=====================================================
# postgresql for build

def docker_service_postgresql(project_name, domain, db_version, db_user, db_password, db_name):
  return (f'''
  db:
    image: postgres:{db_version}
    container_name: {project_name}__db
    hostname: {project_name}__db
    restart: always
    environment:
      POSTGRES_USER: {db_user}
      POSTGRES_PASSWORD: {db_password}
      POSTGRES_DB: {db_name}
    ports:
      - {domain}:5432:5432
    volumes:
      - ./docker/storage/db:/var/lib/postgresql 
''')

def create_postgresql(projects_name, domain, db_version, db_user, db_passowrd, db_name):

  return docker_service_postgresql(projects_name, domain, db_version, db_user, db_passowrd, db_name)
#=====================================================
def create_db (db_driver, project_name, domain, db_version,db_user, db_password, db_name):
  if db_driver == DB_DRIVER_MYSQL:
    return create_mysql(project_name, domain, db_version, db_user, db_password, db_name)
  else:
    return create_postgresql(project_name, domain, db_version, db_user, db_password, db_name)
#=====================================================
# nodejs for build

# создает Dockerfile для node
def node_file_for_build(path_to_node):

  os.makedirs(path_to_node)

  docker_file = f'''FROM node:{NODE_VERSION}-alpine

WORKDIR /app
'''
  save_file(f"{path_to_node}/Dockerfile", docker_file)

def docker_service_node(project_name, path_to_docker_file):
  return (f'''
  node:
    build:
      context: docker
      dockerfile: {path_to_docker_file}
    container_name: {project_name}__node
    hostname: {project_name}__node
    volumes:
      - ./:/app
    tty: true
''')

def create_node(projects_name):

  path_to_node = (f"{PATH_TO_PROJECT}/docker/dev/node")
  path_to_docker_file_for_context = 'dev/node/Dockerfile'

  node_file_for_build(path_to_node)

  return docker_service_node(projects_name, path_to_docker_file_for_context) 
#=====================================================
# redis for build

def docker_service_redis(project_name, domain):
  return (f'''
  redis:
    image: redis:5.0-alpine
    container_name: {project_name}__redis
    hostname: {project_name}__redis
    ports:
      - {domain}:6379:6379
    command:
      - 'redis-server'
      - '--databases 2'
      - '--save 900 1'
      - '--save 300 10'
      - '--save 60 10000'
      - '--requirepass {REDIS_PASSWORD}'
''')

def create_redis(projects_name, domain):
  if IS_REDIS:
    return docker_service_redis(projects_name, domain)

  return ' '
#=====================================================
# mailer
def create_service_mailer():
    return (f'''
  mailer:
    image: mailhog/mailhog
    container_name: {NAME_PROJECT}__mailer
    hostname: {NAME_PROJECT}__mailer
    ports:
      - {DOMAIN}:8025:8025
      - {DOMAIN}:1025:1025
''')

def create_mailer():
    if IS_MAILER:
        return create_service_mailer()
    return ''
#=====================================================
# create Makefile
def createMakefile():
  makefile = (f'''
.SILENT:

include .env

#=============VARIABLES================
php_container = ${{APP_NAME}}__php-fpm
node_container = ${{APP_NAME}}__node
db_container = ${{APP_NAME}}__db
redis_container = ${{APP_NAME}}__redis
#======================================

#=====MAIN_COMMAND=====================

up: up_docker info

rebuild: down build up_docker info

up_docker:
\tdocker-compose up -d

down:
\tdocker-compose down --remove-orphans

# флаг -v удаляет все volume (очищает все данные)
down-clear:
\tdocker-compose down -v --remove-orphans

build:
\tdocker-compose build

ps:
\tdocker-compose ps

#=======COMMAND_FOR_APP================

app-init: composer-install project-init perm

composer-install:
\tdocker-compose run --rm php-fpm composer install

project-init:
\tdocker-compose run --rm php-fpm php artisan key:generate
\tdocker-compose run --rm php-fpm php artisan ide-helper:generate
\tdocker-compose run --rm php-fpm php artisan ide-helper:meta
\tdocker-compose run --rm php-fpm php artisan migrate
\tdocker-compose run --rm php-fpm php artisan db:seed
#\tdocker-compose run --rm node npm install
#\tdocker-compose run --rm node npm run dev

perm:
\tsudo chmod 777 -R storage

#=======INTO_CONTAINER=================

php_bash:
\tdocker exec -it $(php_container) bash

node_bash:
\tdocker exec -it $(node_container) sh

db_bash:
\tdocker exec -it $(db_container) sh

redis_bash:
\tdocker exec -it $(redis_container) sh
#=======INFO===========================

info:
\techo ${{APP_URL}}; 
''')

  save_file(f"{PATH_TO_PROJECT}/Makefile", makefile)
#=====================================================

path_to_env_file = f"{PATH_TO_PROJECT}/.env"
docker_compose_path = (f"{PATH_TO_PROJECT}/docker-compose.yml")

# СОЗДАЕМ Makefile 
createMakefile()

# СОЗДАЕМ файл docker-compose и конфигурационые файлы для сервисов
print(green('--------------------------------------------------------------------------------------'))
docker_compose_file = (f'''version: "3.7"
services:
{create_server(SERVER, NAME_PROJECT, DOMAIN)}
{create_php_fpm(NAME_PROJECT, PHP_VERSION)}
{create_db(DB_DRIVER, NAME_PROJECT, DOMAIN, DB_VERSION, DB_USER , DB_PASSWORD, DB_NAME)}
{create_node(NAME_PROJECT)}
{create_redis(NAME_PROJECT, DOMAIN)}
{create_mailer()}
networks:
  default:
    driver: bridge
    ipam:
      config:
        - subnet: {changeIp(DOMAIN)} 
''')

save_file(docker_compose_path, docker_compose_file)

# инициализируем git в проекте
if IS_GIT_INIT:
    os.system(f"git -C {PATH_TO_PROJECT} init")

# sys.exit()

os.system(f"docker-compose -f {docker_compose_path} build")
os.system(f"docker-compose -f {docker_compose_path} up -d")

# ЗБОРКА ПОД ЧИCТУЮ LARAVEL
if IS_LARAVEL_PROJECT:
  os.system(f"sudo chmod 777 -R {PATH_TO_PROJECT}/docker")
  os.system(f"docker-compose -f {docker_compose_path} run --rm php-fpm composer create-project --prefer-dist laravel/laravel:^{BASE_PROJECT_VERSION}.0")
  # переносим файлы установленой laravel в папку с нашим проектом
  os.system(f"sudo chmod 777 -R {PATH_TO_PROJECT}/laravel/")
  os.system(f"mv {PATH_TO_PROJECT}/laravel/* {PATH_TO_PROJECT}")
  os.system(f"mv {PATH_TO_PROJECT}/laravel/.* {PATH_TO_PROJECT}")
  os.rmdir(f"{PATH_TO_PROJECT}/laravel")

  # останавливаем контейнеры чтоб перезаписать конфиги и поднять с новыми конфигами
  os.system(f"docker-compose -f {docker_compose_path} down -v --remove-orphans")

  # прописываем конфиги
  # .env
  f = open(path_to_env_file, 'r')
  lines = f.readlines()
  # Закрываем файл
  f.close()

  for key in range(len(lines)):
    if 'APP_NAME=' in lines[key]:
      lines[key] = f"APP_NAME={NAME_PROJECT.capitalize()}\n"
    if 'APP_URL=' in lines[key]:
      lines[key] = f"APP_URL=http://{DOMAIN}\n"
    if 'DB_CONNECTION=' in lines[key]:
      if DB_DRIVER == DB_DRIVER_MYSQL:
        lines[key] = 'DB_CONNECTION=mysql\n'
      elif DB_DRIVER == DB_DRIVER_PGSQL:
        lines[key] = 'DB_CONNECTION=pgsql\n'
    if 'DB_PORT=' in lines[key]:
      if DB_DRIVER == DB_DRIVER_MYSQL:
        lines[key] = 'DB_PORT=3306\n'
      elif DB_DRIVER == DB_DRIVER_PGSQL:
        lines[key] = 'DB_PORT=5432\n'
    if 'DB_DATABASE=' in lines[key]:
      lines[key] = f"DB_DATABASE={DB_NAME}\n"
    if 'DB_HOST=' in lines[key]:
      lines[key] = f"DB_HOST=${{DOMAIN}}\n"
    if 'DB_USERNAME=' in lines[key]:
      lines[key] = f"DB_USERNAME={DB_USER}\n"
    if 'DB_PASSWORD=' in lines[key]:
      lines[key] = f"DB_PASSWORD={DB_PASSWORD}\n"
    if 'DB_HOST=' in lines[key]:
      lines[key] = f"DB_HOST={DOMAIN}\n"
    if IS_REDIS:
      if 'REDIS_HOST=' in lines[key]:
        lines[key] = f"REDIS_HOST={DOMAIN}\n"
      if 'REDIS_PASSWORD=' in lines[key]:
        lines[key] = f"REDIS_PASSWORD={REDIS_PASSWORD}\n"
    if IS_MAILER:
        if 'MAIL_HOST=' in lines[key]:
            lines[key] = f"MAIL_HOST={DOMAIN}\n"
        if 'MAIL_PORT=' in lines[key]:
            lines[key] = f"MAIL_PORT=1025\n"

  lines.append(f"\n")
  lines.append(f"DOCKER_BRIDGE={DOMAIN}\n")
  lines.append(f"DOCKER_NETWORK={changeIp(DOMAIN)}\n")

  # Открываем файл для записи
  save_changes = open(path_to_env_file, 'w')
 
  # Сохраняем список строк
  save_changes.writelines(lines)
 
  # Закрываем файл
  save_changes.close()

  # редактируем docker-compose
  f = open(docker_compose_path, 'r')
  lines = f.readlines()
  f.close()

  for key in range(len(lines)):
    if f"{NAME_PROJECT}__" in lines[key]:
      lines[key] = lines[key].replace(f"{NAME_PROJECT}__", "${APP_NAME}__")

    if f"{DOMAIN}:" in lines[key]:
      lines[key] = lines[key].replace(f"{DOMAIN}", "${DOCKER_BRIDGE}")

    if changeIp(DOMAIN) in lines[key]:
      lines[key] = lines[key].replace(f"{changeIp(DOMAIN)}", "${DOCKER_NETWORK}")
    # перенаправляем данные бд в ларавеловский storage
    if './docker/storage/db' in lines[key]:
      lines[key] = lines[key].replace(f"./docker/storage/db", "./storage/db/")
    # перенаправляем логи в ларавеловский storage
    if '/docker/storage/logs' in lines[key]:
      lines[key] = lines[key].replace(f"/docker/storage/logs", "/storage/logs")
    # подставляем переменые для бд
    if DB_DRIVER == DB_DRIVER_MYSQL:
        if f"MYSQL_USER: {DB_USER}" in lines[key]:
            lines[key] = lines[key].replace(f"MYSQL_USER: {DB_USER}", "MYSQL_USER: ${DB_USERNAME}")
        if f"MYSQL_ROOT_USER: {DB_USER}" in lines[key]:
            lines[key] = lines[key].replace(f"MYSQL_ROOT_USER: {DB_USER}", "MYSQL_ROOT_USER: ${DB_USERNAME}")
        if f"MYSQL_PASSWORD: {DB_PASSWORD}" in lines[key]:
            lines[key] = lines[key].replace(f"MYSQL_PASSWORD: {DB_PASSWORD}", "MYSQL_PASSWORD: ${DB_PASSWORD}")
        if f"MYSQL_ROOT_PASSWORD: {DB_PASSWORD}" in lines[key]:
            lines[key] = lines[key].replace(f"MYSQL_ROOT_PASSWORD: {DB_PASSWORD}", "MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}")
        if f"MYSQL_DATABASE: {DB_NAME}" in lines[key]:
            lines[key] = lines[key].replace(f"MYSQL_DATABASE: {DB_NAME}", "MYSQL_DATABASE: ${DB_DATABASE}")
    elif DB_DRIVER == DB_DRIVER_PGSQL:
        if f"POSTGRES_USER: {DB_USER}" in lines[key]:
            lines[key] = lines[key].replace(f"POSTGRES_USER: {DB_USER}", "POSTGRES_USER: ${DB_USERNAME}")
        if f"POSTGRES_PASSWORD: {DB_PASSWORD}" in lines[key]:
            lines[key] = lines[key].replace(f"POSTGRES_PASSWORD: {DB_PASSWORD}", "POSTGRES_PASSWORD: ${DB_PASSWORD}")
        if f"POSTGRES_DB: {DB_NAME}" in lines[key]:
            lines[key] = lines[key].replace(f"POSTGRES_DB: {DB_NAME}", "POSTGRES_DB: ${DB_DATABASEы}")

  save_changes = open(docker_compose_path, 'w')
  save_changes.writelines(lines)
  save_changes.close()

  # ПЕРЕСТРАИВАЕМ КОНТЕЙНЕРЫ ПОД LARAVEL
  os.system(f"sudo chmod 777 -R {PATH_TO_PROJECT}/storage")
  os.system(f"docker-compose -f {docker_compose_path} --env-file {path_to_env_file} build")
  os.system(f"docker-compose -f {docker_compose_path} --env-file {path_to_env_file} up -d")
  os.system(f"sudo chmod 777 -R {PATH_TO_PROJECT}/storage")
  os.system(f"sudo chmod 777 -R {PATH_TO_PROJECT}/docker")
  # удаляем хранилище данных из папаки докера
  shutil.rmtree(f"{PATH_TO_PROJECT}/docker/storage")

  if IS_MIGRATE:
    print(green('Подымается база данных'))
    time.sleep(15)
    os.system(f"docker-compose -f {docker_compose_path} --env-file {path_to_env_file} run --rm php-fpm php artisan migrate")

# ЗБОРКА ПРОЕКТА ЗАКОНЧЕНА

all_time = time.time() - start_time
print(f"Время зборки - {round(all_time, 3)} sec")
print("Проект готов")
print(f"http://{DOMAIN}")
if IS_MAILER:
    print("Почтовик")
    print(f"http://{DOMAIN}:8025")