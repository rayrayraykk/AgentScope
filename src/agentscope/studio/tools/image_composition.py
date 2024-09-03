# -*- coding: utf-8 -*-
"""Image composition"""
from typing import List, Optional, Union
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import json5


def stitch_images_with_grid(
    image_paths: List[str],
    titles: Union[List[str], str],
    output_path: str,
    row: int = 1,
    column: int = 1,
    spacing: int = 10,
    title_height: int = 100,
    font_name: Optional[str] = None,
) -> str:
    """
    Stitch multiple images and titles into a single image, supporting
    custom grid layouts.
    Now supports image loading from URLs.

    Parameters:
    - image_paths: List of image file paths or URLs.
    - titles: List of titles corresponding to each image.
    - output_path: File path for the output image.
    - row: Number of rows in the grid.
    - column: Number of columns in the grid.
    - spacing: The size of the gap between images.
    - title_height: The height of the title area.
    - font_name: font_name for rendering the titles. If None, the default
    font is used.
    """

    if isinstance(titles, str):
        titles = json5.loads(titles)
    images = []
    for path in image_paths:
        if isinstance(path, str):
            img = Image.open(path)

        else:
            response = requests.get(path.url[0])
            img = Image.open(BytesIO(response.content))
        images.append(img)

    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths) + spacing
    max_height = max(heights) + title_height + spacing

    total_width = column * max_width
    total_height = row * max_height

    combined = Image.new(
        "RGB",
        (total_width, total_height),
        color="white",
    )
    draw = ImageDraw.Draw(combined)

    font_size = title_height // 2
    font = (
        ImageFont.load_default(size=font_size)
        if font_name is None
        else (ImageFont.truetype(font_name, font_size))
    )

    for idx, image in enumerate(images):
        row = idx // column
        col = idx % column
        x = col * max_width
        y = row * max_height + title_height
        title_x = x + spacing // 2  # Add some left padding to the title
        title_y = (
            row * (max_height + spacing) + (title_height - font_size) // 2
        )  # Vertically center the title
        draw.text((title_x, title_y), titles[idx], fill="black", font=font)

        combined.paste(image, (x, y))

    if output_path:
        combined.save(output_path)
    combined.show()

    return output_path
