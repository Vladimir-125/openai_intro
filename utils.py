import requests
from pathlib import Path
import hashlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from typing import List
from io import BytesIO
from PIL import Image

def download_image(url:str, data_folder=Path("data"), filename:str='')->str:
    """ Downloads an image from a url and saves it to a folder

    Args:
        url (str): Image url
        data_folder (Path, optional): Folder to store the image. Defaults to Path("data").
        filename (str, optional): New file name. Defaults to ''.

    Returns:
        str: Path to the image
    """  
    try:
        data_folder.mkdir(parents=True, exist_ok=True)
        response = requests.get(url)
        if not filename:
            filename = hashlib.sha1(response.content).hexdigest()
        open(data_folder / f"{filename}.png", "wb").write(response.content)
        return (data_folder / f"{filename}.png").as_posix()
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


def plot_images(images: List[str])->None:
    """ Plots a list of images in a row

    Args:
        images (List[str]): List of image paths
    """    
    fig, ax = plt.subplots(1,len(images))
    for i, image in enumerate(images):
        image = mpimg.imread(image)
        ax[i].imshow(image)
        ax[i].axis("off")   # turns off axes


def load_image_as_bytes(image_path: str, image_size:type=(256, 256))->BytesIO:
    """ Loads an image from disk and converts it to a BytesIO object

    Args:
        image_path (str): Path to the image
        image_size (type, optional): Resize image dimensions (width, height). Defaults to (256, 256).

    Returns:
        BytesIO: Image as a BytesIO object
    """    
    # Read the image file from disk and resize it
    image = Image.open(image_path)
    image = image.resize(image_size)

    # Convert the image to a BytesIO object
    byte_stream = BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()
    return byte_array


def get_answer(response:dict)->None:
    """ Prints the answer from the response

    Args:
        response (dict): Response from the API
    """    
    for index, ans in enumerate(response['choices']):
        print(f"Answer {index+1}:")
        print(ans['text'])