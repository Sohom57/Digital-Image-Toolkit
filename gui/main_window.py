import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np

from processing import operations
from utils import helpers

class DigitalImageToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Image Processing Toolkit")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Image data
        self.original_image = None
        self.original_array = None
        self.enhanced_image = None
        self.enhanced_array = None
        
        # UI State
        self.image_path = tk.StringVar()
        self.source_selection_var = tk.StringVar(value="Original")
        
        # Canvas and display data
        self.original_photo = None
        self.enhanced_photo = None
        self.original_zoom_level = 1.0
        self.enhanced_zoom_level = 1.0
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.image_on_canvas_original = None
        self.image_on_canvas_enhanced = None
        self.progress_bar = None

        self.create_interface()
    
    def create_interface(self):
        """Creates the main application layout with top controls and bottom images."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=0) 
        main_frame.rowconfigure(1, weight=1) 
        main_frame.rowconfigure(2, weight=0) 
        
        self.create_top_panel(main_frame)
        self.create_image_panels(main_frame)
        self.create_status_bar(main_frame)
        
    def create_top_panel(self, parent):
        """Creates the entire top section with developer info and a tabbed notebook for controls."""
        top_panel_frame = ttk.Frame(parent)
        top_panel_frame.grid(row=0, column=0, sticky=tk.W+tk.E, pady=(0, 10))
        top_panel_frame.columnconfigure(1, weight=1)

        self.create_developer_section(top_panel_frame)
        
        notebook = ttk.Notebook(top_panel_frame)
        notebook.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=(10, 0))

        tab1 = ttk.Frame(notebook, padding="10")
        tab2 = ttk.Frame(notebook, padding="10")
        tab3 = ttk.Frame(notebook, padding="10")

        notebook.add(tab1, text='File & Source')
        notebook.add(tab2, text='Basic & Geometric')
        notebook.add(tab3, text='Filters & Advanced')

        self.populate_file_source_tab(tab1)
        self.populate_basic_geo_tab(tab2)
        self.populate_filters_advanced_tab(tab3)

    def populate_file_source_tab(self, parent):
        """Populates the first tab with file operations and source selection."""
        parent.columnconfigure(0, weight=1)
        
        file_frame = ttk.LabelFrame(parent, text="File Operations", padding="10")
        file_frame.grid(row=0, column=0, sticky=tk.W+tk.E)
        file_frame.columnconfigure(1, weight=1)
        ttk.Button(file_frame, text="Select Image", command=self.select_image).grid(row=0, column=0, padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.image_path, state="readonly").grid(row=0, column=1, sticky=tk.W+tk.E)
        ttk.Button(file_frame, text="Save Enhanced", command=self.save_image).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(file_frame, text="Reset Enhanced", command=self.reset_enhanced_image).grid(row=0, column=3, padx=(5, 0))

        source_frame = ttk.LabelFrame(parent, text="Process From", padding="10")
        source_frame.grid(row=1, column=0, sticky=tk.W+tk.E, pady=(10, 0))
        ttk.Radiobutton(source_frame, text="Original Image", variable=self.source_selection_var, value="Original").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(source_frame, text="Enhanced Image", variable=self.source_selection_var, value="Enhanced").pack(side=tk.LEFT, padx=5)
        
    def populate_basic_geo_tab(self, parent):
        """Populates the second tab with basic and geometric operations."""
        basic_frame = ttk.LabelFrame(parent, text="Basic Operations", padding="10")
        basic_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        ttk.Button(basic_frame, text="Convert to Grayscale", command=self.run_grayscale).pack(pady=2, fill=tk.X)
        ttk.Button(basic_frame, text="Negative Image", command=self.run_negative).pack(pady=2, fill=tk.X)
        
        thresh_frame = ttk.Frame(basic_frame)
        thresh_frame.pack(pady=2, fill=tk.X)
        ttk.Label(thresh_frame, text="Threshold:").pack(side=tk.LEFT)
        self.threshold_var = tk.StringVar(value="128")
        ttk.Entry(thresh_frame, textvariable=self.threshold_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(thresh_frame, text="Apply", command=self.run_thresholding).pack(side=tk.LEFT)
        
        contrast_frame = ttk.Frame(basic_frame)
        contrast_frame.pack(pady=2, fill=tk.X)
        ttk.Label(contrast_frame, text="Contrast (α):").pack(side=tk.LEFT)
        self.contrast_var = tk.StringVar(value="1.0")
        ttk.Entry(contrast_frame, textvariable=self.contrast_var, width=6).pack(side=tk.LEFT, padx=5)
        ttk.Button(contrast_frame, text="Apply", command=self.run_contrast).pack(side=tk.LEFT)

        geo_frame = ttk.LabelFrame(parent, text="Geometric Operations", padding="10")
        geo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        size_frame = ttk.Frame(geo_frame)
        size_frame.pack(pady=2, fill=tk.X)
        ttk.Label(size_frame, text="Size (WxH):").pack(side=tk.LEFT)
        self.resize_var = tk.StringVar(value="400x300")
        ttk.Entry(size_frame, textvariable=self.resize_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(size_frame, text="Resize", command=self.run_resize).pack(side=tk.LEFT)
    
        rotate_frame = ttk.Frame(geo_frame)
        rotate_frame.pack(pady=2, fill=tk.X)
        ttk.Label(rotate_frame, text="Rotate (°):").pack(side=tk.LEFT)
        self.rotate_var = tk.StringVar(value="0")
        ttk.Entry(rotate_frame, textvariable=self.rotate_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(rotate_frame, text="Rotate", command=self.run_rotate).pack(side=tk.LEFT)
        
    def populate_filters_advanced_tab(self, parent):
        """Populates the third tab with filters and advanced operations."""
        filter_frame = ttk.LabelFrame(parent, text="Filtering Operations", padding="10")
        filter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        smooth_frame = ttk.Frame(filter_frame)
        smooth_frame.pack(pady=2, fill=tk.X)
        ttk.Label(smooth_frame, text="Kernel:").pack(side=tk.LEFT)
        self.smooth_var = tk.StringVar(value="3")
        ttk.Entry(smooth_frame, textvariable=self.smooth_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Button(smooth_frame, text="Smooth", command=self.run_smooth).pack(side=tk.LEFT)
        
        sharp_frame = ttk.Frame(filter_frame)
        sharp_frame.pack(pady=2, fill=tk.X)
        ttk.Label(sharp_frame, text="Intensity:").pack(side=tk.LEFT)
        self.sharp_var = tk.StringVar(value="1.0")
        ttk.Entry(sharp_frame, textvariable=self.sharp_var, width=5).pack(side=tk.LEFT, padx=5)
        ttk.Button(sharp_frame, text="Sharpen", command=self.run_sharpen).pack(side=tk.LEFT)
        
        advanced_frame = ttk.LabelFrame(parent, text="Advanced Operations", padding="10")
        advanced_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        ttk.Button(advanced_frame, text="Laplacian Edge", command=self.run_laplacian_edge).pack(pady=2, fill=tk.X)
        ttk.Button(advanced_frame, text="Scaled Log Transform", command=self.run_log_transform).pack(pady=2, fill=tk.X)
        ttk.Button(advanced_frame, text="Log Transform (C=1)", command=self.run_log_transform_c1).pack(pady=2, fill=tk.X)
        ttk.Button(advanced_frame, text="Show Histogram", command=self.run_histogram).pack(pady=2, fill=tk.X)

    def create_developer_section(self, parent):
        dev_frame = ttk.LabelFrame(parent, text="Developer Information", padding="10")
        dev_frame.grid(row=0, column=0, sticky=tk.W+tk.N, padx=(0, 10))
        
        photo_frame = ttk.Frame(dev_frame)
        photo_frame.grid(row=0, column=0, pady=(0, 10))
        try:
            img = ImageOps.exif_transpose(Image.open(helpers.resource_path("my_photo.png")))
            zoomed_img = ImageOps.fit(img, (100, 100), Image.Resampling.LANCZOS)
            self.dev_photo = ImageTk.PhotoImage(zoomed_img)
            tk.Label(photo_frame, image=self.dev_photo, relief="solid", borderwidth=1).pack()
        except FileNotFoundError:
            placeholder_frame = tk.Frame(photo_frame, width=100, height=100, bg="lightgray", relief="solid", borderwidth=1)
            placeholder_frame.pack_propagate(False)
            placeholder_frame.pack()
            tk.Label(placeholder_frame, text="Photo Not Found", bg="lightgray").pack(expand=True)

        ttk.Label(dev_frame, text="MD. FOISAL HAQUE SOHOM", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(dev_frame, text="ID: 0812220205101057", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W)

    def create_image_panels(self, parent):
        image_frame = ttk.Frame(parent)
        image_frame.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        image_frame.rowconfigure(0, weight=1)
        
        original_frame = ttk.LabelFrame(image_frame, text="Original Image", padding="5")
        original_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=(0, 5))
        original_frame.rowconfigure(0, weight=1)
        original_frame.columnconfigure(0, weight=1)
        
        self.original_canvas = tk.Canvas(original_frame, bg="white")
        self.original_canvas.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.original_canvas.bind("<MouseWheel>", lambda e: self.zoom_image(e, self.original_canvas, "in" if e.delta > 0 else "out"))
        self.original_canvas.bind("<ButtonPress-1>", self.start_drag)
        self.original_canvas.bind("<B1-Motion>", self.drag_motion)

        enhanced_frame = ttk.LabelFrame(image_frame, text="Enhanced Image", padding="5")
        enhanced_frame.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=(5, 0))
        enhanced_frame.rowconfigure(0, weight=1)
        enhanced_frame.columnconfigure(0, weight=1)
        
        self.enhanced_canvas = tk.Canvas(enhanced_frame, bg="white")
        self.enhanced_canvas.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        self.enhanced_canvas.bind("<MouseWheel>", lambda e: self.zoom_image(e, self.enhanced_canvas, "in" if e.delta > 0 else "out"))
        self.enhanced_canvas.bind("<ButtonPress-1>", self.start_drag)
        self.enhanced_canvas.bind("<B1-Motion>", self.drag_motion)

    def create_status_bar(self, parent):
        """Creates a status bar with a progress bar at the bottom."""
        status_frame = ttk.Frame(parent, padding=(5, 2))
        status_frame.grid(row=2, column=0, sticky=tk.W+tk.E)
        self.progress_bar = ttk.Progressbar(status_frame, orient='horizontal', mode='determinate')
        self.progress_bar.pack(fill=tk.X, expand=True)

    def update_progress(self, value):
        """Updates the progress bar and forces the UI to refresh."""
        if self.progress_bar:
            self.progress_bar['value'] = value
            self.root.update_idletasks()
        
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if not file_path: return
        try:
            img = Image.open(file_path)
            if img.mode != 'RGB':
                if 'A' in img.mode:
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[-1])
                    self.original_image = bg
                else:
                    self.original_image = img.convert('RGB')
            else:
                self.original_image = img
            
            self.original_array = np.array(self.original_image)
            self.image_path.set(file_path)

            self.enhanced_canvas.delete("all")
            self.enhanced_image = None
            self.enhanced_array = None
            self.enhanced_photo = None

            self.original_zoom_level = self._calculate_fit_zoom(self.original_image, self.original_canvas)
            self.display_image(self.original_image, self.original_canvas, is_original=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")

    def save_image(self):
        if self.enhanced_image is None:
            messagebox.showwarning("Warning", "No enhanced image to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            try:
                self.enhanced_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save image: {e}")

    def reset_enhanced_image(self):
        """Resets the enhanced image panel to the original image."""
        if self.original_array is None:
            messagebox.showwarning("Warning", "No original image is loaded.")
            return

        self.enhanced_array = self.original_array.copy()
        self.enhanced_image = self.original_image.copy()
        self.original_zoom_level = self._calculate_fit_zoom(self.original_image, self.original_canvas)
        self.enhanced_zoom_level = self.original_zoom_level

        self.display_image(self.original_image, self.original_canvas, is_original=True)
        self.display_image(self.enhanced_image, self.enhanced_canvas, is_original=False)

    def display_image(self, image, canvas, is_original=False):
        if image is None:
            canvas.delete("all")
            return
            
        canvas.update_idletasks()
        zoom = self.original_zoom_level if is_original else self.enhanced_zoom_level
        new_size = (int(image.width * zoom), int(image.height * zoom))

        if new_size[0] <= 0 or new_size[1] <= 0: return

        disp_img = image.resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(disp_img)
        
        canvas.delete("all")
        img_id = canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2, image=photo)

        if is_original:
            self.original_photo = photo
            self.image_on_canvas_original = img_id
        else:
            self.enhanced_photo = photo
            self.image_on_canvas_enhanced = img_id
        canvas.image = photo

    def _calculate_fit_zoom(self, image, canvas):
        if image is None: return 1.0
        canvas.update_idletasks()
        if image.width == 0 or image.height == 0: return 1.0
        scale = min(canvas.winfo_width()/image.width, canvas.winfo_height()/image.height)
        return scale if scale > 0 else 1.0

    def zoom_image(self, event, canvas, direction):
        is_original = canvas == self.original_canvas
        img_to_zoom = self.original_image if is_original else self.enhanced_image
        if img_to_zoom is None: return

        zoom_factor = 1.1
        if is_original:
            self.original_zoom_level *= zoom_factor if direction == "in" else 1/zoom_factor
            self.display_image(self.original_image, self.original_canvas, True)
        else:
            self.enhanced_zoom_level *= zoom_factor if direction == "in" else 1/zoom_factor
            self.display_image(self.enhanced_image, self.enhanced_canvas, False)

    def start_drag(self, event):
        self.drag_start_x, self.drag_start_y = event.x, event.y

    def drag_motion(self, event):
        dx, dy = event.x - self.drag_start_x, event.y - self.drag_start_y
        canvas = event.widget
        img_id = self.image_on_canvas_original if canvas == self.original_canvas else self.image_on_canvas_enhanced
        if img_id:
            canvas.move(img_id, dx, dy)
        self.drag_start_x, self.drag_start_y = event.x, event.y

    def _process_and_display(self, result_array):
        self.enhanced_image = Image.fromarray(result_array)
        self.enhanced_array = result_array
        self.enhanced_zoom_level = self._calculate_fit_zoom(self.enhanced_image, self.enhanced_canvas)
        self.display_image(self.enhanced_image, self.enhanced_canvas)

    def _run_operation(self, operation_func, *args, **kwargs):
        source_array = None
        if self.source_selection_var.get() == "Original":
            source_array = self.original_array
            if source_array is None:
                messagebox.showwarning("Warning", "Please select an image first.")
                return
        else:
            source_array = self.enhanced_array
            if source_array is None:
                messagebox.showwarning("Warning", "There is no enhanced image to process. Process from 'Original' first.")
                return
        
        try:
            self.update_progress(0)
            kwargs['progress_callback'] = self.update_progress
            result_array = operation_func(source_array, *args, **kwargs)
            self.update_progress(100)
            self._process_and_display(result_array)
            self.update_progress(0)
        except Exception as e:
            self.update_progress(0)
            messagebox.showerror("Error", f"{operation_func.__name__.replace('_', ' ').title()} failed: {e}")

    # --- Operation Runner Methods ---
    def run_grayscale(self): self._run_operation(operations.convert_to_grayscale)
    def run_negative(self): self._run_operation(operations.negative_image)
    def run_thresholding(self):
        try:
            val = int(self.threshold_var.get())
            if not 0 <= val <= 255: raise ValueError()
            self._run_operation(operations.apply_thresholding, val)
        except ValueError: messagebox.showerror("Error", "Threshold must be an integer between 0 and 255.")
    def run_contrast(self):
        try:
            val = float(self.contrast_var.get())
            if val <= 0: raise ValueError()
            self._run_operation(operations.adjust_contrast, val)
        except ValueError: messagebox.showerror("Error", "Contrast must be a positive number.")
    def run_resize(self):
        try:
            w, h = map(int, self.resize_var.get().lower().split('x'))
            if w <= 0 or h <= 0: raise ValueError()
            self._run_operation(operations.resize_image, w, h)
        except ValueError: messagebox.showerror("Error", "Size must be in format WIDTHxHEIGHT with positive integers.")
    def run_rotate(self):
        try:
            deg = float(self.rotate_var.get())
            self._run_operation(operations.manual_rotate, deg)
        except ValueError: messagebox.showerror("Error", "Degree must be a valid number.")
    def run_smooth(self):
        try:
            val = int(self.smooth_var.get())
            if val < 1 or val % 2 == 0: raise ValueError()
            self._run_operation(operations.smooth_image, val)
        except ValueError: messagebox.showerror("Error", "Kernel must be a positive, odd integer.")
    def run_sharpen(self):
        try:
            val = float(self.sharp_var.get())
            self._run_operation(operations.sharpen_image, val)
        except ValueError: messagebox.showerror("Error", "Intensity must be a valid number.")
    def run_laplacian_edge(self): self._run_operation(operations.laplacian_edge)
    def run_log_transform(self): self._run_operation(operations.log_transformation)
    def run_log_transform_c1(self): self._run_operation(operations.log_transform_c1)
    def run_histogram(self): self._run_operation(operations.show_histogram)