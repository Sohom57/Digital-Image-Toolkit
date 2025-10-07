# Digital Image Processing Toolkit

A desktop application built with Python and Tkinter for performing various digital image processing operations. It features a redesigned, user-friendly tabbed interface, allowing for a clean workflow and the ability to chain multiple effects.



## ✨ Features

The toolkit provides a rich set of functionalities for image manipulation and analysis.

#### **Image Operations**
* **Basic Adjustments**: Convert to Grayscale, Image Negation, Binary Thresholding.
* **Tonal Adjustments**: Adjust Contrast, apply Scaled & Fixed Logarithmic Transformations.
* **Filtering**: Image Smoothing (Box Blur) and Sharpening.
* **Analysis**: Edge Detection (Laplacian) and Histogram Visualization.

#### **Geometric Transformations**
* **Resize**: Scale images to custom dimensions (width and height).
* **Rotate**: Rotate images by any specified degree.

#### **Workflow & UI**
* **Chain Operations**: Apply effects sequentially to either the original image or the already enhanced image.
* **Reset Functionality**: Instantly revert the enhanced image back to the original at any time.
* **Interactive Viewer**: Zoom in and out with the mouse wheel and **Pan/Drag** the zoomed image by clicking and dragging.
* **Progress Bar**: Provides visual feedback during time-consuming operations like smoothing or rotation.
* **Modern UI**: A clean, tabbed layout keeps controls organized and maximizes space for image viewing.
* **File Handling**: Select and save images in common formats (`.png`, `.jpg`).

## 📂 Project Structure

The project is organized into a modular structure for better maintainability and scalability.

```
digital-image-toolkit/
├── assets/
│   └── my_photo.png
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── processing/
│   ├── __init__.py
│   └── operations.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── main.py
├── README.md
└── requirements.txt
```

-   **`main.py`**: The main entry point to launch the application.
-   **`gui/main_window.py`**: Defines the entire Tkinter-based user interface and event handling.
-   **`processing/operations.py`**: Contains all the core functions for image manipulation.
-   **`utils/helpers.py`**: Includes helper functions used across the application.
-   **`assets/`**: Stores static assets like images.

## 🛠️ Setup and Installation

Follow these steps to run the application on your local machine.

### **Prerequisites**
-   Python 3.6+
-   pip (Python package installer)

### **Installation**

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/Sohom57/Digital-Image-Toolkit.git](https://github.com/Sohom57/Digital-Image-Toolkit.git)
    cd Digital-Image-Toolkit
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## 🚀 How to Run

With the setup complete, run the main application file from the project's root directory:

```sh
python main.py
```