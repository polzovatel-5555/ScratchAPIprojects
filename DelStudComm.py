import requests
import re
import html
def gettoken(username, password):
    session = requests.Session()
    resp = session.get("https://scratch.mit.edu/csrf_token/")
    csrf_token = session.cookies.get('scratchcsrftoken')
    headers = {
        "referer": "https://scratch.mit.edu",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf_token,
        "Content-Type": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }
    body = {
        "username": username,
        "password": password,
        "useMessages": "true"
    }
    respo = session.post(
        "https://scratch.mit.edu/accounts/login/",
        headers=headers,
        json=body
    )
    if respo.status_code == 200:
        data = respo.json()
        token = data[0].get("token")
        return {"success": True, "data": token}
    elif respo.status_code == 403:
        return {"success": False, "data": data[0].get("msg")}
def decode(text):
    text = html.unescape(text) #Преобразовать чепуху с русскими буквами в нормальный вид
    text = text.replace('<img src="/images/emoji/lol-cat.png" class="emoji" alt="lol-cat emoji">', '😹')#                  Э
    text = text.replace('<img src="/images/emoji/upside-down-cat.png" class="emoji" alt="upside-down-cat emoji">', '🙃')#  М
    text = text.replace('<img src="/images/emoji/cat.png" class="emoji" alt="cat emoji">', '😺')#                          О
    text = text.replace('<img src="/images/emoji/meow.png" class="emoji" alt="meow emoji">', '_meow_')#                    Д
    text = text.replace('<img src="/images/emoji/gobo.png" class="emoji" alt="gobo emoji">', '_gobo_')#                    З
    text = text.replace('<img src="/images/emoji/taco.png" class="emoji" alt="taco emoji">', '🌮')#                       И
    text = text.replace('<img src="/images/emoji/huh-cat.png" class="emoji" alt="huh-cat emoji">', '😼')
    text = text.replace('<img src="/images/emoji/aww-cat.png" class="emoji" alt="aww-cat emoji">', '😸')
    text = text.replace('<img src="/images/emoji/10mil.png" class="emoji" alt="10mil emoji">', '🎉')
    text = text.replace('<img src="/images/emoji/camera.png" class="emoji" alt="camera emoji">', '📷')
    text = text.replace('<img src="/images/emoji/blm.png" class="emoji" alt="blm emoji">', '✊')#       ОСУЖ
    text = text.replace('<img src="/images/emoji/pride.png" class="emoji" alt="pride emoji">', '🏳️‍🌈')#   ДАЮ
    text = text.replace('<img src="/images/emoji/pizza-cat.png" class="emoji" alt="pizza-cat emoji">', '_:D<_')
    text = text.replace('<img src="/images/emoji/rainbow-cat.png" class="emoji" alt="rainbow-cat emoji">', '[Rainbow cat]')
    text = text.replace('<img src="/images/emoji/pizza.png" class="emoji" alt="pizza emoji">', '🍕')
    text = text.replace('<img src="/images/emoji/sushi.png" class="emoji" alt="sushi emoji">', '🍣')
    text = text.replace('<img src="/images/emoji/fav-it-cat.png" class="emoji" alt="fav-it-cat emoji">', '🤩')
    text = text.replace('<img src="/images/emoji/waffle.png" class="emoji" alt="waffle emoji">', '🧇')
    text = text.replace('<img src="/images/emoji/tongue-out-cat.png" class="emoji" alt="tongue-out-cat emoji">', '😛')
    text = text.replace('<img src="/images/emoji/love-it-cat.png" class="emoji" alt="love-it-cat emoji">', '😍')
    text = text.replace('<img src="/images/emoji/compass.png" class="emoji" alt="compass emoji">', '🧭')
    text = text.replace('<img src="/images/emoji/candycorn.png" class="emoji" alt="candycorn emoji">', '🍬')
    text = text.replace('<img src="/images/emoji/map.png" class="emoji" alt="map emoji">', '🗺️')
    text = text.replace('<img src="/images/emoji/apple.png" class="emoji" alt="apple emoji">', '🍎')
    text = text.replace('<img src="/images/emoji/binoculars.png" class="emoji" alt="binoculars emoji">', '🔭')
    text = text.replace('<img src="/images/emoji/broccoli.png" class="emoji" alt="broccoli emoji">', '🥦')
    text = text.replace('<img src="/images/emoji/suitcase.png" class="emoji" alt="suitcase emoji">', '💼')
    text = text.replace('<img src="/images/emoji/cupcake.png" class="emoji" alt="cupcake emoji">', '🧁')
    text = text.replace('<img src="/images/emoji/cupcool-catcake.png" class="emoji" alt="cool-cat emoji">', '😎')
    text = text.replace('<img src="/images/emoji/wink-cat.png" class="emoji" alt="wink-cat emoji">', '😜')
    return text
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
    "X-Token": "X-Token" #Если создатель загрузит комментарии через X-Token, то в последующие разы комментарии будут грузиться даже без X-Token-а!
}
print("Привет! Давай я тебе помогу получить комментарии в удалённых студиях!")
isempty = False
while True:
    print("Войди в аккаунт, который является ВЛАДЕЛЬЦЕМ студии!")
    lop = True
    while lop:
        username = input("Введи имя пользователя: ")
        password = input("Введи пароль: ")
        print("Входим...")
        a = gettoken(username, password)
        if a["success"]:
            lop = False
            loltoken = a["data"]
        else:
            print(a["data"])
    print("Введи ссылку или ID студии!")
    studio = int(re.findall(r'\d+', input(">> "))[0]) #Сразу же сохраняем айди студии
    print("Обработка...")
    off = 0
    loop = True
    headers["X-Token"] = loltoken
    while loop:
        rcomments = requests.get(f"https://api.scratch.mit.edu/studios/{studio}/comments?offset={off}&limit=20", headers=headers) #Комментарии, но без ответов
        if rcomments.status_code == 200:
            comments = rcomments.json() #Преобразование в словарь Python
            if len(comments) < 20:
                loop = False
            if len(comments) != 0:
                for comment in comments:
                    print()
                    print(comment["author"]["username"])
                    print(decode(comment["content"]))
                    if comment["reply_count"] > 0:
                        rreplies = requests.get(f'https://api.scratch.mit.edu/studios/{studio}/comments/{comment["id"]}/replies?offset=0&limit=25', headers=headers) #Ответы
                        if rreplies.status_code == 200:
                            replies = rreplies.json()
                            for reply in replies:
                                print()
                                print(f'    {reply["author"]["username"]}')
                                print(f'    {decode(reply["content"])}')
                        else:
                            print(f"    --- Ошибка {rreplies.status_code} ---")
            else:
                print("--- Комментариев в студии нет! ---")
                isempty = True
        else:
            print(f"--- Ошибка {rcomments.status_code} ---")
            loop = False
        if loop:
            print()
            print("--- Нажмите Enter, чтобы загрузить ещё  ---")
            ent = input("--- Нажмите 0 и Enter для выхода в меню ---")
            if ent != "0":
                off += 20
            else:
                loop = False
        else:
            if isempty:
                isempty = False
            else:
                print("--- Комментарии закончились ---")