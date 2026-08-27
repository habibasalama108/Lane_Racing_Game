import os
import shutil
import random
from ultralytics import YOLO


if not os.path.exists("dataset"):
    os.mkdir("dataset")
if not os.path.exists("dataset/images"):
    os.mkdir("dataset/images")
if not os.path.exists("dataset/images/train"):
    os.mkdir("dataset/images/train")
if not os.path.exists("dataset/images/val"):
    os.mkdir("dataset/images/val")
if not os.path.exists("dataset/labels"):
    os.mkdir("dataset/labels")
if not os.path.exists("dataset/labels/train"):
    os.mkdir("dataset/labels/train")
if not os.path.exists("dataset/labels/val"):
    os.mkdir("dataset/labels/val")


all_files = os.listdir("raw_images")
image_files = []
for file in all_files:
    if file.endswith(".jpg"):
        image_files.append(file)

random.shuffle(image_files)

total_images = len(image_files)
split_index = int(total_images * 0.8)

train_images = image_files[:split_index]
val_images = image_files[split_index:]


for img in train_images:
    txt_name = img.replace(".jpg", ".txt")

    img_source = "raw_images/" + img
    img_dest = "dataset/images/train/" + img
    shutil.copy(img_source, img_dest)

    txt_source = "raw_labels/" + txt_name
    txt_dest = "dataset/labels/train/" + txt_name
    if os.path.exists(txt_source) == True:
        shutil.copy(txt_source, txt_dest)

for img in val_images:
    txt_name = img.replace(".jpg", ".txt")

    img_source = "raw_images/" + img
    img_dest = "dataset/images/val/" + img
    shutil.copy(img_source, img_dest)

    txt_source = "raw_labels/" + txt_name
    txt_dest = "dataset/labels/val/" + txt_name
    if os.path.exists(txt_source) == True:
        shutil.copy(txt_source, txt_dest)


yaml_file = open("data.yaml", "w")
yaml_file.write("path: " + os.path.abspath("dataset") + "\n")
yaml_file.write("train: images/train\n")
yaml_file.write("val: images/val\n\n")
yaml_file.write("names:\n")
yaml_file.write("  0: steer\n")
yaml_file.write("  1: kachow\n")
yaml_file.close()

print("Folders ready. Starting training...")

model = YOLO("yolov8n.pt")
model.train(data="data.yaml", epochs=25, imgsz=640)