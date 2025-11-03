
from typing import Optional, Tuple
import os
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False
import tkinter as tk
def load_image_for_tk(path: str, max_size: Tuple[int, int]) -> Optional[tk.PhotoImage]:
    if not path or not os.path.exists(path):
        return None
    try:
        if PIL_AVAILABLE:
            img = Image.open(path)
            try:
                resample = Image.Resampling.LANCZOS
            except Exception:
                resample = Image.LANCZOS
            img.thumbnail(max_size, resample)
            return ImageTk.PhotoImage(img)
        else:
            img = tk.PhotoImage(file=path)
            w, h = img.width(), img.height()
            if w <= 0 or h <= 0:
                return img
            fx = max(1, w // max(1, max_size[0]))
            fy = max(1, h // max(1, max_size[1]))
            if fx > 1 or fy > 1:
                img = img.subsample(fx, fy)
            return img
    except Exception:
        return None
