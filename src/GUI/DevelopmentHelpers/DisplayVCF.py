"""
VCF File Viewer Application

This application allows users/devs to open and view VCF files.
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QFileDialog, QVBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal


class FileLoaderThread(QThread):
    """
   A thread that loads a file in chunks and emits a signal for each chunk.

   Attributes:
       progress (pyqtSignal): Signal emitted for each chunk of the file.
       filepath (str): Path to the file to be loaded.
       chunk_size (int): Size of each chunk in bytes.
   """

    progress = pyqtSignal(str)

    def __init__(self, filepath, chunk_size=1024 * 1024):
        super().__init__()
        self.filepath = filepath
        self.chunk_size = chunk_size

    def run(self):
        """
        Loads the file in chunks and emits a signal for each chunk.
        """
        try:
            with open(self.filepath, 'r', buffering=self.chunk_size) as file:
                while True:
                    chunk = file.read(self.chunk_size)
                    if not chunk:
                        break
                    self.progress.emit(chunk)
        except Exception as e:
            self.progress.emit(f"Error reading file: {str(e)}")


class VCFViewer(QWidget):
    """
    A widget that displays a VCF file.

    Attributes:
    textEdit (QTextEdit): Text area where the VCF file is displayed.
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1600, 600)
        self.setWindowTitle('VCF File Viewer')

        layout = QVBoxLayout()

        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)

        # Button to open VCF file
        open_button = QPushButton('Open VCF file')
        open_button.clicked.connect(self.openFile)
        layout.addWidget(open_button)

        # Button to save the modified VCF file
        save_button = QPushButton('Save VCF file')
        save_button.clicked.connect(self.saveFile)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def openFile(self):
        """
        Opens a VCF file and displays its contents in the text area.
        """
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open VCF file', '.', 'VCF files (*.vcf)')
        if filepath:
            self.textEdit.clear()
            # Temporarily disable updates
            self.textEdit.setUpdatesEnabled(False)
            self.thread = FileLoaderThread(filepath)
            self.thread.progress.connect(self.appendText)
            # Re-enable updates after loading
            self.thread.finished.connect(lambda: self.textEdit.setUpdatesEnabled(True))
            self.thread.start()

    def appendText(self, text):
        """
        Appends text to the text area.

        Args:
            text (str): Text to be appended.
        """
        # Move cursor to the end
        self.textEdit.moveCursor(self.textEdit.textCursor().End)
        # Insert text without appending a newline
        self.textEdit.insertPlainText(text)

    def saveFile(self):
        """
        Saves the contents of the text area to a VCF file.
        """
        # Open a file dialog to save the file
        filepath, _ = QFileDialog.getSaveFileName(self, 'Save VCF file', '.', 'VCF files (*.vcf)')
        if filepath:
            try:
                # Save the content of the QTextEdit to the selected file
                with open(filepath, 'w') as file:
                    file.write(self.textEdit.toPlainText())
            except Exception as e:
                print(f"Error saving file: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = VCFViewer()
    viewer.show()
    sys.exit(app.exec_())