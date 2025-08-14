Данный репозиторий содержит программы для взаимодействия со Scratch API

# Установка
## Windows
1. Установим нужные утилиты:
   ```powershell
   winget install Git.Git
   ```
   [Питон](https://python.org) скачивайте с оффициального сайта! (я не помню название пакета в winget)
2. Скачиваем программы:
   ```powershell
   git clone https://github.com/polzovatel-5555/ScratchSystem.git
   ```
   .git необезательна но я советую её в конец дописать
3. Запускаем:
   ```powershell
   cd ScratchSystem
   pip install -r requirements.txt
   
   python "<название>.py"
   ```
   Если в названии есть пробелы, то ковычки обязательны!!
## Linux
1. Устанавливаем нужные утилиты:
   Дистрибутивы на базе Debian:
   ```bash
   sudo apt install git python-is-python3 python-pip
   ```
   ArchLinux:
   ```bash
   sudo pacman -Syy git python python-pip
   ```
2. Клонируем репозиторий:
   ```bash
   git clone https://github.com/polzovatel-5555/ScratchSystem.git
   ```
   .git необезательна но я советую её в конец дописать
3. Запускаем:
   ```bash
   cd ScratchSystem
   pip install -r requirements.txt

   python "<название>.py"
   # если python не работает, попробуйте python3
   python3 "<название>.py"
   ```
   Если в названии есть пробелы, то ковычки обязательны!!
