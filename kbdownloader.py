from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QGridLayout, QBoxLayout, QVBoxLayout, QDialog, QPushButton, QLabel,
                               QProgressBar)

from kbsettingshandler import LangSetting


class DownloadsManagement(QDialog):
    def __init__(self):
        super(DownloadsManagement, self).__init__()
        self.LangSetting = LangSetting()
        self.downloads_list = []

        self.resize(400, 600)
        self.setWindowTitle(self.LangSetting.language.lang_downloads_management)
        self.download_file_name = dict()
        self.download_progress_bar = dict()
        self.download_progress_pause_button = dict()
        self.download_progress_resume_button = dict()
        self.download_progress_cancel_button = dict()
        self.download_layout = dict()
        self.download_item = dict()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setDirection(QBoxLayout.BottomToTop)
        self.setLayout(self.layout)

        self.download_info_layout = dict()
        self.download_management_layout = dict()

    def download_progress(self, download):
        if download not in self.downloads_list:
            self.downloads_list.append(download)
            n = self.downloads_list.index(download)
            self.add_download_info(n)
        n = self.downloads_list.index(download)
        total = self.downloads_list[n].totalBytes()
        received = self.downloads_list[n].receivedBytes()
        getpercents = received / total * 100
        self.download_progress_bar[n].setValue(getpercents)
        self.download_file_name[n].setText(download.downloadFileName())

    def add_download_info(self, n):
        self.download_file_name[n] = QLabel()

        self.download_progress_bar[n] = QProgressBar()
        self.download_progress_bar[n].setRange(0, 100)

        self.download_progress_pause_button[n] = QPushButton(self.LangSetting.language.lang_pause)
        self.download_progress_pause_button[n].setFixedWidth(80)
        self.download_progress_resume_button[n] = QPushButton(self.LangSetting.language.lang_resume)
        self.download_progress_resume_button[n].setFixedWidth(80)
        self.download_progress_cancel_button[n] = QPushButton(self.LangSetting.language.lang_cancel)
        self.download_progress_cancel_button[n].setFixedWidth(80)

        self.download_layout[n] = QVBoxLayout()
        self.download_item[n] = QWidget()
        self.download_item[n].setLayout(self.download_layout[n])
        self.layout.addWidget(self.download_item[n])

        self.download_info_layout[n] = QGridLayout()
        self.download_management_layout[n] = QGridLayout()
        self.download_management_layout[n].setAlignment(Qt.AlignCenter)

        self.download_layout[n].addLayout(self.download_info_layout[n])
        self.download_info_layout[n].addWidget(self.download_file_name[n], 0, 0)
        self.download_info_layout[n].addWidget(self.download_progress_bar[n], 1, 0, 1, 9)

        self.download_layout[n].addLayout(self.download_management_layout[n])
        self.download_management_layout[n].addWidget(self.download_progress_pause_button[n], 0, 0)
        self.download_management_layout[n].addWidget(self.download_progress_resume_button[n], 0, 1)
        self.download_management_layout[n].addWidget(self.download_progress_cancel_button[n], 0, 2)

        self.download_progress_pause_button[n].clicked.connect(
            lambda: self.downloads_list[n].pause()
        )
        self.download_progress_resume_button[n].clicked.connect(
            lambda: self.downloads_list[n].resume()
        )
        self.download_progress_cancel_button[n].clicked.connect(
            lambda: self.downloads_list[n].cancel()
        )
