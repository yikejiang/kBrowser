import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (QWidget, QApplication, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget,
                               QCompleter)
from PySide6.QtWebEngineCore import (QWebEnginePage, QWebEngineProfile, QWebEngineSettings, QWebEngineDownloadRequest)
from PySide6.QtWebEngineWidgets import QWebEngineView

from kbsettings import Settings
from kbsettingshandler import BasicSettings, SearchEngines, WindowSettings, LangSetting
from kbdownloader import DownloadsManagement
from kbprivacy import CertificatesHandler, PermissionsHandler
from kbhistory import HistoryManagement, VisitsHistory, DownloadsHistory


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.downloads_dialog = DownloadsManagement()
        self.cert_dialog = CertificatesHandler()
        self.permission_dialog = PermissionsHandler()
        self.settings_dialog = None
        self.history_dialog = None
        self.visits_history = VisitsHistory()
        self.downloads_history = DownloadsHistory()
        self.basic_settings = BasicSettings()
        self.window_settings = WindowSettings()
        self.LangSetting = LangSetting()

        # Title of the browser's main window
        self.setWindowTitle('kBrowser')

        # Address bar
        self.address_bar = QLineEdit()
        self.history_urls = self.visits_history.read_history_urls()
        address_suggestions = QCompleter(self.history_urls)
        address_suggestions.setCompletionMode(QCompleter.PopupCompletion)
        address_suggestions.setFilterMode(Qt.MatchContains)
        self.address_bar.setCompleter(address_suggestions)

        # Tabs for web_view
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setStyleSheet("QTabBar::tab { width: 160px; }")

        # Initial tab
        self.tab_add('')

        # Buttons
        self.back_button = QPushButton(self.LangSetting.language.lang_back)
        self.back_button.setFixedWidth(80)
        self.forward_button = QPushButton(self.LangSetting.language.lang_forward)
        self.forward_button.setFixedWidth(80)
        self.reload_button = QPushButton(self.LangSetting.language.lang_reload)
        self.reload_button.setFixedWidth(80)
        self.stop_button = QPushButton(self.LangSetting.language.lang_stop)
        self.stop_button.setFixedWidth(80)
        self.settings_button = QPushButton(self.LangSetting.language.lang_settings)
        self.settings_button.setFixedWidth(80)
        self.downloads_button = QPushButton(self.LangSetting.language.lang_downloads)
        self.downloads_button.setFixedWidth(80)
        self.history_button = QPushButton(self.LangSetting.language.lang_history)
        self.history_button.setFixedWidth(80)

        # Layout of the browser
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout_top = QHBoxLayout()

        self.layout.addLayout(self.layout_top)

        self.layout_actions = QHBoxLayout()
        self.layout_top.addLayout(self.layout_actions)

        self.layout_actions.addWidget(self.back_button)
        self.layout_actions.addWidget(self.forward_button)
        self.layout_actions.addWidget(self.reload_button)
        self.layout_actions.addWidget(self.stop_button)

        self.layout_addressbar = QHBoxLayout()
        self.layout_top.addLayout(self.layout_addressbar)

        self.layout_addressbar.addWidget(self.address_bar)

        self.layout_features = QHBoxLayout()
        self.layout_top.addLayout(self.layout_features)

        self.layout_features.addWidget(self.settings_button)
        self.layout_features.addWidget(self.downloads_button)
        self.layout_features.addWidget(self.history_button)

        self.layout_tabs = QVBoxLayout()
        self.layout.addLayout(self.layout_tabs)

        self.layout_tabs.addWidget(self.tabs)

        # Actions of clicking buttons
        self.back_button.clicked.connect(self.back)
        self.forward_button.clicked.connect(self.forward)
        self.reload_button.clicked.connect(self.reload)
        self.stop_button.clicked.connect(self.stop)
        self.settings_button.clicked.connect(self.settings_management)
        self.downloads_button.clicked.connect(self.downloads_management)
        self.history_button.clicked.connect(self.history_management)

        # Actions of operating a keyboard
        self.address_bar.returnPressed.connect(self.load)

        # Actions of operating tabs
        self.tabs.tabBarDoubleClicked.connect(self.tab_open)
        self.tabs.currentChanged.connect(self.tab_change)
        self.tabs.tabCloseRequested.connect(self.tab_close)

    def update_address_bar_completer(self, page_title, web_view):
        web_address = web_view.url().toString()
        no_suggest = ['', 'about:blank', page_title, f'{page_title}/']
        if web_address not in no_suggest:
            if web_address not in self.history_urls:
                self.history_urls.append(web_address)
                address_suggestions = QCompleter(self.history_urls)
                address_suggestions.setCompletionMode(QCompleter.PopupCompletion)
                address_suggestions.setFilterMode(Qt.MatchContains)
                self.address_bar.setCompleter(address_suggestions)

    def clear_address_bar_completer(self):
        self.history_urls = []
        address_suggestions = QCompleter(self.history_urls)
        address_suggestions.setCompletionMode(QCompleter.PopupCompletion)
        address_suggestions.setFilterMode(Qt.MatchContains)
        self.address_bar.setCompleter(address_suggestions)

    def open_url_receiver(self, url):
        self.tab_add(url)

    def clear_cookies(self):
        self.tabs.currentWidget().page().profile().cookieStore().deleteAllCookies()

    # Settings of the browser
    def settings_management(self):
        self.settings_dialog = Settings()
        if self.settings_dialog.isVisible():
            self.settings_dialog.activateWindow()
        else:
            self.settings_dialog.show()

        self.settings_dialog.open_url_signal.connect(self.open_url_receiver)

    def history_management(self):
        self.history_dialog = HistoryManagement()
        if self.history_dialog.isVisible():
            self.history_dialog.activateWindow()
        else:
            self.history_dialog.show()

        self.history_dialog.open_url_signal.connect(self.open_url_receiver)
        self.history_dialog.clear_address_bar_completer_signal.connect(self.clear_address_bar_completer)
        self.history_dialog.clear_cookies_signal.connect(self.clear_cookies)

    def tab_add(self, web_address):
        web_view = QWebEngineView()

        private_browsing_status = self.basic_settings.read_private_browsing()
        if private_browsing_status == self.LangSetting.language.lang_no:
            profile = QWebEngineProfile('kBrowser', web_view)

            cache_path, storage_path = self.basic_settings.read_cache_storage_path()
            profile.setCachePath(cache_path)
            profile.setPersistentStoragePath(storage_path)

            profile_page = QWebEnginePage(profile, web_view)
            web_view.setPage(profile_page)

        download_folder = self.basic_settings.read_download_folder()
        web_view.page().profile().setDownloadPath(download_folder)

        http_language_code, _, _ = self.LangSetting.read_preferred_language_setting()
        web_view.page().profile().setHttpAcceptLanguage(http_language_code)

        web_view.setUrl(web_address)

        n = self.tabs.addTab(web_view, self.LangSetting.language.lang_new_tab)
        self.tabs.setCurrentIndex(n)

        self.web_signals(web_view)

    def load(self):
        if self.address_bar.text() == 'about:blank':
            web_address = QUrl('')
        # Recognize the address bar's text which has a space or has no dot as keywords and trigger a search.
        elif ' ' in self.address_bar.text() or '.' not in self.address_bar.text():
            _, enabled_search_engine_url = SearchEngines().read_enabled_search_engine()
            web_address = QUrl(f'{enabled_search_engine_url}{self.address_bar.text()}')
        # Enable or disable a mode that only permit https visits.
        else:
            web_address = self.address_bar.text()
            https_mode_status = self.basic_settings.read_https_mode()
            if https_mode_status == 'Yes':
                if '://' not in web_address:
                    web_address = f'https://{web_address}'
                web_address = QUrl(web_address)
                if web_address.scheme() == 'http':
                    web_address.setScheme('https')
            else:
                if '://' not in web_address:
                    web_address = f'http://{web_address}'
                web_address = QUrl(web_address)

        self.tabs.currentWidget().setUrl(web_address)

    def web_signals(self, web_view):
        # Enable full screen support when playing a video.
        web_view.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        # Update address bar after the url of a page is changed,
        web_view.page().urlChanged.connect(lambda web_address, web_view=web_view:
                                           self.update_address(web_address, web_view))
        # Show the title of a page on a tab.
        web_view.page().titleChanged.connect(lambda page_title, web_view=web_view:
                                             self.page_title_changed(page_title, web_view))

        web_view.page().titleChanged.connect(lambda page_title, web_view=web_view:
                                             self.update_address_bar_completer(page_title, web_view))
        # When private browsing status is disabled, every visit will be recorded into history database.
        private_browsing_status = self.basic_settings.read_private_browsing()
        if private_browsing_status == self.LangSetting.language.lang_no:
            web_view.page().titleChanged.connect(
                lambda page_title, web_view=web_view: self.visits_history.record_a_visit(page_title, web_view)
            )

        # Handle the error of a certificate.
        web_view.page().certificateError.connect(self.cert_dialog.cert_handling)
        # Handle the full screen request when playing a video.
        web_view.page().fullScreenRequested.connect(self.full_screen)
        # Handle a permission request.
        web_view.page().featurePermissionRequested.connect(
            lambda url, permission, web_view=web_view:
            self.permission_dialog.permission_handling(url, permission, web_view)
        )

        # If a link has an attribute "_blank", it will be opened in a new tab instead of a new window.
        web_view.page().newWindowRequested.connect(self.new_window)
        # Handle a request for a download.
        web_view.page().profile().downloadRequested.connect(
            lambda download, web_view=web_view:
            self.open_download(download, web_view)
        )

    def open_download(self, download, web_view):
        download.accept()

        # When private browsing status is disabled, every download will be recorded into history database.
        private_browsing_status = self.basic_settings.read_private_browsing()
        if private_browsing_status == self.LangSetting.language.lang_no:
            if download.state() == QWebEngineDownloadRequest.DownloadInProgress:
                self.downloads_history.record_a_download(download, web_view)

        download.receivedBytesChanged.connect(
            lambda download=download: self.downloads_dialog.download_progress(download)
        )

    def downloads_management(self):
        if self.downloads_dialog.isVisible():
            self.downloads_dialog.activateWindow()
        else:
            self.downloads_dialog.show()

    def full_screen(self, request):
        request.accept()
        if request.toggleOn() is True:
            self.tabs.setWindowFlags(Qt.Window)
            self.tabs.showFullScreen()
        else:
            self.tabs.setWindowFlags(Qt.Widget)
            self.tabs.showNormal()

    def tab_open(self, n):
        # Add a blank tab when double-clicking empty area of tab bar.
        if n == -1:
            self.tab_add('')

    def tab_change(self):
        web_address = self.tabs.currentWidget().url()
        self.update_address(web_address, self.tabs.currentWidget())

    def tab_close(self, n):
        if self.tabs.count() == 1:
            sys.exit()

        # Generally the close of a tab is just hiding the tab and the webengine process still runs in the background.
        # The function terminates an instance after closing a tab, except a webengine process related to a download.
        widget_info = self.tabs.widget(n)
        self.tabs.removeTab(n)
        widget_info.page().deleteLater()

    def update_address(self, web_address, web_view=None):
        if web_view != self.tabs.currentWidget():
            return
        self.address_bar.setText(web_address.toString())

    def page_title_changed(self, page_title, web_view):
        n = self.tabs.indexOf(web_view)
        self.tabs.setTabText(n, page_title)

    def stop(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Stop)

    def reload(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Reload)

    def back(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.tabs.currentWidget().page().triggerAction(QWebEnginePage.Forward)

    def new_window(self, request):
        web_address = request.requestedUrl()
        self.tab_add(web_address)

    def closeEvent(self, event):
        window_width = self.geometry().width()
        window_height = self.geometry().height()
        self.window_settings.save_window_size(window_width, window_height)


if __name__ == '__main__':
    app = QApplication([])
    widget = MainWindow()

    screen = app.primaryScreen()
    available_width = screen.availableSize().width()
    available_height = screen.availableSize().height()

    width, height, window_maximized_status = WindowSettings().read_window_size(available_width, available_height)
    widget.resize(width, height)
    if window_maximized_status is True:
        widget.setWindowState(Qt.WindowMaximized)

    widget.show()
    sys.exit(app.exec())
