from transformers import AutoImageProcessor, ResNetModel
import torch
from PIL import Image
import glob
from tqdm import tqdm
import numpy as np

image_processor = AutoImageProcessor.from_pretrained("microsoft/resnet-18")
model = ResNetModel.from_pretrained("microsoft/resnet-18")

for f in tqdm(glob.glob("./icons/*.webp")):
    inputs = image_processor(
        Image.open(f),
        return_tensors="pt")
    with torch.no_grad():
        embedding = model(**inputs)["pooler_output"].flatten().detach().numpy()
        np.save(f"{f.replace('.webp', '.npy')}", embedding)
