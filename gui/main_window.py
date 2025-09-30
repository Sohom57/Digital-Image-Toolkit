import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np

# Import modularized functions
from processing import operations
from utils import helpers

class DigitalImageToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Image Processing Toolkit")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        self.original_image = None
        self.original_array = None
        self.enhanced_image = None
        self.image_path = tk.StringVar()
        
        self.original_photo = None
        self.enhanced_photo = None
        self.original_zoom_level = 1.0
        self.enhanced_zoom_level = 1.0

        self.create_interface()
    
    def create_interface(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        self.create_developer_section(main_frame)
        self.create_file_section(main_frame)
        self.create_image_panels(main_frame)
        self.create_operations_panel(main_frame)
        
    def create_developer_section(self, parent):
        dev_frame = ttk.LabelFrame(parent, text="Developer Information", padding="10")
        dev_frame.grid(row=0, column=0, sticky=tk.W+tk.N, padx=(0, 10), pady=(0, 10))
        
        photo_frame = ttk.Frame(dev_frame)
        photo_frame.grid(row=0, column=0, pady=(0, 10))

        try:
            img_original = Image.open(helpers.resource_path("my_photo.png"))
            img = ImageOps.exif_transpose(img_original)
            img_resized = img.resize((120, 180), Image.Resampling.LANCZOS)
            self.dev_photo = ImageTk.PhotoImage(img_resized)
            photo_label = tk.Label(photo_frame, image=self.dev_photo, relief="solid", borderwidth=1)
            photo_label.pack()
        except FileNotFoundError:
            photo_placeholder = tk.Label(photo_frame, text="Photo Not Found", 
                                         width=15, height=8, bg="lightgray", 
                                         relief="solid", borderwidth=1)
            photo_placeholder.pack()

        ttk.Label(dev_frame, text="MD. FOISAL HAQUE SOHOM", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(dev_frame, text="ID: 0812220205101057", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W)
        
    def create_file_section(self, parent):
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding="10")
        file_frame.grid(row=0, column=1, sticky=tk.W+tk.E, pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Select Image", command=self.select_image).grid(row=0, column=0, padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.image_path, state="readonly").grid(row=0, column=1, sticky=tk.W+tk.E)
        ttk.Button(file_frame, text="Save Enhanced", command=self.save_image).grid(row=0, column=2, padx=(10, 0))
        
    def create_image_panels(self, parent):
        image_frame = ttk.Frame(parent)
        image_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, pady=(0, 10))
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        image_frame.rowconfigure(0, weight=1)
        
        original_frame = ttk.LabelFrame(image_frame, text="Original Image", padding="5")
        original_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=(0, 5))
        original_frame.rowconfigure(0, weight=1)
        original_frame.columnconfigure(0, weight=1)
        
        self.original_canvas = tk.Canvas(original_frame, bg="white", width=400, height=300)
        self.original_canvas.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.original_canvas.bind("<Button-4>", lambda event: self.zoom_image(event, self.original_canvas, "in"))
        self.original_canvas.bind("<Button-5>", lambda event: self.zoom_image(event, self.original_canvas, "out"))
        self.original_canvas.bind("<MouseWheel>", lambda event: self.zoom_image(event, self.original_canvas, "in" if event.delta > 0 else "out"))

        enhanced_frame = ttk.LabelFrame(image_frame, text="Enhanced Image", padding="5")
        enhanced_frame.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=(5, 0))
        enhanced_frame.rowconfigure(0, weight=1)
        enhanced_frame.columnconfigure(0, weight=1)
        
        self.enhanced_canvas = tk.Canvas(enhanced_frame, bg="white", width=400, height=300)
        self.enhanced_canvas.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.enhanced_canvas.bind("<Button-4>", lambda event: self.zoom_image(event, self.enhanced_canvas, "in"))
        self.enhanced_canvas.bind("<Button-5>", lambda event: self.zoom_image(event, self.enhanced_canvas, "out"))
        self.enhanced_canvas.bind("<MouseWheel>", lambda event: self.zoom_image(event, self.enhanced_canvas, "in" if event.delta > 0 else "out"))
        
    def create_operations_panel(self, parent):
        ops_frame = ttk.LabelFrame(parent, text="Image Processing Operations", padding="10", labelanchor="n")
        ops_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        ops_frame.columnconfigure(0, weight=1) # For centering
        ops_frame.columnconfigure(5, weight=1) # For centering

        # Basic Operations Frame
        basic_frame = ttk.LabelFrame(ops_frame, text="Basic Operations", padding="5")
        basic_frame.grid(row=0, column=1, sticky=tk.W+tk.E, padx=(0, 10))
        ttk.Button(basic_frame, text="Convert to Grayscale", command=self.run_grayscale).pack(pady=2, fill=tk.X)
        ttk.Button(basic_frame, text="Negative Image", command=self.run_negative).pack(pady=2, fill=tk.X)
        
        thresh_frame = ttk.Frame(basic_frame)
        thresh_frame.pack(pady=2, fill=tk.X)
        ttk.Label(thresh_frame, text="Threshold:").pack(side=tk.LEFT)
        self.threshold_var = tk.StringVar(value="128")
        ttk.Entry(thresh_frame, textvariable=self.threshold_var, width=10).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(thresh_frame, text="Apply", command=self.run_thresholding).pack(side=tk.LEFT)

        contrast_frame = ttk.Frame(basic_frame)
        contrast_frame.pack(pady=2, fill=tk.X)
        ttk.Label(contrast_frame, text="Contrast (α):").pack(side=tk.LEFT)
        self.contrast_var = tk.StringVar(value="1.0")
        ttk.Entry(contrast_frame, textvariable=self.contrast_var, width=6).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(contrast_frame, text="Apply", command=self.run_contrast).pack(side=tk.LEFT)
        
        # Resize Operations Frame
        resize_frame = ttk.LabelFrame(ops_frame, text="Resize Operations", padding="5")
        resize_frame.grid(row=0, column=2, sticky=tk.W+tk.E, padx=(0, 10))
        size_frame = ttk.Frame(resize_frame)
        size_frame.pack(pady=2, fill=tk.X)
        ttk.Label(size_frame, text="Size (WxH):").pack(side=tk.LEFT)
        self.resize_var = tk.StringVar(value="400x300")
        ttk.Entry(size_frame, textvariable=self.resize_var, width=10).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(size_frame, text="Resize", command=self.run_resize).pack(side=tk.LEFT)
        
        # Filtering Operations Frame
        filter_frame = ttk.LabelFrame(ops_frame, text="Filtering Operations", padding="5")
        filter_frame.grid(row=0, column=3, sticky=tk.W+tk.E, padx=(0, 10))
        smooth_frame = ttk.Frame(filter_frame)
        smooth_frame.pack(pady=2, fill=tk.X)
        ttk.Label(smooth_frame, text="Kernel:").pack(side=tk.LEFT)
        self.smooth_var = tk.StringVar(value="3")
        ttk.Entry(smooth_frame, textvariable=self.smooth_var, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(smooth_frame, text="Smooth", command=self.run_smooth).pack(side=tk.LEFT)
        
        sharp_frame = ttk.Frame(filter_frame)
        sharp_frame.pack(pady=2, fill=tk.X)
        ttk.Label(sharp_frame, text="Intensity:").pack(side=tk.LEFT)
        self.sharp_var = tk.StringVar(value="1.0")
        ttk.Entry(sharp_frame, textvariable=self.sharp_var, width=5).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(sharp_frame, text="Sharpen", command=self.run_sharpen).pack(side=tk.LEFT)
        
        # Advanced Operations Frame
        advanced_frame = ttk.LabelFrame(ops_frame, text="Advanced Operations", padding="5")
        advanced_frame.grid(row=0, column=4, sticky=tk.W+tk.E)
        
        # --- START OF CHANGES ---
        # Changed button text and command to use the new Laplacian function.
        ttk.Button(advanced_frame, text="Laplacian Edge", command=self.run_laplacian_edge).pack(pady=2, fill=tk.X)
        # --- END OF CHANGES ---
        
        ttk.Button(advanced_frame, text="Scaled Log Transform", command=self.run_log_transform).pack(pady=2, fill=tk.X)
        ttk.Button(advanced_frame, text="Log Transform (C=1)", command=self.run_log_transform_c1).pack(pady=2, fill=tk.X)
        ttk.Button(advanced_frame, text="Show Histogram", command=self.run_histogram).pack(pady=2, fill=tk.X)
        
    def _calculate_fit_zoom(self, image, canvas):
        if image is None: return 1.0
        
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        img_width, img_height = image.size
        
        if img_width == 0 or img_height == 0: return 1.0
            
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        return min(scale_x, scale_y)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                if self.original_image.mode != 'RGB':
                    if 'A' in self.original_image.mode:
                        background = Image.new('RGB', self.original_image.size, (255, 255, 255))
                        background.paste(self.original_image, mask=self.original_image.split()[-1])
                        self.original_image = background
                    else:
                        self.original_image = self.original_image.convert('RGB')
                
                self.original_array = np.array(self.original_image)
                self.image_path.set(file_path)
                
                self.original_zoom_level = self._calculate_fit_zoom(self.original_image, self.original_canvas)
                self.display_image(self.original_image, self.original_canvas, is_original=True)
                
                self.enhanced_canvas.delete("all")
                self.enhanced_image = None
                self.enhanced_photo = None
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")

    def save_image(self):
        if self.enhanced_image is None:
            messagebox.showwarning("Warning", "No enhanced image to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Enhanced Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.enhanced_image.save(file_path)
                messagebox.showinfo("Success", f"Image successfully saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save image: {str(e)}")
    
    def display_image(self, image, canvas, is_original=False):
        if image is None:
            canvas.delete("all")
            return
            
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        current_zoom_level = self.original_zoom_level if is_original else self.enhanced_zoom_level

        img_width, img_height = image.size
        new_width = int(img_width * current_zoom_level)
        new_height = int(img_height * current_zoom_level)

        if new_width <= 0 or new_height <= 0: return

        display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(display_image)
        canvas.delete("all")
        canvas.create_image(canvas_width//2, canvas_height//2, image=photo)
        
        if is_original:
            self.original_photo = photo
        else:
            self.enhanced_photo = photo
        canvas.image = photo

    def zoom_image(self, event, canvas, direction):
        is_original = canvas == self.original_canvas
        image_to_zoom = self.original_image if is_original else self.enhanced_image
        if image_to_zoom is None: return

        zoom_factor = 1.1
        
        if is_original:
            self.original_zoom_level *= zoom_factor if direction == "in" else 1/zoom_factor
            self.original_zoom_level = max(0.01, self.original_zoom_level) 
            self.display_image(self.original_image, self.original_canvas, is_original=True)
        else:
            self.enhanced_zoom_level *= zoom_factor if direction == "in" else 1/zoom_factor
            self.enhanced_zoom_level = max(0.01, self.enhanced_zoom_level) 
            self.display_image(self.enhanced_image, self.enhanced_canvas, is_original=False)
    
    def _process_and_display(self, result_array):
        self.enhanced_image = Image.fromarray(result_array)
        self.enhanced_zoom_level = self._calculate_fit_zoom(self.enhanced_image, self.enhanced_canvas)
        self.display_image(self.enhanced_image, self.enhanced_canvas)
        
    def _run_operation(self, operation_func, *args, **kwargs):
        if self.original_array is None:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        try:
            result_array = operation_func(self.original_array, *args, **kwargs)
            self._process_and_display(result_array)
        except Exception as e:
            messagebox.showerror("Error", f"{operation_func.__name__.replace('_', ' ').title()} failed: {str(e)}")

    # --- Operation Runner Methods ---
    def run_grayscale(self):
        self._run_operation(operations.convert_to_grayscale)
        
    def run_negative(self):
        self._run_operation(operations.negative_image)
        
    def run_thresholding(self):
        try:
            threshold = int(self.threshold_var.get())
            if not 0 <= threshold <= 255:
                messagebox.showerror("Error", "Threshold must be between 0 and 255")
                return
            self._run_operation(operations.apply_thresholding, threshold)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for threshold")
            
    def run_resize(self):
        try:
            size_str = self.resize_var.get().lower()
            new_width, new_height = map(int, size_str.split('x'))
            if new_width <= 0 or new_height <= 0:
                messagebox.showerror("Error", "Width and height must be positive")
                return
            self._run_operation(operations.resize_image, new_width, new_height)
        except ValueError:
            messagebox.showerror("Error", "Please enter size in format: WIDTHxHEIGHT (e.g., 400x300)")

    def run_smooth(self):
        try:
            kernel_size = int(self.smooth_var.get())
            if kernel_size < 1 or kernel_size % 2 == 0:
                messagebox.showerror("Error", "Kernel size must be an odd positive number (e.g., 3, 5)")
                return
            self._run_operation(operations.smooth_image, kernel_size)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid odd integer for kernel size")

    def run_sharpen(self):
        try:
            intensity = float(self.sharp_var.get())
            self._run_operation(operations.sharpen_image, intensity)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid float for intensity")

    # --- START OF CHANGES ---
    # Renamed the runner method to match the new operation.
    def run_laplacian_edge(self):
        self._run_operation(operations.laplacian_edge)
    # --- END OF CHANGES ---

    def run_contrast(self):
        try:
            alpha = float(self.contrast_var.get())
            if alpha <= 0:
                messagebox.showerror("Error", "Contrast factor alpha must be positive")
                return
            self._run_operation(operations.adjust_contrast, alpha)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid float for contrast factor")

    def run_log_transform(self):
        self._run_operation(operations.log_transformation)
        
    def run_log_transform_c1(self):
        self._run_operation(operations.log_transform_c1)

    def run_histogram(self):
        self._run_operation(operations.show_histogram)