import requests
import json
import re
from http.cookies import SimpleCookie
from datetime import datetime, timedelta, UTC
def valid(val):
    if val == None:
        return "-"
    else:
        val = str(val)
        if len(val) < 16:
            return val
        else:
            return f'{val[0]}{val[1]}{val[2]}{val[3]}{val[4]}...{val[-5]}{val[-4]}{val[-3]}{val[-2]}{val[-1]}'
def cookie_to_string(cookie):
    c = SimpleCookie()
    c[cookie.name] = cookie.value
    morsel = c[cookie.name]
    if hasattr(cookie, 'domain') and cookie.domain:
        morsel['domain'] = cookie.domain
    if hasattr(cookie, 'path') and cookie.path:
        morsel['path'] = cookie.path
    if hasattr(cookie, 'secure') and cookie.secure:
        morsel['secure'] = True
    if hasattr(cookie, 'httponly') and cookie.httponly:
        morsel['httponly'] = True
    if hasattr(cookie, 'expires'):
        expires_date = datetime.now(UTC) + timedelta(weeks=2)
        morsel['expires'] = expires_date.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
    if hasattr(cookie, 'expires') and isinstance(cookie.expires, int):
        morsel['Max-Age'] = cookie.expires
    return morsel.OutputString()
def isvalid(json_str):
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False
def addnums(num):
    if num < 10:
        return f"{str(num)}. "
    else:
        return f"{str(num)}."
print("Добро пожаловать в систему управления Scratch!")
print("Программу сделал polzovatel_5555")
resp = requests.get("https://api.scratch.mit.edu/")
if resp.json() == {'response': 'Too many requests'}:
    print("К сожалению, доступ к Scratch API недоступен с твоего ip адреса. Если ты запускаешь это в браузере, то запусти его через файл!")
    print("Нажми на клавишу Enter, чтобы проигнорировать предупреждение (не рекомендуется)")
    input()
