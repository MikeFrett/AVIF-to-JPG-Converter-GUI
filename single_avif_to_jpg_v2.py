#!/usr/bin/env python3
import os
import tempfile
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from PIL import Image

class ImageToJPGConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("AVIF / WebP to JPG Converter")
        self.root.geometry("580x420")
        self.root.minsize(480, 360)
        self.root.resizable(True, True)
        
        # Title label
        title_label = tk.Label(root, text="Select an AVIF or WebP file:", font=("Arial", 12, "bold"))
        title_label.pack(pady=(15, 5))
        
        # File path display
        self.file_var = tk.StringVar(value="No file selected")
        self.file_entry = tk.Entry(root, textvariable=self.file_var, width=70, font=("Arial", 9), state="readonly")
        self.file_entry.pack(fill="x", padx=20, pady=5)
        
        # Browse button
        self.select_btn = tk.Button(root, text="📁 Browse Image (AVIF / WebP)", command=self.select_file, 
                                    bg="#0078d7", fg="white", font=("Arial", 10, "bold"))
        self.select_btn.pack(pady=5)
        
        # Options frame
        options_frame = tk.Frame(root)
        options_frame.pack(pady=10)
        tk.Label(options_frame, text="JPG Quality (1-100):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.quality_var = tk.IntVar(value=95)
        quality_scale = tk.Scale(options_frame, from_=1, to=100, orient=tk.HORIZONTAL, 
                                 variable=self.quality_var, length=320)
        quality_scale.pack(pady=2)
        
        # Convert button
        self.convert_btn = tk.Button(root, text="⚡ Convert to JPG", command=self.convert_file, 
                                     bg="#28a745", fg="white", font=("Arial", 13, "bold"), 
                                     state="disabled", height=2)
        self.convert_btn.pack(pady=10, ipadx=30)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready - Select an AVIF or WebP file to begin.")
        status_label = tk.Label(root, textvariable=self.status_var, fg="blue", 
                                wraplength=520, justify="left", font=("Arial", 10))
        status_label.pack(fill="both", expand=True, padx=20, pady=(5, 15))
        
        self.selected_path = None
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("AVIF & WebP Files", "*.avif *.AVIF *.webp *.WEBP"),
                ("AVIF Files", "*.avif *.AVIF"),
                ("WebP Files", "*.webp *.WEBP"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.selected_path = file_path
            display_text = f"{os.path.basename(file_path)} (Path: {file_path})"
            self.file_var.set(display_text)
            self.convert_btn.config(state="normal")
            self.status_var.set("File selected. Adjust quality if needed, then click 'Convert to JPG'.")
    
    def convert_file(self):
        if not self.selected_path or not os.path.exists(self.selected_path):
            messagebox.showerror("Error", "No valid file selected.")
            return

        is_avif = self.selected_path.lower().endswith(('.avif', '.avifs'))
        temp_png = None

        try:
            # Handle AVIF files using system decoder (avifdec or ffmpeg)
            if is_avif:
                temp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                temp_png.close()
                
                cmd_avifdec = ["avifdec", self.selected_path, temp_png.name]
                cmd_ffmpeg = ["ffmpeg", "-y", "-i", self.selected_path, temp_png.name]
                
                res = subprocess.run(cmd_avifdec, capture_output=True)
                if res.returncode != 0:
                    res = subprocess.run(cmd_ffmpeg, capture_output=True)
                    if res.returncode != 0:
                        raise RuntimeError("Missing AVIF decoder. Run 'sudo apt install libavif-bin' in your terminal.")
                
                source_path = temp_png.name
            else:
                source_path = self.selected_path

            # Open image and save as JPG
            with Image.open(source_path) as img:
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGBA")
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    final_img = background
                else:
                    final_img = img.convert("RGB")
                
                jpg_path = Path(self.selected_path).with_suffix(".jpg")
                final_img.save(jpg_path, "JPEG", quality=self.quality_var.get(), optimize=True)
                
                self.status_var.set(f"✅ Success! Saved:\n{jpg_path}")
                messagebox.showinfo("Complete", f"Converted to JPG successfully!\n\nSaved to:\n{jpg_path}")

        except Exception as e:
            error_msg = f"❌ Conversion failed: {str(e)}"
            self.status_var.set(error_msg)
            messagebox.showerror("Error", error_msg)
            
        finally:
            if temp_png and os.path.exists(temp_png.name):
                os.remove(temp_png.name)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToJPGConverter(root)
    root.mainloop()