import numpy as np
import logging

from typing import Union
from tensorflow import keras
from tensorflow.keras.applications.efficientnet import decode_predictions, preprocess_input
from pathlib import Path
from lib.utils import is_url, DEFAULT_BROWSER_HEADERS
from lib.image.utils import get_image_from_url, get_image_from_file, get_image_from_bytes, default_preprocessing


def get_classifier():
    """
    Returns the classifier model. This prediction class uses the EfficientNetB6 model.
    If the model can't be found on disk it will be downloaded.

    Returns:
        A `keras.Model` instance.
    """

    return keras.applications.EfficientNetB6(input_shape=(528, 528, 3), include_top=True, weights='imagenet')


def predict_image(src: Union[bytes, str]) -> np.ndarray:
    """
    Makes a prediction on an image.

    Args:
        src: Either a `bytes` objects containing the image data or a `str` containing a URL or a file path. ]

    Returns:
        A `np.ndarray` containing the predictions.
    """

    classifier = get_classifier()

    if type(src) is bytes:
        img = get_image_from_bytes(src)
    elif is_url(src):
        img = get_image_from_url(src, headers=DEFAULT_BROWSER_HEADERS)
    elif Path(src).exists():       # This determines if the string input is a valid path
        if Path(src).is_file():
            img = get_image_from_file(src)
        elif Path(src).is_dir():
            raise AttributeError('Input is a directory')
        else:
            raise AttributeError('Input is not a file or directory')
    else:
        raise AttributeError('No Argument specified')

    prediction = classifier.predict(img)
    return prediction


def pretty_print_prediction(prediction: np.ndarray) -> str:
    predictions = decode_predictions(prediction, top=5)[0]
    predictions_str = 'Predictions:\n'
    logging.debug('Predictions: %s', predictions)
    for p in predictions:
        str += f'\t{p[1]}: {p[2] * 100:.2f}%\n'

    return predictions_str
