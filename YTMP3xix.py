import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QProgressBar, QMessageBox
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont
from PyQt5.QtCore import Qt
from pytube import YouTube


class YouTubeToMP3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube to MP3 Converter')
        self.setFixedSize(400, 200)
        self.setWindowIcon(QIcon('icon.png'))

        # Set background color and font
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(34, 49, 63))
        self.setPalette(pal)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)

        # Create labels, input field, and download button
        self.url_label = QLabel('Enter YouTube Video URL:', self)
        self.url_label.move(50, 30)
        self.url_label.setStyleSheet('color: white')

        self.url_input = QLineEdit(self)
        self.url_input.move(50, 60)
        self.url_input.resize(300, 30)
        self.url_input.setStyleSheet('background-color: white')

        self.progress_label = QLabel('Download Progress:', self)
        self.progress_label.move(50, 110)
        self.progress_label.setStyleSheet('color: white')

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 140, 300, 20)
        self.progress_bar.setStyleSheet('QProgressBar {border: 1px solid grey; border-radius: 5px; '
                                         'background-color: #d7dbdd; color: black} '
                                         'QProgressBar::chunk {background-color: #27ae60}')

        self.download_button = QPushButton('Download', self)
        self.download_button.move(150, 170)
        self.download_button.setStyleSheet('background-color: #27ae60; color: white; font-weight: bold')
        self.download_button.clicked.connect(self.download)

        self.made_by_label = QLabel('Virtuosoxix', self)
        self.made_by_label.setAlignment(Qt.AlignRight)
        self.made_by_label.setGeometry(260, 180, 130, 20)
        self.made_by_label.setStyleSheet('color: white')

        self.show()

    def download(self):
        url = self.url_input.text()

        # Download the YouTube video
        video = YouTube(url, on_progress_callback=self.update_progress_bar)
        video.streams.first().download()

        # Convert the video file to MP3 using ffmpeg
        input_file = os.path.join(os.getcwd(), video.title + '.3gpp')
        output_file = os.path.join(os.getcwd(), video.title + '.mp3')
        subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', output_file])

        # Delete the original video file
        os.remove(input_file)

        # Clear the input field
        self.url_input.setText('')

        # Reset the progress bar
        self.progress_bar.reset()

        # Open the downloaded file location
        self.open_download_location(output_file)

    def update_progress_bar(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        downloaded = size - bytes_remaining
        progress = int(downloaded / size * 100)
        self.progress_bar.setValue(progress)

    def open_download_location(self, output_file):
        download_dir = os.path.dirname(output_file)
        if sys.platform == 'win32':
            os.startfile(download_dir)
        else:
            opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            subprocess.call([opener, download_dir])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = YouTubeToMP3()
    sys.exit(app.exec_())
