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
    image: np.ndarray, factor: float = 1.0, clip_range: Optional[Tuple[float, float]] = None, **kwargs: Any
) -> None:
    """Utility function for plotting RGB images."""
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])
    
    fig.savefig(os.path.join(cwd , "output", "out.png"),bbox_inches="tight")
    plt.close()
    
    