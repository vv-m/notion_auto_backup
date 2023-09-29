"""
Выгрузка бэкап Notion в ЯндексДиск установленный на локальной машине.

1. ЯндексДиск:
https://disk.yandex.ru/client/disk/notion_backups

"""

import os

from loguru import logger as log
import yadisk
from dotenv import load_dotenv
import glob

from telegram_sender import send_massage_to_admin_telegram

load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
path_to_upload = "notion_backups/"

# 1. Создаем бэкап на локальной машине
os.system("backup_notion --output-dir='Yandex.Disk/notion_backups/' --space-id=e6edf439-211a-49fb-ac9d-8a91d00f7279")

path_downloaded_backup = glob.glob("notion_backups/*.zip")
path_downloaded_backup = path_downloaded_backup[0]

# Соединение с ЯндексДиск
y = yadisk.YaDisk(token=YANDEX_TOKEN)

# Проверяем токен ЯндексДиска
connect_yandex = y.check_token()
if connect_yandex:
    log.debug("Успешное соединение с ЯндексДиск")
else:
    log.debug("Не удалось соединиться с ЯндексДиск")
    send_massage_to_admin_telegram("Notion-backups:\n\n"
                                   "❌ Не удалось соединиться с ЯндексДиск")
backups_on_disk = list(y.listdir("notion_backups"))

try:
    # 2. Определить сколько бэкапов на ЯндексДиск
    qty_backups = len(backups_on_disk)

    # 3. Если больше 30 бэкапов на ЯндексДиск то удалить самый старый
    if qty_backups > 30:
        list_files = []
        for backup in backups_on_disk:
            list_files.append({"name": backup.name, "created": backup.created})

        sorted_by_created_list = sorted(list_files, key=lambda d: d['created'])
        old_file_name = sorted_by_created_list[0]["name"]

        # Удаляем файл
        y.remove(f"{path_to_upload}{old_file_name}", permanently=True)

    # 4. Загружаем новый бэкап на ЯндексДиск
    # (локальная и удаленная папки называются одинаково - поэтому и параметры олинаковые)
    log.debug("Начинаю загрузку на ЯндексДиск.")
    y.upload(path_downloaded_backup, path_downloaded_backup, timeout=(15, 250))
    log.debug("Закончил загрузку на ЯндексДиск.")

    log.debug(f"Успешная выгрузка бэкапа для Notion - {path_downloaded_backup}")
    send_massage_to_admin_telegram(f"Notion-backups:\n\n"
                                   f"✅ Файл '{path_downloaded_backup.split('/')[-1]}' был "
                                   f"успешно загружен на ЯндексДиск.\n\n"
                                   f"Ссылка на бэкапы:"
                                   f"https://disk.yandex.ru/client/disk/notion_backups"
                                   )
    # 5. Удаляем бэкап с локалки
    os.remove(path_downloaded_backup)
    print('Ok')
except Exception as e:
    send_massage_to_admin_telegram(f"Notion-backups:\n\n"
                                   f"❌ Не удалось выгрузить бэкап.\n\n"
                                   f"{str(e)}")
