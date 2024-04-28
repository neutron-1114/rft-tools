import requests
import os
from tqdm import tqdm

from utils import download_file_with_progress





new_query = """
{
    items {
        id
        name
        types 
        avg24hPrice
        basePrice
        width
        height
        changeLast48hPercent
        iconLink
        link
    }
}
"""

result = run_query(new_query)

items = result["data"]["items"]

icons = []

for item in items:
    icon_url = item["iconLink"]
    file_name = icon_url.split("/")[-1]
    file_path = f"./icons/{file_name}"
    if not os.path.exists(file_path):
        download_file_with_progress(icon_url, file_path)
