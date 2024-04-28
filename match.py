import glob
import mss
import numpy as np
import requests
import torch
from PIL import Image
from pynput.keyboard import KeyCode
from pynput.mouse import Controller as MouseController
from tqdm import tqdm
from transformers import AutoImageProcessor, ResNetModel


def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def loading_market_info():


image_processor = AutoImageProcessor.from_pretrained("microsoft/resnet-18")
model = ResNetModel.from_pretrained("microsoft/resnet-18")

names = []
embeddings = []

for f in tqdm(glob.glob("./icons/*.npy")):
    names.append(f)
    embeddings.append(np.load(f))

embeddings = np.stack(embeddings, axis=0)

# 创建鼠标控制器实例
mouse = MouseController()


def capture_screen(left, top, width, height):
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img.show()
        inputs = image_processor(
            img,
            return_tensors="pt")
        with torch.no_grad():
            embedding = model(**inputs)["pooler_output"].flatten().detach().numpy()

        cosine_similarities = np.dot(embeddings, embedding) / (
                np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embedding))

        # 找到相似度最高的图片向量
        most_similar_index = np.argmax(cosine_similarities)
        Image.open(names[most_similar_index].replace(".npy", ".webp")).show()


from pynput import keyboard


def on_press(key):
    if type(key) is KeyCode and key.char == '`':
        current_position = mouse.position
        left = int(current_position[0]) - 25
        top = int(current_position[1]) - 25
        width, height = 50, 50
        capture_screen(left, top, width, height)


with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()
