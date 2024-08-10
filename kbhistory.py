import os
import shutil

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QWidget, QDialog, QPushButton, QGridLayout, QVBoxLayout, QTabWidget, QLabel,
                               QTableWidget)

from kbdatabase import Database
from kbsettingshandler import BasicSettings, LangSetting


class HistoryManagement(QDialog):
    open_url_signal = Signal(str)
    clear_cookies_signal = Signal()
    clear_address_bar_completer_signal = Signal()

    def __init__(self):
        super(HistoryManagement, self).__init__()

        self.database = Database()
        self.basic_settings = BasicSettings()
        self.LangSetting = LangSetting()

        self.resize(960, 600)
        self.setWindowTitle(self.LangSetting.language.lang_history_management)
        self.visit_page_title = dict()
        self.visit_url = dict()
        self.visit_time = dict()
        self.visit_layout = dict()

        self.download_url = dict()
        self.download_time = dict()
        self.download_file_name = dict()
        self.download_reference_url = dict()
        self.download_layout = dict()

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.dialog = QTabWidget()
        self.layout.addWidget(self.dialog)

        self.visits_history_layout = QVBoxLayout()
        self.visits_history_management_layout = QGridLayout()
        self.visits_history_management_layout.setAlignment(Qt.AlignCenter)

        self.visits_history_tab = QWidget()
        self.visits_history_tab.setLayout(self.visits_history_layout)

        self.visits_history_table = QTableWidget()
        self.visits_history_table.setColumnCount(3)
        self.visits_history_table.setHorizontalHeaderLabels(
            [self.LangSetting.language.lang_page_title,
             self.LangSetting.language.lang_url,
             self.LangSetting.language.lang_time]
        )
        self.visits_history_table.setColumnWidth(0, 360)
        self.visits_history_table.setColumnWidth(1, 360)
        self.visits_history_table.setColumnWidth(2, 160)
        self.visits_history_table.verticalHeader().setHidden(True)
        self.visits_history_table.setShowGrid(False)

        self.show_visits_history()

        self.clear_visits_history_button = QPushButton(self.LangSetting.language.lang_clear_visits_history)
        self.clear_visits_history_button.setFixedWidth(180)
        self.clear_cached_data_button = QPushButton(self.LangSetting.language.lang_clear_cookies_cache)
        self.clear_cached_data_button.setFixedWidth(180)

        self.visits_history_layout.addWidget(self.visits_history_table)
        self.visits_history_layout.addLayout(self.visits_history_management_layout)
        self.visits_history_management_layout.addWidget(self.clear_visits_history_button, 0, 1)
        self.visits_history_management_layout.addWidget(self.clear_cached_data_button, 0, 2)

        self.downloads_history_layout = QVBoxLayout()
        self.downloads_history_management_layout = QGridLayout()
        self.downloads_history_management_layout.setAlignment(Qt.AlignCenter)

        self.downloads_history_tab = QWidget()
        self.downloads_history_tab.setLayout(self.downloads_history_layout)

        self.downloads_history_table = QTableWidget()
        self.downloads_history_table.setColumnCount(4)
        self.downloads_history_table.setHorizontalHeaderLabels(
            [self.LangSetting.language.lang_file_name,
             self.LangSetting.language.lang_time,
             self.LangSetting.language.lang_url,
             self.LangSetting.language.lang_reference_url]
        )
        self.downloads_history_table.setColumnWidth(0, 260)
        self.downloads_history_table.setColumnWidth(1, 160)
        self.downloads_history_table.setColumnWidth(2, 280)
        self.downloads_history_table.setColumnWidth(3, 200)
        self.downloads_history_table.verticalHeader().setHidden(True)
        self.downloads_history_table.setShowGrid(False)

        self.show_downloads_history()

        self.clear_downloads_history_button = QPushButton(self.LangSetting.language.lang_clear_downloads_history)
        self.clear_downloads_history_button.setFixedWidth(180)

        self.downloads_history_layout.addWidget(self.downloads_history_table)
        self.downloads_history_layout.addLayout(self.downloads_history_management_layout)
        self.downloads_history_management_layout.addWidget(self.clear_downloads_history_button, 0, 0)

        self.dialog.addTab(self.visits_history_tab, self.LangSetting.language.lang_visits_history)
        self.dialog.addTab(self.downloads_history_tab, self.LangSetting.language.lang_downloads_history)

        self.clear_visits_history_button.clicked.connect(self.clear_visits_history)
        self.clear_cached_data_button.clicked.connect(self.clear_cached_data)
        self.clear_downloads_history_button.clicked.connect(self.clear_downloads_history)

    def clear_visits_history(self):
        self.database.reset_history_table('visits')
        self.visits_history_table.clearContents()
        self.clear_address_bar_completer_signal.emit()

    def clear_cached_data(self):
        cache_folder = f'{self.basic_settings.profile_path}\\cache'
        storage_folder = f'{self.basic_settings.profile_path}\\storage'
        if os.path.exists(cache_folder):
            shutil.rmtree(cache_folder, ignore_errors=True)
        if os.path.exists(storage_folder):
            shutil.rmtree(storage_folder, ignore_errors=True)
        self.clear_cookies_signal.emit()

    def clear_downloads_history(self):
        self.database.reset_history_table('downloads')
        self.downloads_history_table.clearContents()

    def read_visits_history(self):
        visits = self.database.read_history_table('visits')
        return visits

    def read_downloads_history(self):
        downloads = self.database.read_history_table('downloads')
        return downloads

    def show_visits_history(self):
        visits = self.read_visits_history()
        self.visits_history_table.setRowCount(len(visits))

        for n in range(len(visits)):
            visit = visits[n]

            self.visit_page_title[n] = QLabel(visit[2])
            self.visit_url[n] = QLabel(f'<a href="{visit[1]}">{visit[1]}</a>')
            self.visit_time[n] = QLabel(visit[3])

            self.visit_page_title[n].setMargin(5)
            self.visit_url[n].setMargin(5)
            self.visit_time[n].setMargin(5)

            self.visits_history_table.setCellWidget(n, 0, self.visit_page_title[n])
            self.visits_history_table.setCellWidget(n, 1, self.visit_url[n])
            self.visits_history_table.setCellWidget(n, 2, self.visit_time[n])

            self.visit_url[n].linkActivated.connect(self.send_signal)

    def show_downloads_history(self):
        downloads = self.read_downloads_history()
        self.downloads_history_table.setRowCount(len(downloads))

        for n in range(len(downloads)):
            download = downloads[n]
            self.download_file_name[n] = QLabel(download[2])
            self.download_url[n] = QLabel(f'<a href="{download[1]}">{download[1]}</a>')
            self.download_reference_url[n] = QLabel(f'<a href="{download[4]}">{download[4]}</a>')
            self.download_time[n] = QLabel(download[5])

            self.download_file_name[n].setMargin(5)
            self.download_url[n].setMargin(5)
            self.download_reference_url[n].setMargin(5)
            self.download_time[n].setMargin(5)

            self.downloads_history_table.setCellWidget(n, 0, self.download_file_name[n])
            self.downloads_history_table.setCellWidget(n, 1, self.download_time[n])
            self.downloads_history_table.setCellWidget(n, 2, self.download_url[n])
            self.downloads_history_table.setCellWidget(n, 3, self.download_reference_url[n])

            self.download_url[n].linkActivated.connect(self.send_signal)
            self.download_reference_url[n].linkActivated.connect(self.send_signal)

    def send_signal(self, url):
        self.open_url_signal.emit(url)


class VisitsHistory:
    def __init__(self):
        super(VisitsHistory, self).__init__()
        self.database = Database()

    def record_a_visit(self, page_title, web_view):
        url = web_view.url().toString()
        no_record = ['', 'about:blank', page_title, f'{page_title}/']
        if url not in no_record:
            self.database.insert_visits_history(url, page_title)

    def read_history_urls(self):
        history_urls = self.database.read_history_urls()
        history_urls = list(zip(*history_urls))
        if history_urls:
            history_urls = list(history_urls[0])
        return history_urls


class DownloadsHistory:
    def __init__(self):
        super(DownloadsHistory, self).__init__()
        self.database = Database()

    def record_a_download(self, download, reference):
        url = download.url().toString()
        file_name = download.downloadFileName()
        status = f'{download.state()}'
        reference_url = reference.url().toString()
        self.database.insert_downloads_history(url, file_name, status, reference_url)
