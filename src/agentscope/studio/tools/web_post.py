# -*- coding: utf-8 -*-
"""
Post for removing background from images using a web API.
"""

import os
from typing import Union, Tuple
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
import requests

from agentscope.message import Msg


def web_post(
    url: str,
    output_path: str = "",
    output_type: str = "image",
    msg: Msg = None,
    image_path_or_url: str = None,
    data: Union[str, dict] = None,
    **kwargs: dict,
) -> str:
    """
    Send an HTTP POST request, upload an image and process the response.

    :param url: URL to send the request to
    :param output_path: Path to save the output image
    :param output_type: Type of the output, can be "image" or "text" or
        "audio" or "video"
    :param msg: Msg object containing the image URL
    :param image_path_or_url: Local path or URL of the image
    :param data: Data to send, can be a string or a dictionary
    :param kwargs: Additional request parameters
    :return: Path to the saved output image
    """
    # Parse image source
    image_url, image_path = parse_image_source(msg, image_path_or_url)

    # Update the data or kwargs parameters
    if image_url:
        if isinstance(data, dict):
            data["image_url"] = image_url
    elif image_path:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        kwargs["files"] = {
            "image_file": (
                os.path.basename(image_path),
                image_data,
            ),
        }

    response = requests.post(url, data=data, **kwargs)
    return process_response(response, output_path, output_type)


def parse_image_source(msg: Msg, image_path_or_url: str) -> Tuple[str, str]:
    """
    Parse the image source from msg or image_path_or_url.

    :param msg: Msg object containing the image URL
    :param image_path_or_url: Local path or URL of the image
    :return: Tuple containing image_url and image_path
    """
    image_url = ""
    image_path = ""

    if msg and msg.url:
        image_url = msg.url
    if image_path_or_url:
        if is_url(image_path_or_url):
            image_url = image_path_or_url
        elif is_local_file(image_path_or_url):
            image_path = image_path_or_url

    return image_url, image_path


def process_response(
    response: requests.Response,
    output_path: str,
    output_type: str = "image",
) -> str:
    """
    Process the HTTP response and save the image if successful.

    :param response: HTTP response object
    :param output_path: Path to save the output image
    :param output_type: Type of the output, can be "image" or "text" or
        "audio" or "video"
    :return: Path to the saved output image
    """
    if response.status_code == requests.codes.ok:
        if output_type == "image":
            # Read the response content into a BytesIO object
            img = Image.open(BytesIO(response.content))

            # Display the image
            img.show()

            # Save the image
            if output_path:
                img.save(output_path)
    else:
        # Print the error message
        print("Error:", response.status_code, response.text)

    return output_path


def is_url(path: str) -> bool:
    """
    Check if the provided path is a URL.

    :param path: The path to be checked.
    :return: True if the path is a valid URL, False otherwise.
    """
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_local_file(path: str) -> bool:
    """
    Check if the provided path is a local file.

    :param path: The path to be checked.
    :return: True if the path exists and is a file, False otherwise.
    """
    return os.path.isfile(path)
