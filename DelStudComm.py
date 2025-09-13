import requests
import re
import html

from colorama import Fore, Style
from hashlib import md5

colors = [
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.BLUE,
    Fore.CYAN,
    Fore.MAGENTA,
    Fore.WHITE,
]

emoji_replacements = {
    '<img src="/images/emoji/lol-cat.png" class="emoji" alt="lol-cat emoji">': '😹',
    '<img src="/images/emoji/upside-down-cat.png" class="emoji" alt="upside-down-cat emoji">': '🙃',
    '<img src="/images/emoji/cat.png" class="emoji" alt="cat emoji">': '😺',
    '<img src="/images/emoji/meow.png" class="emoji" alt="meow emoji">': '_meow_',
    '<img src="/images/emoji/gobo.png" class="emoji" alt="gobo emoji">': '_gobo_',
    '<img src="/images/emoji/taco.png" class="emoji" alt="taco emoji">': '🌮',
    '<img src="/images/emoji/huh-cat.png" class="emoji" alt="huh-cat emoji">': '😼',
    '<img src="/images/emoji/aww-cat.png" class="emoji" alt="aww-cat emoji">': '😸',
    '<img src="/images/emoji/10mil.png" class="emoji" alt="10mil emoji">': '🎉',
    '<img src="/images/emoji/camera.png" class="emoji" alt="camera emoji">': '📷',
    '<img src="/images/emoji/blm.png" class="emoji" alt="blm emoji">': '✊',
    '<img src="/images/emoji/pride.png" class="emoji" alt="pride emoji">': '🏳️‍🌈',
    '<img src="/images/emoji/pizza-cat.png" class="emoji" alt="pizza-cat emoji">': '_:D<_',
    '<img src="/images/emoji/rainbow-cat.png" class="emoji" alt="rainbow-cat emoji">': '[Rainbow cat]',
    '<img src="/images/emoji/pizza.png" class="emoji" alt="pizza emoji">': '🍕',
    '<img src="/images/emoji/sushi.png" class="emoji" alt="sushi emoji">': '🍣',
    '<img src="/images/emoji/fav-it-cat.png" class="emoji" alt="fav-it-cat emoji">': '🤩',
    '<img src="/images/emoji/waffle.png" class="emoji" alt="waffle emoji">': '🧇',
    '<img src="/images/emoji/tongue-out-cat.png" class="emoji" alt="tongue-out-cat emoji">': '😛',
    '<img src="/images/emoji/love-it-cat.png" class="emoji" alt="love-it-cat emoji">': '😍',
    '<img src="/images/emoji/compass.png" class="emoji" alt="compass emoji">': '🧭',
    '<img src="/images/emoji/candycorn.png" class="emoji" alt="candycorn emoji">': '🍬',
    '<img src="/images/emoji/map.png" class="emoji" alt="map emoji">': '🗺️',
    '<img src="/images/emoji/apple.png" class="emoji" alt="apple emoji">': '🍎',
    '<img src="/images/emoji/binoculars.png" class="emoji" alt="binoculars emoji">': '🔭',
    '<img src="/images/emoji/broccoli.png" class="emoji" alt="broccoli emoji">': '🥦',
    '<img src="/images/emoji/suitcase.png" class="emoji" alt="suitcase emoji">': '💼',
    '<img src="/images/emoji/cupcake.png" class="emoji" alt="cupcake emoji">': '🧁',
    '<img src="/images/emoji/cupcool-catcake.png" class="emoji" alt="cool-cat emoji">': '😎',
    '<img src="/images/emoji/wink-cat.png" class="emoji" alt="wink-cat emoji">': '😜',
    '\n': ' ',
}

headers = { #Заголовки. Без них запрос бы давал 403
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ru-RU,ru;q=0.8",
    "origin": "https://scratch.mit.edu",
    "priority": "u=1, i",
    "referer": "https://scratch.mit.edu/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "X-Token": "X-Token", #Если создатель загрузит комментарии через X-Token, то в последующие разы комментарии будут грузиться даже без X-Token-а!
}

def gettoken(username, password):
    session = requests.Session()
    session.get("https://scratch.mit.edu/csrf_token/")
    csrf_token = session.cookies.get('scratchcsrftoken')
    headers = {
        "referer": "https://scratch.mit.edu",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf_token,
        "Content-Type": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }
    body = {
        "username": username,
        "password": password,
        "useMessages": "true",
    }
    respo = session.post(
        "https://scratch.mit.edu/accounts/login/",
        headers=headers,
        json=body,
    )
    data = respo.json()

    if respo.status_code == 200:
        token = data[0].get("token")
        return { "success": True, "data": token }

    return { "success": False, "data": data[0].get("msg") }

def decode(text):
    text = html.unescape(text)
    for img, emoji in emoji_replacements.items():
        text = text.replace(img, emoji)
    return text

def print_comments(comments):
    if len(comments) == 0:
        print("--- Комментариев в студии нет! ---")
        return

    for comment in comments:
        username = comment['author']['username']
        print(f'{colors[md5(username.encode()).digest()[0] % len(colors)]}{username:>20}{Style.RESET_ALL}', '>', decode(comment["content"]))
        if comment["reply_count"] > 0:
            res = requests.get(f'https://api.scratch.mit.edu/studios/{studio}/comments/{comment["id"]}/replies?offset=0&limit=25', headers=headers) #Ответы
            if res.status_code != 200:
                print(f"    --- Ошибка {res.status_code} ---")
                print()
                continue

            replies = res.json()
            for reply in replies:
                username = reply["author"]["username"]
                print(f'{colors[md5(username.encode()).digest()[0] % len(colors)]}{username:>24}{Style.RESET_ALL}', '>', f'{Fore.LIGHTBLACK_EX}{decode(reply["content"])}{Style.RESET_ALL}')
            print()

    if len(comments) < 20: 
        print("--- Комментарии закончились ---")

print("Привет! Давай я тебе помогу получить комментарии в удалённых студиях!")
print("Войди в аккаунт, который является ВЛАДЕЛЬЦЕМ студии!")

while True:
    username = input("Введи имя пользователя: ")
    password = input("Введи пароль: ")
    print("Входим...")
    res = gettoken(username, password)
    if res["success"]:
        headers["X-Token"] = res["data"]
        break

    print(res["data"])

print("Введи ссылку или ID студии!")
studio = int(re.findall(r'\d+', input(">> "))[0]) #Сразу же сохраняем айди студии
print("Обработка...")

off = 0
while True:
    res = requests.get(f"https://api.scratch.mit.edu/studios/{studio}/comments?offset={off}&limit=20", headers=headers) #Комментарии, но без ответов
    if res.status_code != 200:
        print(f"--- Ошибка {res.status_code} ---")
        break
    comments = res.json()
    print_comments(comments)
    if len(comments) < 20: break

    print()
    print("--- Нажмите Enter, чтобы загрузить ещё  ---")
    ent = input("--- Нажмите 0 и Enter для выхода ---")
    if ent == "0": break
    off += 20
