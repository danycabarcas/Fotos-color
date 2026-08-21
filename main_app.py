import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import os
import urllib.request
import json
import webbrowser
from optimize import optimize_images

APP_VERSION = "1.0.0"
GITHUB_REPO = "daniel-cabarcas/Optimizador-Fotos" # Cambia esto a tu usuario/repositorio real


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Optimizador de Fotos v{APP_VERSION} - DanyTechCo")
        self.geometry("750x800")
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Optimizador de Fotos", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input Directory
        self.input_dir = ctk.StringVar()
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        self.input_label = ctk.CTkLabel(self.input_frame, text="Carpeta de Origen:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10)
        self.input_entry = ctk.CTkEntry(self.input_frame, textvariable=self.input_dir, state="disabled")
        self.input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.input_btn = ctk.CTkButton(self.input_frame, text="Explorar", command=self.select_input_dir)
        self.input_btn.grid(row=0, column=2, padx=10, pady=10)

        # Output Directory
        self.output_dir = ctk.StringVar()
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.output_frame.grid_columnconfigure(1, weight=1)

        self.output_label = ctk.CTkLabel(self.output_frame, text="Carpeta Destino:")
        self.output_label.grid(row=0, column=0, padx=10, pady=10)
        self.output_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_dir, state="disabled")
        self.output_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.output_btn = ctk.CTkButton(self.output_frame, text="Explorar", command=self.select_output_dir)
        self.output_btn.grid(row=0, column=2, padx=10, pady=10)

        # Settings Frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Max Size
        self.size_label = ctk.CTkLabel(self.settings_frame, text="Peso Máx (MB):")
        self.size_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.size_entry = ctk.CTkEntry(self.settings_frame, width=80)
        self.size_entry.insert(0, "1.0")
        self.size_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Max Dim
        self.dim_label = ctk.CTkLabel(self.settings_frame, text="Ancho/Alto Máx (px):")
        self.dim_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.dim_entry = ctk.CTkEntry(self.settings_frame, width=80)
        self.dim_entry.insert(0, "1920")
        self.dim_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        
        # Quality
        self.quality_label = ctk.CTkLabel(self.settings_frame, text="Calidad Inicial (0-100):")
        self.quality_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.quality_entry = ctk.CTkEntry(self.settings_frame, width=80)
        self.quality_entry.insert(0, "85")
        self.quality_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Watermark Frame
        self.wm_frame = ctk.CTkFrame(self)
        self.wm_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.wm_frame.grid_columnconfigure(1, weight=1)
        
        self.wm_path = ctk.StringVar()
        self.wm_label = ctk.CTkLabel(self.wm_frame, text="Marca de Agua (Opcional):")
        self.wm_label.grid(row=0, column=0, padx=10, pady=10)
        self.wm_entry = ctk.CTkEntry(self.wm_frame, textvariable=self.wm_path, state="disabled")
        self.wm_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.wm_btn = ctk.CTkButton(self.wm_frame, text="Seleccionar PNG", command=self.select_watermark)
        self.wm_btn.grid(row=0, column=2, padx=10, pady=10)
        
        self.wm_pos_label = ctk.CTkLabel(self.wm_frame, text="Posición:")
        self.wm_pos_label.grid(row=1, column=0, padx=10, pady=10)
        self.wm_pos = ctk.CTkOptionMenu(self.wm_frame, values=["bottom-right", "bottom-left", "top-right", "top-left", "center"])
        self.wm_pos.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        self.wm_opacity_label = ctk.CTkLabel(self.wm_frame, text="Opacidad (0.0 - 1.0):")
        self.wm_opacity_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.wm_opacity = ctk.CTkEntry(self.wm_frame, width=60)
        self.wm_opacity.insert(0, "0.5")
        self.wm_opacity.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Process Button
        self.process_btn = ctk.CTkButton(self, text="INICIAR OPTIMIZACIÓN", command=self.start_optimization, font=ctk.CTkFont(size=16, weight="bold"), height=50)
        self.process_btn.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        # Progress
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=6, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

        # Log Textbox
        self.log_box = ctk.CTkTextbox(self, state="disabled", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Credits
        self.credits_label = ctk.CTkLabel(self, text="Creado por DanyTechCo - Danycabarcas@gmail.com", font=ctk.CTkFont(size=12))
        self.credits_label.grid(row=11, column=0, padx=20, pady=(0, 10))

        # Update frame
        self.update_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.update_frame.grid(row=0, column=0, sticky="ne", padx=20, pady=20)

        # Check for updates in background
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def check_for_updates(self):
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "").replace("v", "")
                if latest_version and latest_version != APP_VERSION:
                    # Update UI in main thread using after()
                    self.after(0, self.show_update_available, latest_version, data.get("html_url"))
        except Exception as e:
            pass # Ignore errors if no internet or repo doesn't exist yet

    def show_update_available(self, version, url):
        self.update_btn = ctk.CTkButton(self.update_frame, text=f"¡Nueva versión v{version} disponible!", 
                                        fg_color="#10B981", hover_color="#059669", text_color="white",
                                        font=ctk.CTkFont(weight="bold"),
                                        command=lambda: webbrowser.open(url))
        self.update_btn.pack()

    def select_input_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.input_dir.set(dir_path)

    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)

    def select_watermark(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if file_path:
            self.wm_path.set(file_path)

    def append_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_progress(self, value):
        self.progress_bar.set(value)

    def start_optimization(self):
        if not self.input_dir.get() or not self.output_dir.get():
            self.append_log("Error: Debes seleccionar las carpetas de origen y destino.")
            return
        
        self.process_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        
        # Read settings
        try:
            max_size = float(self.size_entry.get())
            max_dim = int(self.dim_entry.get())
            quality = int(self.quality_entry.get())
            wm_opacity = float(self.wm_opacity.get())
        except ValueError:
            self.append_log("Error: Verifica que los valores de tamaño, calidad y opacidad sean números válidos.")
            self.process_btn.configure(state="normal")
            return

        # Start thread
        thread = threading.Thread(target=self.run_optimization_task, args=(max_size, max_dim, quality, wm_opacity))
        thread.start()

    def run_optimization_task(self, max_size, max_dim, quality, wm_opacity):
        try:
            optimize_images(
                input_dir=self.input_dir.get(),
                output_dir=self.output_dir.get(),
                max_size_mb=max_size,
                max_dim=max_dim,
                start_quality=quality,
                watermark_path=self.wm_path.get(),
                watermark_position=self.wm_pos.get(),
                watermark_opacity=wm_opacity,
                progress_callback=self.update_progress,
                log_callback=self.append_log
            )
        except Exception as e:
            self.append_log(f"Ocurrió un error inesperado: {e}")
        finally:
            self.process_btn.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
