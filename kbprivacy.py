from PySide6.QtWidgets import QGridLayout, QDialog, QPushButton, QLabel
from PySide6.QtWebEngineCore import QWebEnginePage

from kbsettingshandler import CertificatesPermissions, LangSetting


class PermissionDialog(QDialog):
    def __init__(self, title, label):
        super(PermissionDialog, self).__init__()
        self.resize(400, 200)

        self.LangSetting = LangSetting()

        self.setWindowTitle(title)

        self.dialog_label = QLabel(label)

        self.accept_once_button = QPushButton(self.LangSetting.language.lang_accept_once)
        self.reject_once_button = QPushButton(self.LangSetting.language.lang_reject_once)
        self.always_accept_button = QPushButton(self.LangSetting.language.lang_always_accept)
        self.always_reject_button = QPushButton(self.LangSetting.language.lang_always_reject)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.dialog_label, 0, 0, 1, 12)
        self.layout.addWidget(self.accept_once_button, 1, 0, 1, 3)
        self.layout.addWidget(self.reject_once_button, 1, 3, 1, 3)
        self.layout.addWidget(self.always_accept_button, 1, 6, 1, 3)
        self.layout.addWidget(self.always_reject_button, 1, 9, 1, 3)


class CertificatesHandler:
    def __init__(self):
        super(CertificatesHandler, self).__init__()
        self.LangSetting = LangSetting()
        self.permission_dialog = None

    def cert_handling(self, error):
        error.defer()

        url = error.url()

        permission_status, permission_accept_list, permission_reject_list = \
            CertificatesPermissions().read_permission("Certificates")
        if permission_status == "No":
            return
        else:
            check_permission_list = None
            if permission_accept_list:
                if url.toString() in permission_accept_list:
                    error.acceptCertificate()
                    check_permission_list = 'Done'
            if permission_reject_list:
                if url.toString() in permission_reject_list:
                    error.rejectCertificate()
                    check_permission_list = 'Done'

            if check_permission_list is None:
                title = self.LangSetting.language.lang_invalid_certificate

                label = f'{error.description()}\n' \
                        f'{self.LangSetting.language.lang_ask_accept_certificate}{url.toString()}?'
                self.permission_dialog = PermissionDialog(title, label)

                self.permission_dialog.accept_once_button.clicked.connect(lambda: (
                    error.acceptCertificate(),
                    self.permission_dialog.close()
                ))
                self.permission_dialog.reject_once_button.clicked.connect(lambda: (
                    error.rejectCertificate(),
                    self.permission_dialog.close()
                ))
                self.permission_dialog.always_accept_button.clicked.connect(lambda: (
                    CertificatesPermissions().accept_permission("Certificates", url.toString()),
                    error.acceptCertificate(),
                    self.permission_dialog.close()
                ))
                self.permission_dialog.always_reject_button.clicked.connect(lambda: (
                    CertificatesPermissions().reject_permission("Certificates", url.toString()),
                    error.rejectCertificate(),
                    self.permission_dialog.close()
                ))

                self.permission_dialog.show()


class PermissionsHandler:
    def __init__(self):
        super(PermissionsHandler, self).__init__()
        self.LangSetting = LangSetting()
        self.permission_dialog = None

    def permission_handling(self, url, permission, web_view):
        permission_type = f'{permission}'.split('.')
        permission_type = permission_type[4]
        permission_status, permission_accept_list, permission_reject_list = \
            CertificatesPermissions().read_permission(permission_type)
        if permission_status == "No":
            return
        else:
            check_permission_list = None
            if permission_accept_list:
                if url.toString() in permission_accept_list:
                    web_view.page().setFeaturePermission(
                        url, permission, QWebEnginePage.PermissionGrantedByUser
                    )
                    check_permission_list = 'Done'
            if permission_reject_list:
                if url.toString() in permission_reject_list:
                    web_view.page().setFeaturePermission(
                        url, permission, QWebEnginePage.PermissionDeniedByUser
                    )
                    check_permission_list = 'Done'

            if check_permission_list is None:
                title = self.LangSetting.language.lang_permission_requested
                label = f'{url.toString()}{self.LangSetting.language.lang_wants_to_get}{permission}.\n' \
                        f'{self.LangSetting.language.lang_ask_grant_permission}?'
                self.permission_dialog = PermissionDialog(title, label)

                self.permission_dialog.accept_once_button.clicked.connect(lambda: (
                    web_view.page().setFeaturePermission(
                        url, permission, QWebEnginePage.PermissionGrantedByUser),
                    self.permission_dialog.close()
                ))
                self.permission_dialog.reject_once_button.clicked.connect(lambda: (
                    web_view.page().setFeaturePermission(
                        url, permission, QWebEnginePage.PermissionDeniedByUser),
                    self.permission_dialog.close()
                ))
                self.permission_dialog.always_accept_button.clicked.connect(lambda: (
                    CertificatesPermissions().accept_permission(permission_type, url.toString()),
                    web_view.page().setFeaturePermission(
                        url, permission, QWebEnginePage.PermissionGrantedByUser),
                    self.permission_dialog.close()
                ))
                self.permission_dialog.always_reject_button.clicked.connect(lambda: (
                    CertificatesPermissions().reject_permission(permission_type, url.toString()),
                    web_view.page().setFeaturePermission(
                        url, permission, QWebEnginePage.PermissionDeniedByUser),
                    self.permission_dialog.close()
                ))

                self.permission_dialog.show()



