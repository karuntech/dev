import os
import cv2
import numpy as np

NUM_CATEGORIES = 3
data_dir = "gtsrb-small"
IMG_WIDTH = 30
IMG_HEIGHT = 30

images = []
labels = []

for category in range(0, NUM_CATEGORIES -1):
    dir = os.path.join(data_dir, str(category))
    for imgfile in os.listdir(dir):
        print(f"Processing image {imgfile}")
        img = cv2.imread(dir + os.sep + imgfile)
        resized_image = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
        print(f"Resized image size: {resized_image.shape}")
        img_ndarray = np.array(resized_image)
        images.append(img_ndarray)
        labels.append(category)

# print(f"Images list and Labels list: {images} | {labels}")