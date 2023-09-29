from pprint import pprint
import os

import requests
import tqdm
from dotenv import load_dotenv

load_dotenv()
YANDEX_TOKEN = os.getenv("YANDEX_TOKEN")
HEADERS = {
    "Authorization": f"OAuth {YANDEX_TOKEN}",
    "Content-Type": "gzip",
    # "Transfer-Encoding": "chunked"
}

DATA_GET = {
    "path": "notion_backups/export.zip"
}

href_for_upload = requests.get(url="https://cloud-api.yandex.net/v1/disk/resources/upload", headers=HEADERS,
                               params=DATA_GET)
href_for_upload = href_for_upload.json()
href_for_upload = href_for_upload.get("href")
print(href_for_upload)

upload = requests.put(url=href_for_upload, headers=HEADERS, data=open("notion_backups/export.zip", 'rb'))
# with open("notion_backups/export.zip", 'rb') as f:
#     r = requests.put(url=href_for_upload, data=tqdm(f.readlines()))

print(upload.content)
# response = requests.get(url="https://cloud-api.yandex.net/v1/disk/operations/a4bcf46354c31d9add3235ddb42e46b3dcf34be315b4fb3031909aef52baa76b", headers=HEADERS, )


# pprint(response)
