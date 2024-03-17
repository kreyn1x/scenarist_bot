# Бот сценарист
бот-сценарист для telegram на python с нейросетью
# Как использовать
1) Клонируйте этот репозиторий:
```
git clone https://github.com/karukador/scenarist_ai_bot.git
```
2) Установите requirements
3) Получите токен через [BotFather](https://telegram.me/BotFather) в Telegram 
4) В файле config.py вставьте ваш токен:
```
TOKEN = "ВАШ ТОКЕН"
```
5) В файле config.py вставьте ваш telegram id:
```
ADMIN = "ВАШ ID"
```
6) Установите DB Browser
7) Откройте терминал и подключитесь к своей виртуальной машине:   
   • Посмотрите [видео](https://code.s3.yandex.net/kids-ai/video/1710521524357368.mp4) от Яндекс Практикума   
   • Зайдите на сервер, используя команду (указать свой IP и место расположения ключа):   
```
ssh -i <путь_до_файла_с_ключом> student@<ip_адрес_сервера>  
```
   • Посмотрите еще одно [видео](https://code.s3.yandex.net/kids-ai/video/1710080423616925.mp4) о получении IAM-токена   
   • Введите на сервере команду ниже:   
```
curl -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token
```
   • Получите IAM-токен, который живет 12 часов   
# создание финального проекта в процессе
