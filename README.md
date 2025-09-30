# Digital Image Processing Toolkit

A desktop application built with Python and Tkinter for performing various digital image processing operations. The toolkit provides a user-friendly interface to load an image, apply enhancements and transformations, and view the original and processed images side-by-side.



## ✨ Features

- **File Operations**: Select and save images in various formats (`.png`, `.jpg`, `.bmp`).
- **Basic Operations**:
    - Convert to Grayscale
    - Image Negation
    - Binary Thresholding
    - Contrast Adjustment
- **Resize Operations**:
    - Resize image to custom dimensions.
- **Filtering**:
    - Image Smoothing (Mean Filter)
    - Image Sharpening
- **Advanced Operations**:
    - Edge Detection (Sobel Operator)
    - Logarithmic Transformations (Scaled and `C=1`)
    - Histogram Visualization

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
-   **`gui/main_window.py`**: Defines the entire Tkinter-based user interface.
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
    git clone [https://github.com/sohom57/digital-image-toolkit.git](https://github.com/sohom57/digital-image-toolkit.git)
    cd digital-image-toolkit
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

This will launch the Digital Image Processing Toolkit window.