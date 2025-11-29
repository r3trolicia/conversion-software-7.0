# Conversion Software 7.0

**By r3trolicia**  

A versatile desktop application for converting **images, audio, video, and documents** to various formats. Built with **Python 3** and **PyQt6**, it supports drag-and-drop and batch conversion.

---

## Features

- Drag-and-drop files or use the "Add Files" button.
- Automatically detects file type (image, audio, video, document).
- Converts files to a wide range of supported formats.
- Special handling for animated GIFs: can convert to video formats.
- Batch conversion support.
- Auto-closes after conversion (optional workflow-friendly feature).

---

## Supported Formats

**Images:** png, jpg, jpeg, gif, bmp, webp, tiff, heic, avif, svg, ico, jp2, xbm, ppm, pnm, psd, pdf  
**Audio:** mp3, wav, flac, ogg, aac, m4a, opus, wma, alac, ac3, pcm_s16le, amr, caf, aiff, vorbis  
**Video:** mp4, mkv, avi, mov, webm, flv, mpg, mpeg, ogv, wmv, 3gp, ts, m4v, rm, vob  
**Documents:** pdf, docx, odt, txt, rtf, html, epub, fodt, xls, xlsx, ods, csv, ppt, pptx, fodp  

---

## Requirements

- Python 3.10+  
- [PyQt6](https://pypi.org/project/PyQt6/)  
- [ImageMagick](https://imagemagick.org/) (`convert` command) for image conversions  
- [FFmpeg](https://ffmpeg.org/) for audio/video conversions  
- LibreOffice for document conversions  

**Install Python dependencies:**

```bash
pip install PyQt6
```

---

## Requirements

**Install system dependencies (Debian/Ubuntu example):**

```bash
sudo apt install imagemagick ffmpeg libreoffice
```

---

## Usage

```bash
python3 converter.py
```
- Drag files into the window or click Add Files.
- Select the desired output format from the dropdown.
- Click Convert to start conversion.
- A message box will appear when the conversion is complete.

---


## Notes

- Animated GIFs can be converted to video formats using FFmpeg.
- Unsupported file types will be skipped with a warning.
- Conversion errors are shown via dialog boxes.

---

## License

This project is MIT licensed
