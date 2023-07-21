"""
Utilities used by example notebooks
https://github.com/sentinel-hub/sentinelhub-py/blob/master/examples/utils.py

"""
from typing import Any, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
cwd = Path(__file__).parent.parent
import os


def plot_image(
    image: np.ndarray, 
    factor: float = 1.0, 
    clip_range: Optional[Tuple[float, float]] = None,
    save_name: str = "sample.png",
    **kwargs: Any
) -> None:
    """Utility function for plotting RGB images."""
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])
    
    fig.savefig(os.path.join(cwd , "output", save_name),bbox_inches="tight")
    plt.close()

# def plot_image(image, factor=1):
#     """
#     Utility function for plotting RGB images.
#     """
#     plt.subplots(nrows=1, ncols=1, figsize=(15, 7))

#     if np.issubdtype(image.dtype, np.floating):
#         plt.imshow(np.minimum(image * factor, 1))
#     else:
#         plt.imshow(image)


def plot_images_2x2(images,unique_acquisitions) -> None:
    
    if len(images)>4:
        images  = images[:4]
        unique_acquisitions = unique_acquisitions[:4]
    
    """Utility function for plotting RGB images."""
    ncols, nrows = 2, 2

    fig, axis = plt.subplots(
        ncols=ncols, nrows=nrows, figsize=(15, 10), subplot_kw={"xticks": [], "yticks": [], "frame_on": False}
    )
    for idx, (image, timestamp) in enumerate(zip(images, unique_acquisitions)):
        ax = axis[idx // ncols][idx % ncols]
        ax.imshow(np.clip(image * 2.5 / 255, 0, 1))
        ax.set_title(timestamp.date().isoformat(), fontsize=10)

    fig.savefig(os.path.join(cwd , "output", "out_2x2.png"),bbox_inches="tight")
    plt.close()
    return None
    
    