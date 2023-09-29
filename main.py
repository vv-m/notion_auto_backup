"""
Выгрузка бэкап Notion в ЯндексДиск установленный на локальной машине.

1. ЯндексДиск:
https://disk.yandex.ru/client/disk/notion_backups

"""

import os

from loguru import logger as log
import yadisk
from dotenv import load_dotenv
from timeit import default_timer as timer
from datetime import timedelta

from telegram_sender import send_massage_to_admin_telegram

load_dotenv()

YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
PATH_BACKUPS_IN_YA_DISK = "notion_backups/"

# 1. Создаем бэкап в директории ЯндексДиск 'Yandex.Disk/notion_backups/'

start_time = timer()
os.system(f"backup_notion --output-dir='Yandex.Disk/notion_backups/' --space-id=e6edf439-211a-49fb-ac9d-8a91d00f7279")

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
    log.debug("Не удалось соединиться с ЯндексДиск")
    send_massage_to_admin_telegram("Notion-backups:\n\n"
                                   "❌ Не удалось соединиться с ЯндексДиск")
backups_on_disk = list(y.listdir("notion_backups"))

try:
    # - Определить сколько бэкапов на ЯндексДиск
    qty_backups = len(backups_on_disk)

    # - Если больше 30 бэкапов на ЯндексДиск то удалить самый старый
    if qty_backups > 30:
        list_files = []
        for backup in backups_on_disk:
            list_files.append({"name": backup.name, "created": backup.created})

        sorted_by_created_list = sorted(list_files, key=lambda d: d['created'])
        old_file_name = sorted_by_created_list[0]["name"]

        # Удаляем файл
        y.remove(f"{PATH_BACKUPS_IN_YA_DISK}{old_file_name}", permanently=True)
        send_massage_to_admin_telegram(f"Notion-backups:\n"
                                       f"✅ Успешный бэкап.\n"
                                       f"Бэкап создан за {time_for_backup}")
except Exception as e:
    send_massage_to_admin_telegram(f"Notion-backups:\n\n"
                                   f"❌ Не удалось выгрузить бэкап.\n\n"
                                   f"{str(e)}")
