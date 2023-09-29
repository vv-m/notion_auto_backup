"""
Выгрузка бэкап Notion в ЯндексДиск установленный на локальной машине.

1. ЯндексДиск:
https://disk.yandex.ru/client/disk/notion_backups

2. Что бы использовать backup_service.main в коде пришлось в библиотеке notion_backup/backup_service.py
закомментировать 3 строчки.
"""

import os
import sys

from loguru import logger as log
import yadisk
from dotenv import load_dotenv
from timeit import default_timer as timer
from datetime import timedelta

from telegram_sender import send_massage_to_admin_telegram
from notion_backup import backup_service
load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
PATH_BACKUPS_IN_YA_DISK = "notion_backups/"

# 1. Создаем бэкап в директории ЯндексДиск 'Yandex.Disk/notion_backups/'
# - Меняем текущий путь os для того что бы можно было указать верный путь для команды backup_notion
os.chdir("/home/vlad")
# os.chdir("/Users/vladmironov2")

start_time = timer()
try:
    message_start = (f"Notion-backups:\n\n"
                     f"🎬 Начинаю загрузку бэкапа.\n\n")
    log.debug(message_start)
    send_massage_to_admin_telegram(message_start)
    backup_service.main(output_dir="Yandex.Disk/notion_backups", space_id="e6edf439-211a-49fb-ac9d-8a91d00f7279")
except Exception as e:
    message_exception = (f"Notion-backups:\n\n"
                         f"❌ Не удалось выгрузить бэкап.\n\n"
                         f"{str(e)}")
    log.debug(message_exception)
    send_massage_to_admin_telegram(message_exception)
    sys.exit()

end_time = timer()
time_for_backup = str(timedelta(seconds=end_time - start_time))

# - Время за которое получили бэкап
time_for_backup = time_for_backup[:7]

# 2. Удаление лишнего бэкап с ЯндексДиск, если их больше 30

# - Соединение с ЯндексДиск
y = yadisk.YaDisk(token=YANDEX_TOKEN)

# - Проверяем токен ЯндексДиска
CONNECT_YANDEX = y.check_token()

if CONNECT_YANDEX:
    log.debug("Успешное соединение с ЯндексДиск")
else:
    message_connect_success = ("Notion-backups:\n\n"
                               "❌ Не удалось соединиться с ЯндексДиск")
    log.debug(message_connect_success)
    send_massage_to_admin_telegram(message_connect_success)

backups_on_disk = list(y.listdir("notion_backups"))

try:
    # - Определить сколько бэкапов на ЯндексДиск
    qty_backups = len(backups_on_disk)
    message_remove = ''
    # - Если больше 30 бэкапов на ЯндексДиск то удалить самый старый
    if qty_backups > 30:
        list_files = []
        for backup in backups_on_disk:
            list_files.append({"name": backup.name, "created": backup.created})

        sorted_by_created_list = sorted(list_files, key=lambda d: d['created'])
        old_file_name = sorted_by_created_list[0]["name"]

        # Удаляем файл
        y.remove(f"{PATH_BACKUPS_IN_YA_DISK}{old_file_name}", permanently=True)
        message_remove = f"Удален старый бэкап {old_file_name}"
        log.debug(message_remove)

    message_success = (f"Notion-backups:\n"
                       f"✅ Успешный бэкап.\n"
                       f"Бэкап создан за {time_for_backup}\n"
                       f"Кол-во бэкапов: {qty_backups}"
                       f"{message_remove}")
    log.debug(message_success)
    send_massage_to_admin_telegram(message_success)

except Exception as e:
    message_exception = (f"Notion-backups:\n\n"
                         f"❌ Не удалось выгрузить бэкап.\n\n"
                         f"{str(e)}")
    log.debug(message_exception)
    send_massage_to_admin_telegram(message_exception)
