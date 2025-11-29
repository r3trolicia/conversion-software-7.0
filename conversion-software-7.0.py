#!/usr/bin/env python3
# Conversion Software 7.0 - By r3trolicia 
import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QComboBox, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt

# --- Expanded format lists ---
IMAGE_FORMATS = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff", "heic", "avif", "svg", "ico", "jp2", "xbm", "ppm", "pnm", "psd", "pdf"]
AUDIO_FORMATS = ["mp3", "wav", "flac", "ogg", "aac", "m4a", "opus", "wma", "alac", "ac3", "pcm_s16le", "amr", "caf", "aiff", "vorbis"]
VIDEO_FORMATS = ["mp4", "mkv", "avi", "mov", "webm", "flv", "mpg", "mpeg", "ogv", "wmv", "3gp", "ts", "m4v", "rm", "vob"]
DOC_FORMATS   = ["pdf", "docx", "odt", "txt", "rtf", "html", "epub", "fodt", "xls", "xlsx", "ods", "csv", "ppt", "pptx", "fodp"]

FORMAT_MAP = {
    "image": IMAGE_FORMATS,
    "audio": AUDIO_FORMATS,
    "video": VIDEO_FORMATS,
    "document": DOC_FORMATS
}

def detect_type(ext):
    ext = ext.lower()
    if ext in IMAGE_FORMATS:
        return "image"
    elif ext in AUDIO_FORMATS:
        return "audio"
    elif ext in VIDEO_FORMATS:
        return "video"
    elif ext in DOC_FORMATS:
        return "document"
    else:
        return None

class Converter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion Software 7.0")
        self.setGeometry(100, 100, 500, 400)
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()
        self.label = QLabel("Drag files here or click 'Add Files'")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        self.add_button = QPushButton("Add Files")
        self.add_button.clicked.connect(self.add_files)
        self.layout.addWidget(self.add_button)

        self.format_combo = QComboBox()
        self.layout.addWidget(QLabel("Select output format:"))
        self.layout.addWidget(self.format_combo)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_files)
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select files")
        for f in files:
            self.file_list.addItem(f)
        self.update_format_options()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.file_list.addItem(url.toLocalFile())
        self.update_format_options()

    def update_format_options(self):
        if self.file_list.count() == 0:
            return
        first_file = self.file_list.item(0).text()
        ext = os.path.splitext(first_file)[1][1:].lower()
        file_type = detect_type(ext)

        if not file_type:
            self.format_combo.clear()
            return

        options = FORMAT_MAP[file_type]

        # Special: if animated GIF, allow video outputs as well
        if ext == "gif":
            options += VIDEO_FORMATS

        self.format_combo.clear()
        self.format_combo.addItems(options)

    def convert_files(self):
        target_format = self.format_combo.currentText()
        for i in range(self.file_list.count()):
            file_path = self.file_list.item(i).text()
            ext = os.path.splitext(file_path)[1][1:].lower()
            output_file = os.path.splitext(file_path)[0] + "." + target_format
            file_type = detect_type(ext)

            try:
                if file_type == "image":
                    # GIF -> Video conversion using ffmpeg
                    if ext == "gif" and target_format in VIDEO_FORMATS:
                        subprocess.run(["ffmpeg", "-i", file_path, output_file], check=True)
                    else:
                        subprocess.run(["convert", file_path, output_file], check=True)

                elif file_type in ["audio", "video"]:
                    subprocess.run(["ffmpeg", "-i", file_path, output_file], check=True)

                elif file_type == "document":
                    subprocess.run(["libreoffice", "--headless", "--convert-to", target_format, file_path], check=True)

                else:
                    QMessageBox.warning(self, "Unsupported Format", f"File {file_path} is not supported")

            except subprocess.CalledProcessError as e:
                QMessageBox.critical(self, "Error", f"Failed to convert {file_path}:\n{e}")

        QMessageBox.information(self, "Done", "Conversion completed!")
        self.close()  # Auto-close

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Converter()

    # Load files passed from Dolphin Open With
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            if os.path.isfile(f):
                window.file_list.addItem(f)
        window.update_format_options()

    window.show()
    sys.exit(app.exec())
