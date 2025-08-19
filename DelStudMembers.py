import requests
import re
from http.cookies import SimpleCookie
from datetime import datetime, timedelta, UTC
def cookie_to_string(cookie):
    c = SimpleCookie()
    c[cookie.name] = cookie.value
    morsel = c[cookie.name]
    if getattr(cookie, 'domain', None):
        morsel['domain'] = cookie.domain
    if getattr(cookie, 'path', None):
        morsel['path'] = cookie.path
    if getattr(cookie, 'secure', None):
        morsel['secure'] = True
    if getattr(cookie, 'httponly', None):
        morsel['httponly'] = True
    if hasattr(cookie, 'expires'):
        expires_date = datetime.now(UTC) + timedelta(weeks=2)
        morsel['expires'] = expires_date.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
    if isinstance(getattr(cookie, 'expires', None), int):
        morsel['Max-Age'] = cookie.expires
    return morsel.OutputString()
def login(username, password):
    session = requests.Session()
    session.get("https://scratch.mit.edu/csrf_token/")
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
        cookies = respo.cookies
        for cook in cookies:
            if cook.name == 'scratchsessionsid':
                cookie_string = cookie_to_string(cook)
        match = re.search(r'([^=]+)="\\"([^"]+)\\""', cookie_string)
        if match:
            cookie_name = match.group(1)
            cookie_value = match.group(2)
            clean_cookie = f'{cookie_name}="{cookie_value}"'
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
        }
        resp = requests.get("https://scratch.mit.edu/session/", headers=head)
        lol = resp.json()
        return {"success": True, "cookie": head, "token": lol["user"]["token"], "username": lol["user"]["username"], "isbanned": lol["user"]["banned"]}
    else:
        data = respo.json()
        return {"success": False, "msg": data[0].get("msg")}
def promote(studio, username, cookie):
    req = requests.put(f"https://scratch.mit.edu/site-api/users/curators-in/{str(studio)}/promote/?usernames={username}", headers=cookie)
    return req.status_code
def removeuser(studio, user, cookie):
    resp = requests.put(f"https://scratch.mit.edu/site-api/users/curators-in/{str(studio)}/remove/?usernames={user}", headers=cookie)
    return resp.status_code
#------------------------------------------------# https://scratch.mit.edu/site-api/users/curators-in/50774852/invite_curator/?usernames=a
def invite(studio, user, cookie):
    resp = requests.put(f"https://scratch.mit.edu/site-api/users/curators-in/{str(studio)}/invite_curator/?usernames={user}", headers=cookie)
    if resp.status_code == 200:
        j = resp.json()
        if j["status"] == "success":
            return {"success": True, "data": "Успешно!"}
        elif j["status"] == "error":
            return {"success": True, "data": f"{user} уже есть в приглашённых/кураторах/менеджерах"}
        else:
            return {"success": True, "data": f"Произошла неизвестная ошибка. Попробуй ещё раз!"}
    else:
        return {"success": False, "status": resp.status_code}
def acceptinvite(studio, cookie, username):
    resp = requests.put(f"https://scratch.mit.edu/site-api/users/curators-in/{str(studio)}/add/?usernames={username}", headers=cookie)
    return resp.status_code == 200
def closeprojects(cookie, studio):
    resp = requests.put(f"https://scratch.mit.edu/site-api/galleries/{str(studio)}/mark/closed/", headers=cookie)
    return resp.status_code == 200
def openprojects(cookie, studio):
    resp = requests.put(f"https://scratch.mit.edu/site-api/galleries/{str(studio)}/mark/open/", headers=cookie)
    return resp.status_code == 200
def addproject(token, studio, project):
    r = requests.post(f"https://api.scratch.mit.edu/studios/{str(studio)}/project/{str(project)}/", headers={"X-Token": token})
    return r.status_code
def removeproject(token, studio, project):
    r = requests.delete(f"https://api.scratch.mit.edu/studios/{str(studio)}/project/{str(project)}/", headers={"X-Token": token})
    return r.status_code
print("Добро пожаловать в систему управления удалёнными студиями 1.0!")
isworking = True
mustlogin = True
mustchoosestudio = True
logstatus = 1
while isworking:
    if mustlogin:
        if logstatus == 1:
            print("=== Войди в аккаунт ===")
        elif logstatus == 2:
            print("=== Сменить аккаунт ===")
        logstatus = 0
        print("Введи имя пользователя:")
        username = input(">> ")
        print("Введи пароль:")
        password = input(">> ")
        account = login(username, password)
        if account["success"]:
            if account["isbanned"]:
                print("Аккаунт забанен! Такой не подойдёт!")
            else:
                mustlogin = False
        else:
            print(account["msg"])
    elif mustchoosestudio:
        print("=== Выбрать студию ===")
        print("Введи ссылку или ID студии:")
        studio = int(re.findall(r'\d+', input(">> "))[0])
        mustchoosestudio = False
    else:
        loop = True
        print("=== Выбрать действие ===\n1. Повысить куратора\n2. Удалить куратора/менеджера\n3. Пригласить куратора\n4. Принять приглашение\n------------------------\n5. Добавить проект\n6. Удалить проект\n------------------------\n7. Включить добавление проектов\n8. Выключить добавление проектов\n------------------------\n9. Сменить аккаунт\n0. Сменить студию\n------------------------")
        while loop:
            choose = int(input(">> "))
            if choose == 1:
                print("Введи имя того, кого повысить:")
                person = input(">> ")
                status = promote(studio, person, account["cookie"])
                if status == 200:
                    print("Успешно!")
                elif status == 403:
                    print("Недостаточно прав (403)")
                elif status == 404:
                    print("Куратор не найден (404)")
                else:
                    print(f"Ошибка {status}")
            elif choose == 2:
                print("Введи имя того, кого удалить:")
                person = input(">> ")
                status = removeuser(studio, person, account["cookie"])
                if status == 200:
                    print("Успешно!")
                elif status == 403:
                    print("Недостаточно прав (403)")
                elif status == 404:
                    print("Куратор/менеджер не найден (404)")
                else:
                    print(f"Ошибка {status}")
            elif choose == 3:
                print("Введи имя того, кого пригласить:")
                person = input(">> ")
                status = invite(studio, person, account["cookie"])
                if status["success"]:
                    print(status["data"])
                elif status["status"] == 403:
                    print("Недостаточно прав (403)")
                elif status["status"] == 404:
                    print("Такое имя не найдено! (404)")
                else:
                    print(f"Ошибка {status}")
            elif choose == 4:
                if acceptinvite(studio, account["cookie"], account["username"]):
                    print("Успешно!")
                else:
                    print("Произошла ошибка. Возможно, приглашения нету")
            elif choose == 5:
                print("Введи ссылку или ID проекта:")
                project = int(re.findall(r'\d+', input(">> "))[0])
                if addproject(account["token"], studio, project):
                    print("Успешно!")
                else:
                    print("Произошла ошибка")
            elif choose == 6:
                print("Введи ссылку или ID проекта:")
                project = int(re.findall(r'\d+', input(">> "))[0])
                if removeproject(account["token"], studio, project):
                    print("Успешно!")
                else:
                    print("Произошла ошибка")
            elif choose == 7:
                if openprojects(account["cookie"], studio):
                    print("Успешно!")
                else:
                    print("Произошла ошибка")
            elif choose == 8:
                if closeprojects(account["cookie"], studio):
                    print("Успешно!")
                else:
                    print("Произошла ошибка")
            elif choose == 9:
                logstatus = 2
                mustlogin = True
                loop = False
            elif choose == 0:
                mustchoosestudio = True
                loop = False
            print("------------------------")
