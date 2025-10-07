import numpy as np
import math
import matplotlib.pyplot as plt
import io
from PIL import Image

def convert_to_grayscale(image_array, progress_callback=None):
    if len(image_array.shape) == 3:
        return np.dot(image_array[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)
    return image_array.copy()

def negative_image(image_array, progress_callback=None):
    return (255 - image_array).astype(np.uint8)

def apply_thresholding(image_array, threshold, progress_callback=None):
    if len(image_array.shape) == 3:
        gray_array = convert_to_grayscale(image_array)
    else:
        gray_array = image_array.copy()
    return np.where(gray_array > threshold, 255, 0).astype(np.uint8)

def resize_image(image_array, new_width, new_height, progress_callback=None):
    temp_image = Image.fromarray(image_array)
    resized_image = temp_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return np.array(resized_image)

def smooth_image(image_array, kernel_size, progress_callback=None):
    mean_filter = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
    smoothed_array = np.zeros_like(image_array, dtype=np.float64)
    padding = kernel_size // 2
    is_color = image_array.ndim == 3
    padded_array = np.pad(image_array, ((padding, padding), (padding, padding), (0, 0)) if is_color else padding, 'constant')

    if is_color:
        height, width, channels = image_array.shape
        for i in range(height):
            for j in range(width):
                for c in range(channels):
                    roi = padded_array[i : i + kernel_size, j : j + kernel_size, c]
                    smoothed_array[i, j, c] = np.sum(roi * mean_filter)
            if progress_callback:
                progress_callback((i + 1) / height * 100)
    else:
        height, width = image_array.shape
        for i in range(height):
            for j in range(width):
                roi = padded_array[i : i + kernel_size, j : j + kernel_size]
                smoothed_array[i, j] = np.sum(roi * mean_filter)
            if progress_callback:
                progress_callback((i + 1) / height * 100)
                
    return np.clip(smoothed_array, 0, 255).astype(np.uint8)

def sharpen_image(image_array, intensity, progress_callback=None):
    kernel = np.array([[-1, -1, -1], [-1,  9, -1], [-1, -1, -1]])
    source_array = image_array.astype(np.float32)
    sharpened_array = np.zeros_like(source_array, dtype=np.float64)
    is_color = source_array.ndim == 3
    
    if is_color:
        height, width, channels = source_array.shape
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                for c in range(channels):
                    roi = source_array[i-1:i+2, j-1:j+2, c]
                    new_pixel = np.sum(roi * kernel)
                    sharpened_array[i, j, c] = new_pixel * intensity + (1 - intensity) * source_array[i, j, c]
            if progress_callback:
                progress_callback(i / (height - 2) * 100)
    else:
        height, width = source_array.shape
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                roi = source_array[i-1:i+2, j-1:j+2]
                new_pixel = np.sum(roi * kernel)
                sharpened_array[i, j] = new_pixel * intensity + (1 - intensity) * source_array[i, j]
            if progress_callback:
                progress_callback(i / (height - 2) * 100)
                
    return np.clip(sharpened_array, 0, 255).astype(np.uint8)

def laplacian_edge(arr: np.ndarray, progress_callback=None) -> np.ndarray:
    gray = convert_to_grayscale(arr) if arr.ndim == 3 else arr.squeeze()
    
    ksize = 3
    pad = ksize // 2
    kernel = np.array([[1, 1, 1],
                       [1,-8, 1],
                       [1, 1, 1]], dtype=np.float32)

    padded = np.pad(gray, pad, mode="constant", constant_values=0)
    out = np.zeros_like(gray, dtype=np.float32)
    height = padded.shape[0]
    
    for i in range(pad, height - pad):
        for j in range(pad, padded.shape[1] - pad):
            region = padded[i - pad:i + pad + 1, j - pad:j + pad + 1]
            out[i - pad, j - pad] = np.sum(region * kernel)
        if progress_callback:
            progress_callback(i / (height - 2*pad) * 100)
            
    out = np.abs(out)
    out = (out / np.max(out) * 255) if np.max(out) > 0 else out
    return np.clip(out, 0, 255).astype(np.uint8)

def adjust_contrast(image_array, alpha, progress_callback=None):
    arr = image_array.astype(np.float32)
    adjusted = 128 + alpha * (arr - 128)
    return np.clip(adjusted, 0, 255).astype(np.uint8)

def log_transformation(image_array, progress_callback=None):
    max_val = float(np.max(image_array))
    c = 255 / np.log(1 + max_val) if max_val > 0 else 0
    log_array = c * (np.log(image_array.astype(np.float32) + 1))
    return np.clip(log_array, 0, 255).astype(np.uint8)

def log_transform_c1(image_array, progress_callback=None):
    gray_array = convert_to_grayscale(image_array) if image_array.ndim == 3 else image_array
    log_array = np.log10(1 + gray_array.astype(np.float32))
    c = 255 / np.log10(1 + 255)
    scaled_log_array = c * log_array
    return scaled_log_array.astype(np.uint8)

def show_histogram(image_array, progress_callback=None):
    gray_array = convert_to_grayscale(image_array) if len(image_array.shape) == 3 else image_array.copy()

    fig = plt.figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.hist(gray_array.ravel(), bins=256, range=(0, 256), color='black', alpha=0.7)
    ax.set_xlim(0, 255)
    ax.set_xlabel('Pixel Intensity')
    ax.set_ylabel('Frequency')
    ax.set_title('Image Histogram')
    ax.grid(True, alpha=0.3)
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plot_img = Image.open(buf)
    plot_data = np.array(plot_img.convert('RGB'))
    buf.close()
    plt.close(fig)
    
    return plot_data

def manual_rotate(image_array, angle_deg, progress_callback=None):
    angle_rad = np.deg2rad(angle_deg)
    h, w = image_array.shape[:2]
    cos_a, sin_a = np.abs(np.cos(angle_rad)), np.abs(np.sin(angle_rad))
    new_w, new_h = int(h * sin_a + w * cos_a), int(h * cos_a + w * sin_a)
    center_orig_x, center_orig_y = w // 2, h // 2
    center_new_x, center_new_y = new_w // 2, new_h // 2
    is_color = image_array.ndim == 3
    rotated_array = np.zeros((new_h, new_w, image_array.shape[2]) if is_color else (new_h, new_w), dtype=np.uint8)

    for y_new in range(new_h):
        for x_new in range(new_w):
            x_c, y_c = x_new - center_new_x, y_new - center_new_y
            x_orig = x_c * np.cos(angle_rad) + y_c * np.sin(angle_rad) + center_orig_x
            y_orig = -x_c * np.sin(angle_rad) + y_c * np.cos(angle_rad) + center_orig_y
            x, y = int(round(x_orig)), int(round(y_orig))
            if 0 <= x < w and 0 <= y < h:
                rotated_array[y_new, x_new] = image_array[y, x]
        if progress_callback:
            progress_callback((y_new + 1) / new_h * 100)

    return rotated_array