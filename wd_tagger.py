import numpy as np
import onnxruntime as rt
import pandas as pd
from PIL import Image

# Model and config file paths
MODEL_PATH = "C:\\Users\\Drac\\Downloads\\wd tagger eva02_ConvNext v3\\wdEva02LargeTaggerV3.onnx"
LABEL_PATH = "C:\\Users\\Drac\\Downloads\\wd tagger eva02_ConvNext v3\\selected_tags.csv"


def load_labels(csv_path):
    tags_df = pd.read_csv(csv_path)
    tag_names = tags_df["name"].tolist()

    rating_indexes = list(np.where(tags_df["category"] == 9)[0])
    general_indexes = list(np.where(tags_df["category"] == 0)[0])
    character_indexes = list(np.where(tags_df["category"] == 4)[0])

    return tag_names, rating_indexes, general_indexes, character_indexes


def prepare_image(image, target_size):
    # Pad image to square and resize
    max_dim = max(image.size)
    padded_image = Image.new("RGB", (max_dim, max_dim), (255, 255, 255))
    pad_left = (max_dim - image.size[0]) // 2
    pad_top = (max_dim - image.size[1]) // 2
    padded_image.paste(image, (pad_left, pad_top))
    padded_image = padded_image.resize((target_size, target_size), Image.BICUBIC)

    # Convert to numpy array and change RGB to BGR
    image_array = np.asarray(padded_image, dtype=np.float32)[:, :, ::-1]
    return np.expand_dims(image_array, axis=0)


def predictsimple(image):
    tag_names, rating_indexes, general_indexes, character_indexes = load_labels(LABEL_PATH)

    general_res, character_res = predict(
        image, rt.InferenceSession(MODEL_PATH), tag_names, general_indexes, character_indexes
    )

    return general_res, character_res


# TODO: add rating
def predict(image, model, tag_names, general_indexes, character_indexes, general_thresh=0.3, character_thresh=0.8):
    image = prepare_image(image, model.get_inputs()[0].shape[1])
    preds = model.run([model.get_outputs()[0].name], {model.get_inputs()[0].name: image})[0]

    labels = list(zip(tag_names, preds[0].astype(float)))

    # Separate and filter labels based on thresholds
    general_res = [
        (tag, prob) for i, (tag, prob) in enumerate(labels) if prob > general_thresh and i in general_indexes
    ]
    character_res = [
        (tag, prob) for i, (tag, prob) in enumerate(labels) if prob > character_thresh and i in character_indexes
    ]

    # Sort the results by probability in descending order
    general_res = sorted(general_res, key=lambda x: x[1], reverse=True)
    character_res = sorted(character_res, key=lambda x: x[1], reverse=True)

    return general_res, character_res  # rating
