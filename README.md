# AVIF to JPG Converter (Single Image GUI)

A simple cross-platform Python GUI tool that converts a single AVIF image to JPG using a quality slider. Built with Tkinter and Pillow.

## Features
- Convert `.avif` / `.AVIF` images to `.jpg`
- Adjustable JPG quality (1–100, default 95)
- Saves output in the same directory as the original file
- Handles transparency (RGBA → RGB flattening)
- Optimized JPG output
- Clear success/error messages
- Usage: python single_avif_to_jpg.py

## Requirements
- Python 3.8+
- Pillow 10.0+ with AVIF support

## Installation
```bash
pip install pillow pillow-avif-plugin
