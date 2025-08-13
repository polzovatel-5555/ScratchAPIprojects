import requests
import json
print("Хочешь прикол? Введи имя любого скретчера, а я дам его ОС и браузер")
while True:
    scratcher = input(">> ")
    r1 = requests.get(f"https://api.scratch.mit.edu/users/{scratcher}/projects")
    if r1.status_code == 200:
        if r1.text == "[]":
            print("Увы, у него нет проектов :(\nБез проектов вычислить его нельзя")
        else:
            j1 = r1.json()
            r2 = requests.get(f"https://api.scratch.mit.edu/projects/{j1[0].get('id')}")
            if r2.status_code == 200:
                j2 = r2.json()
                r3 = requests.get(f"https://projects.scratch.mit.edu/{j1[0].get('id')}?token={j2.get('project_token')}")
                if r3.status_code == 200:
                    m = json.loads(r3.text)
                    #print(r3.text)
                    print(m.get("meta").get("agent"))
                else:
                    print("Ошибка :(")
            else:
                print("Ошибка :(")
    else:
        print("Ошибка :(")
    print("Введи имя другого скретчера")