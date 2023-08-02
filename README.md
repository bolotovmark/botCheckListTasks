[<img src="https://img.shields.io/badge/Telegram-%40EriskipCheckListBot-blue?logo=telegram">](https://t.me/EriskipCheckListBot)


# <img src="http://eriskip.com/images/logo-black.svg"  width="15%" height="20%"> Бот для отметки ежедневных задач ГК ЭРИС

## Технологии

 * [aiogram 2.25.1](https://github.com/aiogram/aiogram) - работа с Telegram Bot API;
 * sqlite3 - хранение, учет, ведение задач. Разграничение прав доступа

## Установка

Скопируйте файл `env_param` как `.env` (с точкой в начале), откройте и отредактируйте содержимое.
В `.env` должны находиться параметры для первого старта бота: 
```python
# Этот файл необходимо переименовать в ' .env'

# Токен бота, узнать можно у https://t.me/botfather
API_TOKEN='123456789:abcdefghijklmnopqrstuvwxyz'

# Telegram ID первого пользователя
FIRST_USER_ID=566332122434

# Имя первого пользователя
FIRST_USER_NAME='Имя Фамилия Отчество'
```
При первом запуске создаться база данных `db.sqlite`. \

Если необходимо использовать уже существующую базу данных, перед первым запуском перенесите в корень
проекта файл с названием `db.sqlite`:
```
botCheckList/                                     
    ├── adminPanel/                              
    ├── common/    
    ...                            
    ├── db.sqlite            
    └── README.md                            
```