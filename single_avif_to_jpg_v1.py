import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_avif
import os
from pathlib import Path

class AVIFtoJPGConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Single AVIF to JPG Converter")
        self.root.geometry("550x350")
        self.root.minsize(450, 300)
        self.root.resizable(True, True)
        
        # Title label
        title_label = tk.Label(root, text="Select an AVIF file:", font=("Arial", 12, "bold"))
        title_label.pack(pady=15)
        
        # File path display - Entry for horizontal scrolling on long paths
        self.file_var = tk.StringVar(value="No file selected")
        self.file_entry = tk.Entry(root, textvariable=self.file_var, width=70, font=("Arial", 9), state="readonly")
        self.file_entry.pack(fill="x", padx=20, pady=5)
        
        # Browse button
        self.select_btn = tk.Button(root, text="Browse AVIF File", command=self.select_file, 
                                    bg="orange", fg="white", font=("Arial", 10, "bold"))
        self.select_btn.pack(pady=10)
        
        # Options frame
        options_frame = tk.Frame(root)
        options_frame.pack(pady=25)
        tk.Label(options_frame, text="JPG Quality (1-100):", font=("Arial", 10, "bold")).pack(anchor="w")
        self.quality_var = tk.IntVar(value=95)
        quality_scale = tk.Scale(options_frame, from_=1, to=100, orient=tk.HORIZONTAL, 
                                 variable=self.quality_var, length=300)
        quality_scale.pack(pady=5)
        
        # Convert button - fixed prominent position
        self.convert_btn = tk.Button(root, text="Convert to JPG", command=self.convert_file, 
                                     bg="green", fg="white", font=("Arial", 14, "bold"), 
                                     state="disabled", height=2)
        self.convert_btn.pack(pady=25, ipadx=40)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready - Select a file to begin.")
        status_label = tk.Label(root, textvariable=self.status_var, fg="blue", 
                                wraplength=500, justify="left", font=("Arial", 10))
        status_label.pack(pady=10)
        
        self.selected_path = None
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select AVIF File",
            filetypes=[("AVIF files", "*.avif *.AVIF")]
        )
        if file_path:
            self.selected_path = file_path
            # Show filename + full path; Entry scrolls horizontally for long names/paths
            display_text = f"{os.path.basename(file_path)} (Full path: {file_path})"
            self.file_var.set(display_text)
            self.convert_btn.config(state="normal")
            self.status_var.set("File selected. Adjust quality if needed, then click 'Convert to JPG'.")
    
    def convert_file(self):
        if not self.selected_path or not os.path.exists(self.selected_path):
            messagebox.showerror("Error", "No valid file selected.")
            return
        
        try:
            with Image.open(self.selected_path) as img:
                # Convert to RGB if necessary (handles RGBA, transparency flattening, etc.)
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")
                
                # Output: same directory, replace .avif with .jpg
                jpg_path = Path(self.selected_path).with_suffix(".jpg")
                
                # Save optimized JPG
                img.save(jpg_path, "JPEG", quality=self.quality_var.get(), optimize=True)
                
                self.status_var.set(f"✅ Success! Converted and saved: {jpg_path}")
                messagebox.showinfo("Complete", f"AVIF converted to JPG!\n\nOutput: {jpg_path}\n\nFile ready in the original directory.")
                
        except Exception as e:
            error_msg = f"❌ Conversion failed: {str(e)}"
            self.status_var.set(error_msg)
            messagebox.showerror("Error", error_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = AVIFtoJPGConverter(root)
    root.mainloop()