act = -1
while act != 0:
    print("Выберите действие: (Введите 0 для выхода)")
    print("1. Загрузить проект")
    print("2. Загрузить профиль")
    print("3. Загрузить студию")
    print("4. Войти в аккаунт")
    print("5. Проверить ip адрес на бан")
    print("6. Проверить пароль на надёжность")
    print("7. Логи облачных переменных (любой проект)")
    act = int(input(">> "))
    if (act == 1):
        id = -1
        while id != 0:
            print("Введите ссылку или ID на проект: (Введите 0 чтобы выйти)")
            id = int(re.findall(r'\d+', input(">> "))[0])
            if id != 0:
                resp = requests.get("https://api.scratch.mit.edu/projects/" + str(id))
                if resp.status_code == 200:
                    data = resp.json()
                    print(data.get("title"))
                    print("от", data.get("author").get("username"))
                    print()
                    print("Инструкции:")
                    print(data.get("instructions"))
                    print()
                    print("Примечания и благодарности:")
                    print(data.get("description"))
                    print()
                    if data.get("stats").get("remixes") < 100:
                        resp = requests.get("https://scratch.mit.edu/projects/" + str(id) + "/remixtree/bare")
                        if resp.text != "no data":
                            data = json.loads(resp.text)
                            print("Статус:", (data.get(str(id))).get("moderation_status"))
                            print()
                elif resp.status_code == 404:
                    resp = requests.get("https://api.scratch.mit.edu/projects/" + str(id) + "/remixes")
                    d = resp.json()
                    if len(d) > 0:
                        resp = requests.get("https://scratch.mit.edu/projects/" + str(d[0].get("id")) + "/remixtree/bare")
                        if resp.status_code == 200:
                            a = json.loads(resp.text)
                            data = a.get(str(id))
                            print(data.get("title"))
                            print("от", data.get("username"))
                            print(data.get("love_count"), "лайков,", data.get("favorite_count"), "звёзд,", len(data.get("children")), "ремиксов")
                            print("Статус:", data.get("moderation_status"))
                            print("Видимость:", data.get("visibility"))
                        else:
                            print("Не удалось узнать информацию о проекте. Попробуй ещё раз!")
                    else:
                        print("Не удалось узнать информацию о проекте")
                else:
                    print("Не удалось узнать информацию о проекте")
    elif act == 2:
        user = "!"
        while user != "0":
            print("Введите имя пользователя: (Введите 0 чтобы выйти)")
            user = input(">> ")
            if user != "0":
                resp = requests.get("https://api.scratch.mit.edu/users/" + user)
                if resp.status_code == 200:
                    data = resp.json()
                    print(data.get("username"))
                    print("Из:", data.get("profile").get("country"))
                    print()
                    print("Обо мне:")
                    print(data.get("profile").get("bio"))
                    print()
                    print("Над чем я работаю:")
                    print(data.get("profile").get("status"))
                    resp = requests.get("https://api.scratch.mit.edu/users/" + user + "/messages/count")
                    data = resp.json()
                    print()
                    print("Сообщений:", data.get("count"))
                else:
                    print("Профиль не найден")
    elif act == 3:
        id = -1
        while id != 0:
            print("Введите ссылку или ID на студию: (Введите 0 чтобы выйти)")
            id = int(re.findall(r'\d+', input(">> "))[0])
            if id != 0:
                resp = requests.get("https://api.scratch.mit.edu/studios/" + str(id))
                if resp.status_code == 200:
                    data = resp.json()
                    print(data.get("title"))
                    print()
                    print(data.get("description"))
                    print()
                    print("Комментариев:", data.get("stats").get("comments"))
                    print("Подписчиков:", data.get("stats").get("followers"))
                    print("Менеджеров:", data.get("stats").get("managers"))
                    print("Проектов:", data.get("stats").get("projects"))
                else:
                    print("Не удалось узнать информацию о студии")
    elif act == 4:
        validuser = False
        print("Введи имя пользователя:")
        while validuser != True:
            user = input(">> ")
            resp = requests.get("https://api.scratch.mit.edu/users/" + user)
            if resp.status_code == 200:
                validuser = True
                data = resp.json()
                user = data.get("username")
            else:
                print("Такого имени не существует. Проверь имя на наличие опечаток!")
        validtoken = False
        print("Выбери способ входа:")
        print("1. Через пароль")
        print("2. Через X-Token")
        loginmeth = int(input(">> "))
        haspw = (loginmeth == 1)
        if loginmeth == 1:
            print("Введи пароль: (0 - выйти)")
            loop = True
            while loop:
                pw = input(">> ")
                if pw != "0":
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
                        "username": user,
                        "password": pw,
                        "useMessages": "true"
                    }
                    respo = session.post(
                        "https://scratch.mit.edu/accounts/login/",
                        headers=headers,
                        json=body
                    )
                    if respo.status_code == 200:
                        validtoken = True
                        loop = False
                        data = respo.json()
                        token = data[0].get("token")
                        headers = {
                            "X-Token": token
                        }
                        print("Успешно!")
                        print("Личная информация:")
                        print("X-Token:", token)
                        #print(respo.cookies)
                        cookies = respo.cookies
                        for cook in cookies:
                            #print(cook)
                            if cook.name == 'scratchsessionsid':
                                cookie_string = cookie_to_string(cook)
                                #print(cookie_string)
                        #print(respo.cookies.get('Set-Cookie'))
                        match = re.search(r'([^=]+)="\\"([^"]+)\\""', cookie_string)
                        if match:
                            cookie_name = match.group(1)
                            cookie_value = match.group(2)
                            clean_cookie = f'{cookie_name}="{cookie_value}"'
                            #print(clean_cookie)
                            clean_cookie = clean_cookie + ";scratchcsrftoken=" + csrf_token
                        head = {
                            "Cookie": clean_cookie,
                            "referer": "https://scratch.mit.edu/",
                            "X-Requested-With": "XMLHttpRequest",
                            "X-CSRFToken": csrf_token,
                            "Content-Type": "application/json",
                            "Accept-Language": "ru-RU,ru;q=0.9",
                            "Origin": "https://scratch.mit.edu",
                            "Accept-Encoding": "gzip, deflate, br, zstd",
                            "Accept": "*/*",
                            #"Content-Length": "1693"
                        }
                        #print(cookie_string)
                        resp = requests.get("https://scratch.mit.edu/session/", headers=head)
                        if resp.status_code == 200:
                            if isvalid(resp.text):
                                data = resp.json()
                                print("Почта:", data.get("user").get("email"))
                                months = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
                                print("Месяц и год рождения:", months[data.get("user").get("birthMonth") - 1], data.get("user").get("birthYear"))
                                gender = data.get("user").get("gender")
                                if gender == "male":
                                    print("Пол: мужской")
                                elif gender == "female":
                                    print("Пол: женский")
                                elif gender == "non-binary":
                                    print("Пол: небинарный")
                                elif gender == "(Prefer not to say)":
                                    print("Пол: предпочитаю не говорить")
                                else:
                                    print("Пол:", gender)
                            else:
                                print("Данный аккаунт является сломанным, поэтому часть личной информации недоступна")
                        resp = requests.get("https://api.scratch.mit.edu/users/" + user + "/messages", headers=headers)
                        banned = (resp.status_code == 403)
                    elif respo.status_code == 403:
                        if isvalid(respo.text):
                            data = respo.json()
                            print(data[0].get("msg"))
                        else:
                            print("К сожалению, твой ip адрес находится в бане. Данный способ входа недоступен")
                            pw = "0"
                    else:
                        print("Произошла ошибка с кодом", respo.status_code)
                else:
                    loop = False
                    loginmeth = 0
        elif loginmeth == 2:
            print("Введи X-Token:")
            while validtoken != True:
                token = input(">> ")
                headers = {
                    "X-Token": token
                }
                resp = requests.get("https://api.scratch.mit.edu/users/" + user + "/messages", headers=headers)
                if resp.status_code != 401:
                    validtoken = True
                    if resp.status_code == 403:
                        banned = True
                    elif resp.status_code == 200:
                        banned = False
                    else:
                        banned = False
                        print("Хм. Что-то странное происходит... Зачту токен как правильный, но ожидай появления ошибок!")
                else:
                    print("Токен неверный. Убедись, что он скопирован правильно!")
        if loginmeth == 1 or loginmeth == 2:
            if banned:
                print("! Статус аккаунта: ЗАБАНЕН !")
            else:
                print("Статус аккаунта: живой")
            inp = -1
            while inp != 0:
                print("Выбери нужное: (0 - Выйти)")
                print("1. Предупреждения")
                print("2. Рюкзак")
                print("3. Личные проекты")
                if banned == False:
                    print("4. Добавить проект в студию")
                    print("5. Удалить проект из студии (даже если ты куратор)")
                    print("6. Изменить данные проекта")
                    print("7. Узнать недавно просмотренные проекты")
                    print("8. Обычные сообщения")
                    print("9. Передача прав владельца студии")
                    if haspw:
                        print("10. Сделать ремикс любого проекта")
                        print("11. Подписаться на кого угодно")
                inp = int(input(">> "))
                if inp == 1:
                    resp = requests.get("https://api.scratch.mit.edu/users/" + user + "/messages/admin", headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        #arr = json.loads(data)
                        if len(data) == 0:
                            print("Предупреждений нет!")
                        else:
                            for i in data:
                                print(i.get("message"))
                                print()
                    else:
                        print("Ошибка", resp.status_code)
                elif inp == 2:
                    resp = requests.get("https://backpack.scratch.mit.edu/" + user, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        #Программу сделал пользователь 5555
                        n = 0
                        if len(data) == 0:
                            print("Рюкзак пустой!")
                        else:
                            for i in data:
                                n += 1
                                print(str(n) + ". " + i.get("name"))
                                print("https://backpack.scratch.mit.edu/" + i.get("body"))
                    else:
                        print("Ошибка", resp.status_code)
                elif inp == 3:
                    print("Введите ссылку или ID на проект: (Введите 0 чтобы выйти)")
                    id = int(re.findall(r'\d+', input(">> "))[0])
                    if id != 0:
                        resp = requests.get("https://api.scratch.mit.edu/projects/" + str(id), headers=headers)
                        if resp.status_code == 200:
                            data = resp.json()
                            print(data.get("title"))
                            print("от", data.get("author").get("username"))
                            print()
                            print("Инструкции:")
                            print(data.get("instructions"))
                            print()
                            print("Примечания и благодарности:")
                            print(data.get("description"))
                            print()
                            print(f"Ссылка: https://turbowarp.org/{id}/#?token={data.get("project_token")}")
                        else:
                            print("Не удалось узнать информацию о проекте")
                elif banned == False:
                    if inp == 4:
                        print("Введи ссылку или ID на студию:")
                        studio = int(re.findall(r'\d+', input(">> "))[0])
                        print("Введи ссылку или ID на проект:")
                        project = int(re.findall(r'\d+', input(">> "))[0])
                        resp = requests.post("https://api.scratch.mit.edu/studios/" + str(studio) + "/project/" + str(project), headers=headers)
                        if resp.status_code == 200:
                            print("Успешно!")
                        elif resp.status_code == 403:
                            print("Это не разрешено делать. Возможные причины:")
                            print("1. Проект не в общем доступе")
                            print("2. Аккаунт не является куратором, а проекты могут добавлять только кураторы")
                            print("3. Аккаунт забанен")
                        elif resp.status_code == 404:
                            print("Студия не найдена")
                        else:
                            print("Произошла ошибка", resp.status_code)
                    elif inp == 5:
                        print("Введи ссылку или ID на студию:")
                        studio = int(re.findall(r'\d+', input(">> "))[0])
                        print("Введи ссылку или ID на проект:")
                        project = int(re.findall(r'\d+', input(">> "))[0])
                        resp = requests.delete("https://api.scratch.mit.edu/studios/" + str(studio) + "/project/" + str(project), headers=headers)
                        if resp.status_code == 200 or resp.status_code == 204:
                            print("Успешно!")
                        elif resp.status_code == 403:
                            print("Это не разрешено делать")
                        elif resp.status_code == 404:
                            print("Студия не найдена")
                        else:
                            print("Произошла ошибка", resp.status_code)
                    elif inp == 6:
                        print("Введи ссылку или ID на проект, который изменить")
                        id = int(input(">> "))
                        inp = -1
                        while inp != 0:
                            print("Что ты хочешь изменить? (введи 0 для выхода)")
                            print("1. Название")
                            print("2. Инструкции")
                            print("3. Примечания и благодарности")
                            print("4. Включить/выключить комментарии")
                            inp = int(input(">> "))
                            if inp == 1:
                                print("Введи новое название проекта:")
                                name = input(">> ")
                                resp = requests.put("https://api.scratch.mit.edu/projects/" + str(id), headers=headers, json={"title": name})
                                if resp.status_code == 200:
                                    print("Успешно!")
                                elif resp.status_code == 404:
                                    print("Проект не найден")
                                elif resp.status_code == 403:
                                    print("Похоже, что проект не твой")
                                elif resp.status_code == 400:
                                    print("Кажется, сработал фильтр")
                                else:
                                    print("Внезапно произошла ошибка с кодом", resp.status_code)
                            elif inp == 2:
                                print("Введи новое содержимое инструкций:")
                                name = input(">> ")
                                resp = requests.put("https://api.scratch.mit.edu/projects/" + str(id), headers=headers, json={"instructions": name})
                                if resp.status_code == 200:
                                    print("Успешно!")
                                elif resp.status_code == 404:
                                    print("Проект не найден")
                                elif resp.status_code == 403:
                                    print("Похоже, что проект не твой")
                                elif resp.status_code == 400:
                                    print("Кажется, сработал фильтр")
                                else:
                                    print("Внезапно произошла ошибка с кодом", resp.status_code)
                            elif inp == 3:
                                print("Введи новое содержимое примечаний и благодарностей:")
                                name = input(">> ")
                                resp = requests.put("https://api.scratch.mit.edu/projects/" + str(id), headers=headers, json={"description": name})
                                if resp.status_code == 200:
                                    print("Успешно!")
                                elif resp.status_code == 404:
                                    print("Проект не найден")
                                elif resp.status_code == 403:
                                    print("Похоже, что проект не твой")
                                elif resp.status_code == 400:
                                    print("Кажется, сработал фильтр")
                                else:
                                    print("Внезапно произошла ошибка с кодом", resp.status_code)
                            elif inp == 4:
                                print("1 - Включить комментарии")
                                print("0 - Выключить комментарии")
                                temp = input(">> ")
                                if temp:
                                    resp = requests.put("https://api.scratch.mit.edu/projects/" + str(id), headers=headers, json={"comments_allowed": True})
                                else:
                                    resp = requests.put("https://api.scratch.mit.edu/projects/" + str(id), headers=headers, json={"comments_allowed": False})
                                
                                if resp.status_code == 200:
                                    print("Успешно!")
                                elif resp.status_code == 404:
                                    print("Проект не найден")
                                elif resp.status_code == 403:
                                    print("Похоже, что проект не твой")
                                else:
                                    print("Внезапно произошла ошибка с кодом", resp.status_code)
                    elif inp == 7:
                        resp = requests.get("https://api.scratch.mit.edu/users/" + user + "/projects/recentlyviewed?limit=40", headers=headers)
                        if resp.status_code == 200:
                            data = resp.json()
                            #arr = json.loads(data)
                            if len(data) == 0:
                                print("Просмотренных проектов нет!")
                            else:
                                for i in data:
                                    print(i.get("title"))
                    elif inp == 8:
                        resp = requests.get("https://api.scratch.mit.edu/users/" + user + "/messages?limit=40", headers=headers)
                        if resp.status_code == 200:
                            data = resp.json()
                            if len(data) == 0:
                                print("Сообщений нет!")
                            for msg in data:
                                type = msg.get("type")
                                if type == "addcomment":
                                    if msg.get("comment_type") == 0:
                                        print(msg.get("actor_username"), "комментирует в проекте \"" + msg.get("comment_obj_title") + "\":")
                                    elif msg.get("comment_type") == 1:
                                        print(msg.get("actor_username"), "комментирует в профиле", msg.get("comment_obj_title") + ":")
                                    elif msg.get("comment_type") == 2:
                                        print(msg.get("actor_username"), "комментирует в студии \"" + msg.get("comment_obj_title") + "\":")
                                    print(msg.get("comment_fragment"))
                                elif type == "studioactivity":
                                    print("Новая активность в студии \"" + msg.get("title") + "\"")
                                elif type == "curatorinvite":
                                    print(msg.get("actor_username"), "пригласил в студию \"" + msg.get("title") + "\"")
                                elif type == "followuser":
                                    print(msg.get("actor_username"), "подписался")
                                elif type == "loveproject":
                                    print(msg.get("actor_username"), "нравится проект \"" + msg.get("title") + "\"")
                                elif type == "favoriteproject":
                                    print(msg. get("actor_username"), "добавил в избранное проект \"" + msg.get("project_title") + "\"")
                                elif type == "becomeownerstudio":
                                    print(msg.get("actor_username"), "повысил до менеджера в студии \"" + msg.get("gallery_title") + "\"")
                                elif type == "becomehoststudio":
                                    print(msg.get("actor_username"), "назначил владельцем студии \"" + msg.get("gallery_title") + "\"")
                                elif type == "remixproject":
                                    print(msg.get("actor_username"), "сделал ремикс")
                                    print("Исходный проект:", msg.get("parent_title"))
                                    print("Ремикс:", msg.get("title"))
                                elif type == "forumpost":
                                    print(msg.get("actor_username"), "написал пост в теме \"" + msg.get("topic_title") + "\"")
                                elif type == "userjoin":
                                    print("Приветственное сообщение")
                                else:
                                    print("Неизвестное сообщение")
                        elif resp.status_code == 403:
                            print("Аккаунт забанили!")
                            banned = True
                        else:
                            print("Произошла ошибка", resp.status_code)
                    elif inp == 9:
                        print("Введи ссылку или ID на студию:")
                        id = int(input(">> "))
                        print("Введи имя того, кому передать студию:")
                        tr = input(">> ")
                        if loginmeth == 2:
                            print("Scratch требует ввести пароль от", user, "в целях безопасности. Введи его:")
                            pw = input(">> ")
                        resp = requests.put("https://api.scratch.mit.edu/studios/" + str(id) + "/transfer/" + tr, headers=headers, json={"password": pw})
                        if resp.status_code == 200:
                            print("Студия успешно передана", tr + "!")
                        elif resp.status_code == 403:
                            print("Студия не твоя")
                        elif resp.status_code == 409:
                            print(tr, "не является менеджером в студии")
                        elif resp.status_code == 404:
                            print("Студия не найдена")
                        elif resp.status_code == 429:
                            print("Студия может менять владельца раз в сутки. Попробуй ещё раз позже!")
                        elif resp.status_code == 401:
                            print("Пароль неверный!")
                        else:
                            print(resp.status_code, resp.json())
                    elif haspw:
                        if inp == 10:
                            print("Введи ссылку или ID на проект, ремикс которого нужно сделать:")
                            rm = int(input(">> "))
                            print("Делаем ремикс...")
                            resp = requests.get("https://api.scratch.mit.edu/projects/510186917/")
                            data = resp.json()
                            resp = requests.get("https://projects.scratch.mit.edu/510186917?token=" + data.get("project_token"))
                            data = resp.json()
                            head = {
                                "x-csrftoken": csrf_token,
                                "x-requested-with": "XMLHttpRequest",
                                "Cookie": clean_cookie,
                                "referer": "https://scratch.mit.edu/",
                                "user-agent": "Mozilla/5.0"
                            }
                            resp = requests.post("https://projects.scratch.mit.edu/?is_remix=1&original_id=" + str(rm), headers=head, json=data)
                            if resp.status_code == 200:
                                data = resp.json()
                                print("Успешно! В качестве заполнителя используется пустой проект, но название и инструкции доступны!")
                                print("ID проекта:", data.get("content-name"))
                            elif resp.status_code == 403:
                                print("Не удалось сделать ремикс. Возможная причина: проект сделан в очень ранней версии Scratch")
                        elif inp == 11:
                            print("Введи имя того, на кого подписаться:")
                            rm = input(">> ")
                            head = {
                                "x-csrftoken": csrf_token,
                                "x-requested-with": "XMLHttpRequest",
                                "Cookie": clean_cookie,
                                "referer": "https://scratch.mit.edu/",
                                "user-agent": "Mozilla/5.0"
                            }
                            resp = requests.put(f"https://scratch.mit.edu/site-api/users/followers/{rm}/add/", headers=head)
                            if resp.status_code == 200 or resp.status_code == 204:
                                print("Успешно!")
                            else:
                                print("Произошла ошибка. Возможно, ты пытаешься подписаться на человека, профиль которого удалён")
    elif act == 5:
        ip = -1
        while ip != "0":
            print("Введи ip адрес. Введи 0 для выхода")
            ip = input(">> ")
            if ip != "0":
                resp = requests.get("https://scratch.mit.edu/ip_ban_appeal/" + ip + "/")
                if resp.status_code == 403:
                    print("IP адрес забанен!")
                elif resp.status_code == 200:
                    print("IP адрес не забанен")
                elif resp.status_code == 500:
                    print("Сервера Scratch упали!")
                else:
                    print("Произошла ошибка")
    elif act == 6:
        testpw = "-1"
        while testpw != "0":
            print("Введи пароль, который проверить: (0 - выйти)")
            testpw = input(">> ")
            if testpw != "0":
                data = requests.post("https://api.scratch.mit.edu/accounts/checkpassword", json={"password": testpw}).json()
                if data.get("msg") == "invalid password":
                    print("Пароль слишком лёгкий!")
                elif data.get("msg") == "valid password":
                    print("Пароль надёжный!")
                else:
                    print("Произошла ошибка")
    elif act == 7:
        id = -1
        while id != 0:
            print("Введите ссылку или ID на проект: (Введите 0 чтобы выйти)")
            id = int(re.findall(r'\d+', input(">> "))[0])
            if id != 0:
                resp = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={str(id)}&limit=40&offset=0")
                data = resp.json()
                if len(data) == 0:
                    print("В проекте нет изменений облачных переменных")
                else:
                    maxunlen = 3
                    maxvr = 8
                    maxact = 8
                    for obj in data:
                        if len(obj.get("user")) > maxunlen:
                            maxunlen = len(obj.get("user"))
                        if len(obj.get("name")) > maxvr:
                            maxvr = len(obj.get("name"))
                        if obj.get("verb") == "rename_var": #Задать Удалить Переименовать Создать
                            if maxact < 13:
                                maxact = 13
                    print(f'#   Имя{" " * (maxunlen - 3)} Название{" " * (maxvr - 8)} Действие{" " * (maxact - 8)} Значение')
                    for i in range(len(data)):
                        obj = data[i]
                        if obj.get("verb") == "set_var":
                            print(f'{addnums(i + 1)} {obj.get("user")}{" " * (maxunlen - len(obj.get("user")))} {obj.get("name")}{" " * (maxvr - len(obj.get("name")))} Задать{" " * (maxact - 6)} {valid(obj.get("value"))}')
                        elif obj.get("verb") == "create_var":
                            print(f'{addnums(i + 1)} {obj.get("user")}{" " * (maxunlen - len(obj.get("user")))} {obj.get("name")}{" " * (maxvr - len(obj.get("name")))} Создать{" " * (maxact - 7)} {valid(obj.get("value"))}')
                        elif obj.get("verb") == "del_var":
                            print(f'{addnums(i + 1)} {obj.get("user")}{" " * (maxunlen - len(obj.get("user")))} {obj.get("name")}{" " * (maxvr - len(obj.get("name")))} Удалить{" " * (maxact - 7)} {valid(obj.get("value"))}')
                        elif obj.get("verb") == "rename_var":
                            print(f'{addnums(i + 1)} {obj.get("user")}{" " * (maxunlen - len(obj.get("user")))} {obj.get("name")}{" " * (maxvr - len(obj.get("name")))} Переименовать{" " * (maxact - 13)} {valid(obj.get("value"))}')
                        else:
                            print(f'{addnums(i + 1)} {obj.get("user")}{" " * (maxunlen - len(obj.get("user")))} {obj.get("name")}{" " * (maxvr - len(obj.get("name")))} -{" " * (maxact - 1)} {valid(obj.get("value"))}')
                        
                        
                        
                        