import os
from box.exceptions import BoxValueError
import yaml
from chickenDiseaseClassifier import logger
import json
import joblib
from ensure import ensure_annotations 
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64



@ensure_annotations # Decorator that enforces type hints on the function's arguments.
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Function Description: Reads a YAML file and performs the following tasks:

    Arguments:
    path_to_yaml (string): A path-like input.
    
    Exceptions Raised:
    ValueError: If the YAML file is empty.
    e: Represents an empty file.
    
    Return Value:
    ConfigBox: A type of object called ConfigBox.
    """
    # We use ConfigBox to make it easier for us to access values using keys.
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Create a list of directories based on the provided input arguments:

    Input Arguments:
    path_to_directories (list): A list of directory paths.
    ignore_log (boolean, optional): An optional boolean flag to ignore creating multiple directories (default is set to False).
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save data in JSON format to a specified file.

    Arguments:
    path (Path): The path to the JSON file.
    data (dict): The data to be saved in the JSON file.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load data from a JSON file and convert it into class attributes.

    Arguments:
    path (Path): The path to the JSON file.

    Returns:
    ConfigBox: Data represented as class attributes instead of a dictionary.
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save binary data to a file.

    Arguments:
    data (Any): Data to be saved in binary format.
    path (Path): Path to the binary file.
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load binary data from a file.

    Arguments:
    path (Path): Path to the binary file.

    Returns:
    Any: The object stored in the file.
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Calculate the size of a file in kilobytes (KB).

    Arguments:
    path (Path): The file's path.

    Returns:
    str: The size in kilobytes (KB).
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


def decodeImage(imgstring, fileName):
    """
    Decode a base64-encoded image string and save it to a file.

    Args:
        imgstring (str): The base64-encoded image string.
        fileName (str): The name of the file to save the image to.

    Returns:
        None
    """
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    """
    Encode an image from a file into base64 format.

    Args:
        croppedImagePath (str): The path to the image file to be encoded.

    Returns:
        str: The base64-encoded image string.
    """
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())