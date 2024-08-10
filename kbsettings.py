from PySide6.QtCore import Qt, QDir, Signal
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget,
                               QDialog, QLabel, QStyle, QComboBox, QFileDialog, QScrollArea)

from kbsettingshandler import BasicSettings, SearchEngines, CertificatesPermissions, LangSetting


class Settings(QDialog):
    open_url_signal = Signal(str)

    def __init__(self):
        super(Settings, self).__init__()

        self.BasicSettings = BasicSettings()
        self.SearchEngines = SearchEngines()
        self.CertificatesPermissions = CertificatesPermissions()
        self.LangSetting = LangSetting()

        self.resize(960, 600)
        title = self.LangSetting.language.lang_settings
        self.setWindowTitle(title)

        font_title = QFont()
        font_title.setPointSize(10)

        translation_name, available_translations_list = self.LangSetting.read_ui_translation_setting()
        _, language_name, available_languages_list = self.LangSetting.read_preferred_language_setting()

        self.ui_translation_label = QLabel(self.LangSetting.language.lang_ui_translation)
        self.ui_translation_label.setFont(font_title)
        self.ui_translation = QComboBox()
        self.ui_translation.addItems(available_translations_list)
        self.ui_translation.setCurrentText(translation_name)

        self.preferred_language_label = QLabel(self.LangSetting.language.lang_preferred_language)
        self.preferred_language_label.setFont(font_title)
        self.preferred_language = QComboBox()
        self.preferred_language.addItems(available_languages_list)
        self.preferred_language.setCurrentText(language_name)

        private_browsing_status = self.BasicSettings.read_private_browsing()
        https_mode_status = self.BasicSettings.read_https_mode()
        download_folder_path = self.BasicSettings.read_download_folder()

        yes_or_no = [self.LangSetting.language.lang_yes, self.LangSetting.language.lang_no]
        self.private_browsing_label = QLabel(self.LangSetting.language.lang_private_browsing)
        self.private_browsing_label.setFont(font_title)
        self.private_browsing_description = QLabel(self.LangSetting.language.lang_new_setting_effective_note)
        self.private_browsing = QComboBox()
        self.private_browsing.addItems(yes_or_no)
        self.private_browsing.setCurrentText(private_browsing_status)

        self.https_mode_label = QLabel(self.LangSetting.language.lang_https_mode)
        self.https_mode_label.setFont(font_title)
        self.https_mode = QComboBox()
        self.https_mode.addItems(yes_or_no)
        self.https_mode.setCurrentText(https_mode_status)

        self.download_folder_label = QLabel(self.LangSetting.language.lang_download_folder)
        self.download_folder_label.setFont(font_title)
        self.download_folder = QLineEdit()
        self.download_folder.setText(download_folder_path)
        self.download_folder_action = QAction()
        self.download_folder_action.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.download_folder_action.triggered.connect(self.choose_download_folder)
        self.download_folder.addAction(self.download_folder_action, QLineEdit.TrailingPosition)

        self.search_engine_label = QLabel(self.LangSetting.language.lang_search_engine)
        self.search_engine_label.setFont(font_title)
        self.search_engine = QComboBox()

        search_engines_list = self.SearchEngines.read_search_engines()
        enabled_search_engine, _ = self.SearchEngines.read_enabled_search_engine()

        self.search_engine.addItems(search_engines_list)
        self.search_engine.setCurrentText(enabled_search_engine)

        self.certificates_section = QLabel(self.LangSetting.language.lang_certificates)
        self.certificates_section.setFont(font_title)

        certificates_status, certificates_accept_list, certificates_reject_list =\
            self.CertificatesPermissions.read_permission("Certificates")

        self.Certificates_status_label = QLabel(self.LangSetting.language.lang_ask_every_time_invalid_certificate)
        self.Certificates_status = QComboBox()
        self.Certificates_status.addItems(yes_or_no)
        self.Certificates_status.setCurrentText(certificates_status)

        self.Certificates_accept_label = QLabel(self.LangSetting.language.lang_accepted_certificates)
        self.Certificates_accept = QComboBox()
        self.Certificates_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if certificates_accept_list:
            self.Certificates_accept.addItems(certificates_accept_list)
            self.Certificates_accept_remove_button.setEnabled(True)
        else:
            self.Certificates_accept_remove_button.setEnabled(False)

        self.Certificates_reject_label = QLabel(self.LangSetting.language.lang_rejected_certificates)
        self.Certificates_reject = QComboBox()
        self.Certificates_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if certificates_reject_list:
            self.Certificates_reject.addItems(certificates_reject_list)
            self.Certificates_reject_remove_button.setEnabled(True)
        else:
            self.Certificates_reject_remove_button.setEnabled(False)

        self.permissions_section = QLabel(self.LangSetting.language.lang_permissions)
        self.permissions_section.setFont(font_title)

        notifications_status, notifications_accept_list, notifications_reject_list = \
            self.CertificatesPermissions.read_permission("Notifications")

        self.Notifications_status_label = QLabel(self.LangSetting.language.lang_ask_every_time_notifications)
        self.Notifications_status = QComboBox()
        self.Notifications_status.addItems(yes_or_no)
        self.Notifications_status.setCurrentText(notifications_status)

        self.Notifications_accept_label = QLabel(self.LangSetting.language.lang_sites_notifications)
        self.Notifications_accept = QComboBox()
        self.Notifications_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if notifications_accept_list:
            self.Notifications_accept.addItems(notifications_accept_list)
            self.Notifications_accept_remove_button.setEnabled(True)
        else:
            self.Notifications_accept_remove_button.setEnabled(False)

        self.Notifications_reject_label = QLabel(self.LangSetting.language.lang_sites_no_notifications)
        self.Notifications_reject = QComboBox()
        self.Notifications_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if notifications_reject_list:
            self.Notifications_reject.addItems(notifications_reject_list)
            self.Notifications_reject_remove_button.setEnabled(True)
        else:
            self.Notifications_reject_remove_button.setEnabled(False)

        geolocation_status, geolocation_accept_list, geolocation_reject_list = \
            self.CertificatesPermissions.read_permission("Geolocation")

        self.Geolocation_status_label = QLabel(self.LangSetting.language.lang_ask_every_time_geolocation)
        self.Geolocation_status = QComboBox()
        self.Geolocation_status.addItems(yes_or_no)
        self.Geolocation_status.setCurrentText(geolocation_status)

        self.Geolocation_accept_label = QLabel(self.LangSetting.language.lang_sites_geolocation)
        self.Geolocation_accept = QComboBox()
        self.Geolocation_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if geolocation_accept_list:
            self.Geolocation_accept.addItems(geolocation_accept_list)
            self.Geolocation_accept_remove_button.setEnabled(True)
        else:
            self.Geolocation_accept_remove_button.setEnabled(False)

        self.Geolocation_reject_label = QLabel(self.LangSetting.language.lang_sites_no_geolocation)
        self.Geolocation_reject = QComboBox()
        self.Geolocation_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if geolocation_reject_list:
            self.Geolocation_reject.addItems(geolocation_reject_list)
            self.Geolocation_reject_remove_button.setEnabled(True)
        else:
            self.Geolocation_reject_remove_button.setEnabled(False)

        mediaaudiocapture_status, mediaaudiocapture_accept_list, mediaaudiocapture_reject_list = \
            self.CertificatesPermissions.read_permission("MediaAudioCapture")

        self.MediaAudioCapture_status_label = QLabel(self.LangSetting.language.lang_ask_every_time_microphone)
        self.MediaAudioCapture_status = QComboBox()
        self.MediaAudioCapture_status.addItems(yes_or_no)
        self.MediaAudioCapture_status.setCurrentText(mediaaudiocapture_status)

        self.MediaAudioCapture_accept_label = QLabel(self.LangSetting.language.lang_sites_microphone)
        self.MediaAudioCapture_accept = QComboBox()
        self.MediaAudioCapture_accept_remove_button = QPushButton('Remove')
        if mediaaudiocapture_accept_list:
            self.MediaAudioCapture_accept.addItems(mediaaudiocapture_accept_list)
            self.MediaAudioCapture_accept_remove_button.setEnabled(True)
        else:
            self.MediaAudioCapture_accept_remove_button.setEnabled(False)

        self.MediaAudioCapture_reject_label = QLabel(self.LangSetting.language.lang_sites_no_microphone)
        self.MediaAudioCapture_reject = QComboBox()
        self.MediaAudioCapture_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if mediaaudiocapture_reject_list:
            self.MediaAudioCapture_reject.addItems(mediaaudiocapture_reject_list)
            self.MediaAudioCapture_reject_remove_button.setEnabled(True)
        else:
            self.MediaAudioCapture_reject_remove_button.setEnabled(False)

        mediavideocapture_status, mediavideocapture_accept_list, mediavideocapture_reject_list = \
            self.CertificatesPermissions.read_permission("MediaVideoCapture")

        self.MediaVideoCapture_status_label = QLabel(self.LangSetting.language.lang_ask_every_time_camera)
        self.MediaVideoCapture_status = QComboBox()
        self.MediaVideoCapture_status.addItems(yes_or_no)
        self.MediaVideoCapture_status.setCurrentText(mediavideocapture_status)

        self.MediaVideoCapture_accept_label = QLabel(self.LangSetting.language.lang_sites_camera)
        self.MediaVideoCapture_accept = QComboBox()
        self.MediaVideoCapture_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if mediavideocapture_accept_list:
            self.MediaVideoCapture_accept.addItems(mediavideocapture_accept_list)
            self.MediaVideoCapture_accept_remove_button.setEnabled(True)
        else:
            self.MediaVideoCapture_accept_remove_button.setEnabled(False)

        self.MediaVideoCapture_reject_label = QLabel(self.LangSetting.language.lang_sites_no_camera)
        self.MediaVideoCapture_reject = QComboBox()
        self.MediaVideoCapture_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if mediavideocapture_reject_list:
            self.MediaVideoCapture_reject.addItems(mediavideocapture_reject_list)
            self.MediaVideoCapture_reject_remove_button.setEnabled(True)
        else:
            self.MediaVideoCapture_reject_remove_button.setEnabled(False)

        mediaaudiovideocapture_status, mediaaudiovideocapture_accept_list, mediaaudiovideocapture_reject_list = \
            self.CertificatesPermissions.read_permission("MediaAudioVideoCapture")

        self.MediaAudioVideoCapture_status_label = QLabel(
            self.LangSetting.language.lang_ask_every_time_microphone_camera
        )
        self.MediaAudioVideoCapture_status = QComboBox()
        self.MediaAudioVideoCapture_status.addItems(yes_or_no)
        self.MediaAudioVideoCapture_status.setCurrentText(mediaaudiovideocapture_status)

        self.MediaAudioVideoCapture_accept_label = QLabel(self.LangSetting.language.lang_sites_microphone_camera)
        self.MediaAudioVideoCapture_accept = QComboBox()
        self.MediaAudioVideoCapture_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if mediaaudiovideocapture_accept_list:
            self.MediaAudioVideoCapture_accept.addItems(mediaaudiovideocapture_accept_list)
            self.MediaAudioVideoCapture_accept_remove_button.setEnabled(True)
        else:
            self.MediaAudioVideoCapture_accept_remove_button.setEnabled(False)

        self.MediaAudioVideoCapture_reject_label = QLabel(self.LangSetting.language.lang_sites_no_microphone_camera)
        self.MediaAudioVideoCapture_reject = QComboBox()
        self.MediaAudioVideoCapture_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if mediaaudiovideocapture_reject_list:
            self.MediaAudioVideoCapture_reject.addItems(mediaaudiovideocapture_reject_list)
            self.MediaAudioVideoCapture_reject_remove_button.setEnabled(True)
        else:
            self.MediaAudioVideoCapture_reject_remove_button.setEnabled(False)

        mouselock_status, mouselock_accept_list, mouselock_reject_list = \
            self.CertificatesPermissions.read_permission("MouseLock")

        self.MouseLock_status_label = QLabel(self.LangSetting.language.lang_ask_every_time_mouse_lock)
        self.MouseLock_status = QComboBox()
        self.MouseLock_status.addItems(yes_or_no)
        self.MouseLock_status.setCurrentText(mouselock_status)

        self.MouseLock_accept_label = QLabel(self.LangSetting.language.lang_sites_mouse_lock)
        self.MouseLock_accept = QComboBox()
        self.MouseLock_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if mouselock_accept_list:
            self.MouseLock_accept.addItems(mouselock_accept_list)
            self.MouseLock_accept_remove_button.setEnabled(True)
        else:
            self.MouseLock_accept_remove_button.setEnabled(False)

        self.MouseLock_reject_label = QLabel(self.LangSetting.language.lang_sites_no_mouse_lock)
        self.MouseLock_reject = QComboBox()
        self.MouseLock_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if mouselock_reject_list:
            self.MouseLock_reject.addItems(mouselock_reject_list)
            self.MouseLock_reject_remove_button.setEnabled(True)
        else:
            self.MouseLock_reject_remove_button.setEnabled(False)

        desktopvideocapture_status, desktopvideocapture_accept_list, desktopvideocapture_reject_list = \
            self.CertificatesPermissions.read_permission("DesktopVideoCapture")

        self.DesktopVideoCapture_status_label = QLabel(
            self.LangSetting.language.lang_ask_every_time_desktop_video_capture
        )
        self.DesktopVideoCapture_status = QComboBox()
        self.DesktopVideoCapture_status.addItems(yes_or_no)
        self.DesktopVideoCapture_status.setCurrentText(desktopvideocapture_status)

        self.DesktopVideoCapture_accept_label = QLabel(self.LangSetting.language.lang_sites_desktop_video_capture)
        self.DesktopVideoCapture_accept = QComboBox()
        self.DesktopVideoCapture_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if desktopvideocapture_accept_list:
            self.DesktopVideoCapture_accept.addItems(desktopvideocapture_accept_list)
            self.DesktopVideoCapture_accept_remove_button.setEnabled(True)
        else:
            self.DesktopVideoCapture_accept_remove_button.setEnabled(False)

        self.DesktopVideoCapture_reject_label = QLabel(self.LangSetting.language.lang_sites_no_desktop_video_capture)
        self.DesktopVideoCapture_reject = QComboBox()
        self.DesktopVideoCapture_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if desktopvideocapture_reject_list:
            self.DesktopVideoCapture_reject.addItems(desktopvideocapture_reject_list)
            self.DesktopVideoCapture_reject_remove_button.setEnabled(True)
        else:
            self.DesktopVideoCapture_reject_remove_button.setEnabled(False)

        desktopaudiovideocapture_status, desktopaudiovideocapture_accept_list, desktopaudiovideocapture_reject_list = \
            self.CertificatesPermissions.read_permission("DesktopAudioVideoCapture")

        self.DesktopAudioVideoCapture_status_label = QLabel(
            self.LangSetting.language.lang_ask_every_time_desktop_audio_video_capture
        )
        self.DesktopAudioVideoCapture_status = QComboBox()
        self.DesktopAudioVideoCapture_status.addItems(yes_or_no)
        self.DesktopAudioVideoCapture_status.setCurrentText(desktopaudiovideocapture_status)

        self.DesktopAudioVideoCapture_accept_label = QLabel(
            self.LangSetting.language.lang_sites_desktop_audio_video_capture
        )
        self.DesktopAudioVideoCapture_accept = QComboBox()
        self.DesktopAudioVideoCapture_accept_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if desktopaudiovideocapture_accept_list:
            self.DesktopAudioVideoCapture_accept.addItems(desktopaudiovideocapture_accept_list)
            self.DesktopAudioVideoCapture_accept_remove_button.setEnabled(True)
        else:
            self.DesktopAudioVideoCapture_accept_remove_button.setEnabled(False)

        self.DesktopAudioVideoCapture_reject_label = QLabel(
            self.LangSetting.language.lang_sites_no_desktop_audio_video_capture
        )
        self.DesktopAudioVideoCapture_reject = QComboBox()
        self.DesktopAudioVideoCapture_reject_remove_button = QPushButton(self.LangSetting.language.lang_remove)
        if desktopaudiovideocapture_reject_list:
            self.DesktopAudioVideoCapture_reject.addItems(desktopaudiovideocapture_reject_list)
            self.DesktopAudioVideoCapture_reject_remove_button.setEnabled(True)
        else:
            self.DesktopAudioVideoCapture_reject_remove_button.setEnabled(False)

        # The browser's version
        self.browser_name = QLabel('kBrowser')
        self.browser_version = QLabel('1.0')
        self.browser_license = QLabel(
            'kBrowser is released as free software under GNU General Public License version 3.'
        )
        self.browser_description = QLabel(
            'The software is based on Chromium and developed using Python and PySide6.'
        )
        self.qt_license = QLabel(
            'kBrowser uses Qt libraries dynamically under GNU Lesser General Public License version 3.\n'
            'There is no modification in Qt source code.'
        )
        self.browser_release = QLabel(
            'For more information, please visit <a href="https://github.com/yikejiang/kBrowser">https://github.com/yikejiang/kBrowser</a>.'
        )
        self.browser_name.setFixedHeight(40)
        self.browser_version.setFixedHeight(30)
        self.browser_license.setFixedHeight(30)
        self.browser_description.setFixedHeight(30)
        self.qt_license.setFixedHeight(50)
        self.browser_release.setFixedHeight(30)

        font_browser_name = QFont()
        font_browser_name.setPointSize(15)
        self.browser_name.setFont(font_browser_name)

        self.browser_name.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.browser_version.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.browser_license.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.browser_description.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.qt_license.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.browser_release.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout_basic = QVBoxLayout()
        self.layout_certificates = QVBoxLayout()
        self.layout_permissions = QVBoxLayout()
        self.layout_about = QVBoxLayout()
        self.dialog = QTabWidget()
        self.layout.addWidget(self.dialog)

        self.layout_basic.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_certificates.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_permissions.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.basic_area = QWidget()
        self.certificates_area = QWidget()
        self.permissions_area = QWidget()
        self.about_area = QWidget()

        self.basic_area.setLayout(self.layout_basic)
        self.certificates_area.setLayout(self.layout_certificates)
        self.permissions_area.setLayout(self.layout_permissions)
        self.about_area.setLayout(self.layout_about)

        self.layout_version = QVBoxLayout()
        self.layout_version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_about.addLayout(self.layout_version)

        # Scrollbar
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.permissions_area)

        # Sections of main layout
        self.dialog.addTab(self.basic_area, self.LangSetting.language.lang_basic_settings)
        self.dialog.addTab(self.certificates_area, self.LangSetting.language.lang_certificates)
        self.dialog.addTab(self.scroll, self.LangSetting.language.lang_permissions)
        self.dialog.addTab(self.about_area, self.LangSetting.language.lang_about)

        # Layout of basic settings
        self.layout_ui_translation = QHBoxLayout()
        self.layout_basic.addLayout(self.layout_ui_translation)

        self.layout_ui_translation.addWidget(self.ui_translation_label)
        self.layout_ui_translation.addWidget(self.ui_translation)

        self.layout_preferred_language = QHBoxLayout()
        self.layout_basic.addLayout(self.layout_preferred_language)

        self.layout_preferred_language.addWidget(self.preferred_language_label)
        self.layout_preferred_language.addWidget(self.preferred_language)

        self.layout_private_browsing = QHBoxLayout()
        self.layout_basic.addLayout(self.layout_private_browsing)

        self.layout_private_browsing.addWidget(self.private_browsing_label)
        self.layout_private_browsing.addWidget(self.private_browsing_description)
        self.layout_private_browsing.addWidget(self.private_browsing)

        self.layout_https_mode = QHBoxLayout()
        self.layout_basic.addLayout(self.layout_https_mode)

        self.layout_https_mode.addWidget(self.https_mode_label)
        self.layout_https_mode.addWidget(self.https_mode)

        self.layout_download_folder = QHBoxLayout()
        self.layout_basic.addLayout(self.layout_download_folder)

        self.layout_download_folder.addWidget(self.download_folder_label)
        self.layout_download_folder.addWidget(self.download_folder)

        # Layout of search engines
        self.layout_search_engine = QHBoxLayout()
        self.layout_basic.addLayout(self.layout_search_engine)

        self.layout_search_engine.addWidget(self.search_engine_label)
        self.layout_search_engine.addWidget(self.search_engine)

        # Layout of certificate management
        self.layout_Certificates_status = QHBoxLayout()
        self.layout_Certificates_accept = QHBoxLayout()
        self.layout_Certificates_reject = QHBoxLayout()

        self.layout_certificates.addLayout(self.layout_Certificates_status)
        self.layout_certificates.addLayout(self.layout_Certificates_accept)
        self.layout_certificates.addLayout(self.layout_Certificates_reject)

        self.layout_Certificates_status.addWidget(self.Certificates_status_label)
        self.layout_Certificates_status.addWidget(self.Certificates_status)

        self.layout_Certificates_accept.addWidget(self.Certificates_accept_label)
        self.layout_Certificates_accept.addWidget(self.Certificates_accept)
        self.layout_Certificates_accept.addWidget(self.Certificates_accept_remove_button)

        self.layout_Certificates_reject.addWidget(self.Certificates_reject_label)
        self.layout_Certificates_reject.addWidget(self.Certificates_reject)
        self.layout_Certificates_reject.addWidget(self.Certificates_reject_remove_button)

        # Layout of permission management
        self.layout_Notifications_status = QHBoxLayout()
        self.layout_Notifications_accept = QHBoxLayout()
        self.layout_Notifications_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_Notifications_status)
        self.layout_permissions.addLayout(self.layout_Notifications_accept)
        self.layout_permissions.addLayout(self.layout_Notifications_reject)

        self.layout_Notifications_status.addWidget(self.Notifications_status_label)
        self.layout_Notifications_status.addWidget(self.Notifications_status)

        self.layout_Notifications_accept.addWidget(self.Notifications_accept_label)
        self.layout_Notifications_accept.addWidget(self.Notifications_accept)
        self.layout_Notifications_accept.addWidget(self.Notifications_accept_remove_button)

        self.layout_Notifications_reject.addWidget(self.Notifications_reject_label)
        self.layout_Notifications_reject.addWidget(self.Notifications_reject)
        self.layout_Notifications_reject.addWidget(self.Notifications_reject_remove_button)

        self.layout_Geolocation_status = QHBoxLayout()
        self.layout_Geolocation_accept = QHBoxLayout()
        self.layout_Geolocation_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_Geolocation_status)
        self.layout_permissions.addLayout(self.layout_Geolocation_accept)
        self.layout_permissions.addLayout(self.layout_Geolocation_reject)

        self.layout_Geolocation_status.addWidget(self.Geolocation_status_label)
        self.layout_Geolocation_status.addWidget(self.Geolocation_status)

        self.layout_Geolocation_accept.addWidget(self.Geolocation_accept_label)
        self.layout_Geolocation_accept.addWidget(self.Geolocation_accept)
        self.layout_Geolocation_accept.addWidget(self.Geolocation_accept_remove_button)

        self.layout_Geolocation_reject.addWidget(self.Geolocation_reject_label)
        self.layout_Geolocation_reject.addWidget(self.Geolocation_reject)
        self.layout_Geolocation_reject.addWidget(self.Geolocation_reject_remove_button)

        self.layout_MediaAudioCapture_status = QHBoxLayout()
        self.layout_MediaAudioCapture_accept = QHBoxLayout()
        self.layout_MediaAudioCapture_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_MediaAudioCapture_status)
        self.layout_permissions.addLayout(self.layout_MediaAudioCapture_accept)
        self.layout_permissions.addLayout(self.layout_MediaAudioCapture_reject)

        self.layout_MediaAudioCapture_status.addWidget(self.MediaAudioCapture_status_label)
        self.layout_MediaAudioCapture_status.addWidget(self.MediaAudioCapture_status)

        self.layout_MediaAudioCapture_accept.addWidget(self.MediaAudioCapture_accept_label)
        self.layout_MediaAudioCapture_accept.addWidget(self.MediaAudioCapture_accept)
        self.layout_MediaAudioCapture_accept.addWidget(self.MediaAudioCapture_accept_remove_button)

        self.layout_MediaAudioCapture_reject.addWidget(self.MediaAudioCapture_reject_label)
        self.layout_MediaAudioCapture_reject.addWidget(self.MediaAudioCapture_reject)
        self.layout_MediaAudioCapture_reject.addWidget(self.MediaAudioCapture_reject_remove_button)

        self.layout_MediaVideoCapture_status = QHBoxLayout()
        self.layout_MediaVideoCapture_accept = QHBoxLayout()
        self.layout_MediaVideoCapture_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_MediaVideoCapture_status)
        self.layout_permissions.addLayout(self.layout_MediaVideoCapture_accept)
        self.layout_permissions.addLayout(self.layout_MediaVideoCapture_reject)

        self.layout_MediaVideoCapture_status.addWidget(self.MediaVideoCapture_status_label)
        self.layout_MediaVideoCapture_status.addWidget(self.MediaVideoCapture_status)

        self.layout_MediaVideoCapture_accept.addWidget(self.MediaVideoCapture_accept_label)
        self.layout_MediaVideoCapture_accept.addWidget(self.MediaVideoCapture_accept)
        self.layout_MediaVideoCapture_accept.addWidget(self.MediaVideoCapture_accept_remove_button)

        self.layout_MediaVideoCapture_reject.addWidget(self.MediaVideoCapture_reject_label)
        self.layout_MediaVideoCapture_reject.addWidget(self.MediaVideoCapture_reject)
        self.layout_MediaVideoCapture_reject.addWidget(self.MediaVideoCapture_reject_remove_button)

        self.layout_MediaAudioVideoCapture_status = QHBoxLayout()
        self.layout_MediaAudioVideoCapture_accept = QHBoxLayout()
        self.layout_MediaAudioVideoCapture_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_MediaAudioVideoCapture_status)
        self.layout_permissions.addLayout(self.layout_MediaAudioVideoCapture_accept)
        self.layout_permissions.addLayout(self.layout_MediaAudioVideoCapture_reject)

        self.layout_MediaAudioVideoCapture_status.addWidget(self.MediaAudioVideoCapture_status_label)
        self.layout_MediaAudioVideoCapture_status.addWidget(self.MediaAudioVideoCapture_status)

        self.layout_MediaAudioVideoCapture_accept.addWidget(self.MediaAudioVideoCapture_accept_label)
        self.layout_MediaAudioVideoCapture_accept.addWidget(self.MediaAudioVideoCapture_accept)
        self.layout_MediaAudioVideoCapture_accept.addWidget(self.MediaAudioVideoCapture_accept_remove_button)

        self.layout_MediaAudioVideoCapture_reject.addWidget(self.MediaAudioVideoCapture_reject_label)
        self.layout_MediaAudioVideoCapture_reject.addWidget(self.MediaAudioVideoCapture_reject)
        self.layout_MediaAudioVideoCapture_reject.addWidget(self.MediaAudioVideoCapture_reject_remove_button)

        self.layout_MouseLock_status = QHBoxLayout()
        self.layout_MouseLock_accept = QHBoxLayout()
        self.layout_MouseLock_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_MouseLock_status)
        self.layout_permissions.addLayout(self.layout_MouseLock_accept)
        self.layout_permissions.addLayout(self.layout_MouseLock_reject)

        self.layout_MouseLock_status.addWidget(self.MouseLock_status_label)
        self.layout_MouseLock_status.addWidget(self.MouseLock_status)

        self.layout_MouseLock_accept.addWidget(self.MouseLock_accept_label)
        self.layout_MouseLock_accept.addWidget(self.MouseLock_accept)
        self.layout_MouseLock_accept.addWidget(self.MouseLock_accept_remove_button)

        self.layout_MouseLock_reject.addWidget(self.MouseLock_reject_label)
        self.layout_MouseLock_reject.addWidget(self.MouseLock_reject)
        self.layout_MouseLock_reject.addWidget(self.MouseLock_reject_remove_button)

        self.layout_DesktopVideoCapture_status = QHBoxLayout()
        self.layout_DesktopVideoCapture_accept = QHBoxLayout()
        self.layout_DesktopVideoCapture_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_DesktopVideoCapture_status)
        self.layout_permissions.addLayout(self.layout_DesktopVideoCapture_accept)
        self.layout_permissions.addLayout(self.layout_DesktopVideoCapture_reject)

        self.layout_DesktopVideoCapture_status.addWidget(self.DesktopVideoCapture_status_label)
        self.layout_DesktopVideoCapture_status.addWidget(self.DesktopVideoCapture_status)

        self.layout_DesktopVideoCapture_accept.addWidget(self.DesktopVideoCapture_accept_label)
        self.layout_DesktopVideoCapture_accept.addWidget(self.DesktopVideoCapture_accept)
        self.layout_DesktopVideoCapture_accept.addWidget(self.DesktopVideoCapture_accept_remove_button)

        self.layout_DesktopVideoCapture_reject.addWidget(self.DesktopVideoCapture_reject_label)
        self.layout_DesktopVideoCapture_reject.addWidget(self.DesktopVideoCapture_reject)
        self.layout_DesktopVideoCapture_reject.addWidget(self.DesktopVideoCapture_reject_remove_button)

        self.layout_DesktopAudioVideoCapture_status = QHBoxLayout()
        self.layout_DesktopAudioVideoCapture_accept = QHBoxLayout()
        self.layout_DesktopAudioVideoCapture_reject = QHBoxLayout()

        self.layout_permissions.addLayout(self.layout_DesktopAudioVideoCapture_status)
        self.layout_permissions.addLayout(self.layout_DesktopAudioVideoCapture_accept)
        self.layout_permissions.addLayout(self.layout_DesktopAudioVideoCapture_reject)

        self.layout_DesktopAudioVideoCapture_status.addWidget(self.DesktopAudioVideoCapture_status_label)
        self.layout_DesktopAudioVideoCapture_status.addWidget(self.DesktopAudioVideoCapture_status)

        self.layout_DesktopAudioVideoCapture_accept.addWidget(self.DesktopAudioVideoCapture_accept_label)
        self.layout_DesktopAudioVideoCapture_accept.addWidget(self.DesktopAudioVideoCapture_accept)
        self.layout_DesktopAudioVideoCapture_accept.addWidget(self.DesktopAudioVideoCapture_accept_remove_button)

        self.layout_DesktopAudioVideoCapture_reject.addWidget(self.DesktopAudioVideoCapture_reject_label)
        self.layout_DesktopAudioVideoCapture_reject.addWidget(self.DesktopAudioVideoCapture_reject)
        self.layout_DesktopAudioVideoCapture_reject.addWidget(self.DesktopAudioVideoCapture_reject_remove_button)

        self.layout_version.addWidget(self.browser_name)
        self.layout_version.addWidget(self.browser_version)
        self.layout_version.addWidget(self.browser_license)
        self.layout_version.addWidget(self.browser_description)
        self.layout_version.addWidget(self.qt_license)
        self.layout_version.addWidget(self.browser_release)

        self.Certificates_accept_remove_button.clicked.connect(self.certificates_accept_remove)
        self.Certificates_reject_remove_button.clicked.connect(self.certificates_reject_remove)
        self.Notifications_accept_remove_button.clicked.connect(self.notifications_accept_remove)
        self.Notifications_reject_remove_button.clicked.connect(self.notifications_reject_remove)
        self.Geolocation_accept_remove_button.clicked.connect(self.geolocation_accept_remove)
        self.Geolocation_reject_remove_button.clicked.connect(self.geolocation_reject_remove)
        self.MediaAudioCapture_accept_remove_button.clicked.connect(self.mediaaudiocapture_accept_remove)
        self.MediaAudioCapture_reject_remove_button.clicked.connect(self.mediaaudiocapture_reject_remove)
        self.MediaVideoCapture_accept_remove_button.clicked.connect(self.mediavideocapture_accept_remove)
        self.MediaVideoCapture_reject_remove_button.clicked.connect(self.mediavideocapture_reject_remove)
        self.MediaAudioVideoCapture_accept_remove_button.clicked.connect(self.mediaaudiovideocapture_accept_remove)
        self.MediaAudioVideoCapture_reject_remove_button.clicked.connect(self.mediaaudiovideocapture_reject_remove)
        self.MouseLock_accept_remove_button.clicked.connect(self.mouselock_accept_remove)
        self.MouseLock_reject_remove_button.clicked.connect(self.mouselock_reject_remove)
        self.DesktopVideoCapture_accept_remove_button.clicked.connect(self.desktopvideocapture_accept_remove)
        self.DesktopVideoCapture_reject_remove_button.clicked.connect(self.desktopvideocapture_reject_remove)
        self.DesktopAudioVideoCapture_accept_remove_button.clicked.connect(self.desktopaudiovideocapture_accept_remove)
        self.DesktopAudioVideoCapture_reject_remove_button.clicked.connect(self.desktopaudiovideocapture_reject_remove)

        self.Certificates_status.currentTextChanged.connect(
            lambda option, permission_type='Certificates': self.permission_status_changed(option, permission_type)
        )
        self.Notifications_status.currentTextChanged.connect(
            lambda option, permission_type='Notifications': self.permission_status_changed(option, permission_type)
        )
        self.Geolocation_status.currentTextChanged.connect(
            lambda option, permission_type='Geolocation': self.permission_status_changed(option, permission_type)
        )
        self.MediaAudioCapture_status.currentTextChanged.connect(
            lambda option, permission_type='MediaAudioCapture': self.permission_status_changed(option, permission_type)
        )
        self.MediaVideoCapture_status.currentTextChanged.connect(
            lambda option, permission_type='MediaVideoCapture': self.permission_status_changed(option, permission_type)
        )
        self.MediaAudioVideoCapture_status.currentTextChanged.connect(
            lambda option, permission_type='MediaAudioVideoCapture':
            self.permission_status_changed(option, permission_type)
        )
        self.MouseLock_status.currentTextChanged.connect(
            lambda option, permission_type='MouseLock': self.permission_status_changed(option, permission_type)
        )
        self.DesktopVideoCapture_status.currentTextChanged.connect(
            lambda option, permission_type='DesktopVideoCapture':
            self.permission_status_changed(option, permission_type)
        )
        self.DesktopAudioVideoCapture_status.currentTextChanged.connect(
            lambda option, permission_type='DesktopAudioVideoCapture':
            self.permission_status_changed(option, permission_type)
        )

        self.ui_translation.currentTextChanged.connect(
            lambda option: self.LangSetting.change_ui_translation_setting(option)
        )
        self.preferred_language.currentTextChanged.connect(
            lambda option: self.LangSetting.change_preferred_language_setting(option)
        )

        self.private_browsing.currentTextChanged.connect(
            lambda option, item_type='private_browsing': self.basic_setting_status_changed(option, item_type)
        )
        self.https_mode.currentTextChanged.connect(
            lambda option, item_type='https_mode': self.basic_setting_status_changed(option, item_type)
        )

        self.search_engine.currentTextChanged.connect(self.search_engine_changed)

        self.download_folder.textChanged.connect(self.download_folder_changed)

        self.browser_release.linkActivated.connect(self.send_signal)

    def send_signal(self, url):
        self.open_url_signal.emit(url)

    def choose_download_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, self.LangSetting.language.lang_choose_download_folder, QDir.homePath(), QFileDialog.ShowDirsOnly
        )
        if folder:
            self.download_folder.setText(folder)

    def basic_setting_status_changed(self, option, item_type):
        if option == self.LangSetting.language.lang_yes:
            self.BasicSettings.enable_basic_setting(item_type)
        if option == self.LangSetting.language.lang_no:
            self.BasicSettings.disable_basic_setting(item_type)

    def search_engine_changed(self, option):
        enabled_search_engine, _ = self.SearchEngines.read_enabled_search_engine()
        self.SearchEngines.disable_search_engine(enabled_search_engine)
        self.SearchEngines.enable_search_engine(option)

    def download_folder_changed(self, path):
        self.BasicSettings.change_download_folder(path)

    def permission_status_changed(self, option, permission_type):
        if option == self.LangSetting.language.lang_yes:
            self.CertificatesPermissions.enable_permission(permission_type)
        if option == self.LangSetting.language.lang_no:
            self.CertificatesPermissions.disable_permission(permission_type)

    # Certificates
    def certificates_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'Certificates', self.Certificates_accept.currentText()
        )
        self.Certificates_accept.removeItem(
            self.Certificates_accept.findText(self.Certificates_accept.currentText())
        )
        if self.Certificates_accept.count() == 0:
            self.Certificates_accept_remove_button.setEnabled(False)

    def certificates_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'Certificates', self.Certificates_reject.currentText()
        )
        self.Certificates_reject.removeItem(
            self.Certificates_reject.findText(self.Certificates_reject.currentText())
        )
        if self.Certificates_reject.count() == 0:
            self.Certificates_reject_remove_button.setEnabled(False)

    # Notifications
    def notifications_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'Notifications', self.Notifications_accept.currentText()
        )
        self.Notifications_accept.removeItem(
            self.Notifications_accept.findText(self.Notifications_accept.currentText())
        )
        if self.Notifications_accept.count() == 0:
            self.Notifications_accept_remove_button.setEnabled(False)

    def notifications_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'Notifications', self.Notifications_reject.currentText()
        )
        self.Notifications_reject.removeItem(
            self.Notifications_reject.findText(self.Notifications_reject.currentText())
        )
        if self.Notifications_reject.count() == 0:
            self.Notifications_reject_remove_button.setEnabled(False)

    # Geolocation
    def geolocation_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'Geolocation', self.Geolocation_accept.currentText()
        )
        self.Geolocation_accept.removeItem(
            self.Geolocation_accept.findText(self.Geolocation_accept.currentText())
        )
        if self.Geolocation_accept.count() == 0:
            self.Geolocation_accept_remove_button.setEnabled(False)

    def geolocation_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'Geolocation', self.Geolocation_reject.currentText()
        )
        self.Geolocation_reject.removeItem(
            self.Geolocation_reject.findText(self.Geolocation_reject.currentText())
        )
        if self.Geolocation_reject.count() == 0:
            self.Geolocation_reject_remove_button.setEnabled(False)

    # MediaAudioCapture
    def mediaaudiocapture_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'MediaAudioCapture', self.MediaAudioCapture_accept.currentText()
        )
        self.MediaAudioCapture_accept.removeItem(
            self.MediaAudioCapture_accept.findText(self.MediaAudioCapture_accept.currentText())
        )
        if self.MediaAudioCapture_accept.count() == 0:
            self.MediaAudioCapture_accept_remove_button.setEnabled(False)

    def mediaaudiocapture_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'MediaAudioCapture', self.MediaAudioCapture_reject.currentText()
        )
        self.MediaAudioCapture_reject.removeItem(
            self.MediaAudioCapture_reject.findText(self.MediaAudioCapture_reject.currentText())
        )
        if self.MediaAudioCapture_reject.count() == 0:
            self.MediaAudioCapture_reject_remove_button.setEnabled(False)

    # MediaVideoCapture
    def mediavideocapture_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'MediaVideoCapture', self.MediaVideoCapture_accept.currentText()
        )
        self.MediaVideoCapture_accept.removeItem(
            self.MediaVideoCapture_accept.findText(self.MediaVideoCapture_accept.currentText())
        )
        if self.MediaVideoCapture_accept.count() == 0:
            self.MediaVideoCapture_accept_remove_button.setEnabled(False)

    def mediavideocapture_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'MediaVideoCapture', self.MediaVideoCapture_reject.currentText()
        )
        self.MediaVideoCapture_reject.removeItem(
            self.MediaVideoCapture_reject.findText(self.MediaVideoCapture_reject.currentText())
        )
        if self.MediaVideoCapture_reject.count() == 0:
            self.MediaVideoCapture_reject_remove_button.setEnabled(False)

    # MediaAudioVideoCapture
    def mediaaudiovideocapture_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'MediaAudioVideoCapture', self.MediaAudioVideoCapture_accept.currentText()
        )
        self.MediaAudioVideoCapture_accept.removeItem(
            self.MediaAudioVideoCapture_accept.findText(self.MediaAudioVideoCapture_accept.currentText())
        )
        if self.MediaAudioVideoCapture_accept.count() == 0:
            self.MediaAudioVideoCapture_accept_remove_button.setEnabled(False)

    def mediaaudiovideocapture_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'MediaAudioVideoCapture', self.MediaAudioVideoCapture_reject.currentText()
        )
        self.MediaAudioVideoCapture_reject.removeItem(
            self.MediaAudioVideoCapture_reject.findText(self.MediaAudioVideoCapture_reject.currentText())
        )
        if self.MediaAudioVideoCapture_reject.count() == 0:
            self.MediaAudioVideoCapture_reject_remove_button.setEnabled(False)

    # MouseLock
    def mouselock_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'MouseLock', self.MouseLock_accept.currentText()
        )
        self.MouseLock_accept.removeItem(
            self.MouseLock_accept.findText(self.MouseLock_accept.currentText())
        )
        if self.MouseLock_accept.count() == 0:
            self.MouseLock_accept_remove_button.setEnabled(False)

    def mouselock_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'MouseLock', self.MouseLock_reject.currentText()
        )
        self.MouseLock_reject.removeItem(
            self.MouseLock_reject.findText(self.MouseLock_reject.currentText())
        )
        if self.MouseLock_reject.count() == 0:
            self.MouseLock_reject_remove_button.setEnabled(False)

    # DesktopVideoCapture
    def desktopvideocapture_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'DesktopVideoCapture', self.DesktopVideoCapture_accept.currentText()
        )
        self.DesktopVideoCapture_accept.removeItem(
            self.DesktopVideoCapture_accept.findText(self.DesktopVideoCapture_accept.currentText())
        )
        if self.DesktopVideoCapture_accept.count() == 0:
            self.DesktopVideoCapture_accept_remove_button.setEnabled(False)

    def desktopvideocapture_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'DesktopVideoCapture', self.DesktopVideoCapture_reject.currentText()
        )
        self.DesktopVideoCapture_reject.removeItem(
            self.DesktopVideoCapture_reject.findText(self.DesktopVideoCapture_reject.currentText())
        )
        if self.DesktopVideoCapture_reject.count() == 0:
            self.DesktopVideoCapture_reject_remove_button.setEnabled(False)

    # DesktopAudioVideoCapture
    def desktopaudiovideocapture_accept_remove(self):
        self.CertificatesPermissions.remove_from_accept(
            'DesktopAudioVideoCapture', self.DesktopAudioVideoCapture_accept.currentText()
        )
        self.DesktopAudioVideoCapture_accept.removeItem(
            self.DesktopAudioVideoCapture_accept.findText(self.DesktopAudioVideoCapture_accept.currentText())
        )
        if self.DesktopAudioVideoCapture_accept.count() == 0:
            self.DesktopAudioVideoCapture_accept_remove_button.setEnabled(False)

    def desktopaudiovideocapture_reject_remove(self):
        self.CertificatesPermissions.remove_from_reject(
            'DesktopAudioVideoCapture', self.DesktopAudioVideoCapture_reject.currentText()
        )
        self.DesktopAudioVideoCapture_reject.removeItem(
            self.DesktopAudioVideoCapture_reject.findText(self.DesktopAudioVideoCapture_reject.currentText())
        )
        if self.DesktopAudioVideoCapture_reject.count() == 0:
            self.DesktopAudioVideoCapture_reject_remove_button.setEnabled(False)
