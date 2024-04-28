import glob
import mss
import numpy as np
import requests
import torch
from PIL import Image
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Controller as MouseController, Button
from tqdm import tqdm
from transformers import AutoImageProcessor, ResNetModel


def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


# def loading_market_info():


image_processor = AutoImageProcessor.from_pretrained("./resnet-18")
model = ResNetModel.from_pretrained("./resnet-18")

names = []
embeddings = []

for f in tqdm(glob.glob("./icons/*.npy")):
    names.append(f)
    embeddings.append(np.load(f))

embeddings = np.stack(embeddings, axis=0)

from pynput import keyboard, mouse

first = None
second = None

listen = False


def do(point1, point2):
    try:
        left, right, top, bottom = point1[0], point2[0], point1[1], point2[1]
        with mss.mss() as sct:
            monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
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
    except Exception as e:
        print(e)


def on_press(key):
    global listen, first, second
    # if type(key) is KeyCode and key.char == 'f2':
    if type(key) is Key and key.name == 'menu':
        first, second = None, None
        listen = False if listen else True


def on_click(x, y, button, pressed):
    global listen, first, second
    if listen and button == Button.left and pressed is True:
        if first is None:
            first = (x, y)
        else:
            second = (x, y)
            do(first, second)
            first, second = None, None


listener1 = keyboard.Listener(on_press=on_press)
listener2 = mouse.Listener(on_click=on_click)
listener1.start()
listener2.start()
listener1.join()
listener2.join()
