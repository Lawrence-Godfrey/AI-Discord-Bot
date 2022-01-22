import requests
import io
import numpy as np
import logging
import cv2

from PIL import Image
from discord.ext import commands
from tensorflow import keras
from tensorflow.keras.applications.efficientnet import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.image import resize
from PIL import Image


def get_image_from_url(url: str, headers: dict, timeout: int = 3, retries: int = 4) -> bytes:
    data = None

    timeout_exception = True
    timeout_count = 1
    while timeout_exception:
        try:
            data = requests.get(url, headers=headers, timeout=timeout).content
        except requests.Timeout:
            if timeout_count > retries:
                raise commands.CommandError("Timed out too many times. Try again later.")

            timeout_count += 1
            timeout_exception = True

            logging.debug(
                f'Timed out for the while downloading image from thispersondoesnotexist.com (attempt {timeout_count}), trying again...'
            )

            continue

        timeout_exception = False

    return data

def get_image_from_file(filename):
    img = image.load_img(filename, target_size=(528, 528))
    img = image.img_to_array(img)

    return img

def get_image_from_bytes(bytes):
    img = np.array(Image.open(io.BytesIO(bytes)))

    return img

def default_preprocessing(img, target_size=(528, 528)):
    """
    Does default preprocessing on an image, including:
     - Converting from 4-channel to 3-channel (RGBA to RGB).
     - Resizing to 528x528.

    Returns:
        A numpy array of shape (1, target_size[0], target_size[1], 3).
    """

    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    img = resize(img, target_size, antialias=True)

    return img