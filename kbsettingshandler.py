import ast

from kbdatabase import EnvironConfig, Database
from kblang import LangEnUS


class BasicSettings:
    def __init__(self):
        super(BasicSettings, self).__init__()

        self.environ_config = EnvironConfig()
        self.database = Database()
        self.LangSetting = LangSetting()

    def read_cache_storage_path(self):
        cache_path, storage_path = self.environ_config.read_cache_storage_path()
        return cache_path, storage_path

    def read_download_folder(self):
        temp = self.database.read_settings_data('basic', 'item', 'download_folder')
        temp = temp[0]
        download_folder = temp[2]
        return download_folder

    def change_download_folder(self, path):
        self.database.update_settings_data('basic', 'item', 'download_folder', 'value', path)

    def read_private_browsing(self):
        temp = self.database.read_settings_data('basic', 'item', 'private_browsing')
        temp = temp[0]
        value = temp[2]
        if value == "1":
            status = self.LangSetting.language.lang_yes
        else:
            status = self.LangSetting.language.lang_no

        return status

    def read_https_mode(self):
        temp = self.database.read_settings_data('basic', 'item', 'https_mode')
        temp = temp[0]
        value = temp[2]
        if value == "1":
            status = self.LangSetting.language.lang_yes
        else:
            status = self.LangSetting.language.lang_no

        return status

    def enable_basic_setting(self, item_type):
        self.database.update_settings_data('basic', 'item', item_type, 'value', '1')

    def disable_basic_setting(self, item_type):
        self.database.update_settings_data('basic', 'item', item_type, 'value', '0')


class SearchEngines:
    def __init__(self):
        super(SearchEngines, self).__init__()

        self.database = Database()

    def read_search_engines(self):
        temp = self.database.read_settings_table('search_engines')
        temp = list(zip(*temp))
        search_engines_list = temp[1]
        return search_engines_list

    def read_enabled_search_engine(self):
        temp = self.database.read_settings_data('search_engines', 'enable', '1')
        temp = temp[0]
        enabled_search_engine = temp[1]
        enabled_search_engine_url = temp[2]
        return enabled_search_engine, enabled_search_engine_url

    def enable_search_engine(self, provider):
        self.database.update_settings_data('search_engines', 'provider', provider, 'enable', '1')

    def disable_search_engine(self, provider):
        self.database.update_settings_data('search_engines', 'provider', provider, 'enable', '0')


class CertificatesPermissions:
    def __init__(self):
        super(CertificatesPermissions, self).__init__()

        self.database = Database()
        self.LangSetting = LangSetting()

    def read_permission(self, permission_type):
        temp = self.database.read_settings_data('permissions', 'permission', permission_type)
        temp = temp[0]
        permission_status = temp[2]

        if permission_status == '1':
            permission_status = self.LangSetting.language.lang_yes
        else:
            permission_status = self.LangSetting.language.lang_no

        permission_accept_list = temp[3]
        if permission_accept_list == '' or permission_accept_list is None:
            permission_accept_list = list()
        else:
            permission_accept_list = ast.literal_eval(permission_accept_list)

        permission_reject_list = temp[4]
        if permission_reject_list == '' or permission_reject_list is None:
            permission_reject_list = list()
        else:
            permission_reject_list = ast.literal_eval(permission_reject_list)

        return permission_status, permission_accept_list, permission_reject_list

    def enable_permission(self, permission_type):
        self.database.update_settings_data('permissions', 'permission', permission_type, 'status', '1')

    def disable_permission(self, permission_type):
        self.database.update_settings_data('permissions', 'permission', permission_type, 'status', '0')

    def accept_permission(self, permission_type, url):
        _, permission_accept_list, _ = self.read_permission(permission_type)
        if permission_accept_list == '' or permission_accept_list is None:
            permission_accept_list = list()

        check_permission_list = None
        if permission_accept_list:
            if url in permission_accept_list:
                check_permission_list = 'Found'

        if check_permission_list is None:
            permission_accept_list.append(url)
            self.database.update_settings_data(
                'permissions', 'permission', permission_type, 'accept', permission_accept_list
            )

    def reject_permission(self, permission_type, url):
        _, _, permission_reject_list = self.read_permission(permission_type)
        if permission_reject_list == "" or permission_reject_list is None:
            permission_reject_list = list()

        check_permission_list = None
        if permission_reject_list:
            if url in permission_reject_list:
                check_permission_list = 'Found'

        if check_permission_list is None:
            permission_reject_list.append(url)
            self.database.update_settings_data(
                'permissions', 'permission', permission_type, 'reject', permission_reject_list
            )

    def remove_from_accept(self, permission_type, url):
        permission_status, permission_accept_list, permission_reject_list = self.read_permission(permission_type)
        accepted_list = permission_accept_list.remove(url)
        self.database.update_settings_data('permissions', 'permission', permission_type, 'accept', accepted_list)

    def remove_from_reject(self, permission_type, url):
        permission_status, permission_accept_list, permission_reject_list = self.read_permission(permission_type)
        rejected_list = permission_reject_list.remove(url)
        self.database.update_settings_data('permissions', 'permission', permission_type, 'reject', rejected_list)


class LangSetting:
    def __init__(self):
        super(LangSetting, self).__init__()
        self.environ_config = EnvironConfig()
        self.database = Database()

        self.language = self.switch_ui_translation()
        self.languages_list = [('en_US', self.language.lang_en_us), ('zh_CN', self.language.lang_zh_cn)]

    def switch_ui_translation(self):
        temp = self.database.read_settings_data('basic', 'item', 'ui_translation')
        temp = temp[0]
        locale_code = temp[2]
        ui_translation = None
        if locale_code == 'en_US':
            ui_translation = LangEnUS()
        return ui_translation

    def read_translations_list(self):
        translations_list = self.environ_config.read_translations_list()

        for locale_code in translations_list:
            language_name = self.show_language_name(locale_code)
            n = translations_list.index(locale_code)
            translations_list[n] = language_name

        return translations_list

    def language_name_to_language_code(self, language_name):
        temp = list(zip(*self.languages_list))
        locale_code_list = temp[0]
        language_name_list = temp[1]

        n = language_name_list.index(language_name)
        locale_code = locale_code_list[n]
        http_language_code = self.environ_config.locale_code_to_http_language_code(locale_code)
        return locale_code, http_language_code

    def show_language_name(self, language_code):
        temp = list(zip(*self.languages_list))
        locale_code_list = temp[0]
        language_name_list = temp[1]

        if language_code not in locale_code_list:
            language_code = self.environ_config.http_language_code_to_locale_code(language_code)

        n = locale_code_list.index(language_code)
        language_name = language_name_list[n]

        return language_name

    def read_ui_translation_setting(self):
        temp = self.database.read_settings_data('basic', 'item', 'ui_translation')
        temp = temp[0]
        locale_code = temp[2]
        translation_name = self.show_language_name(locale_code)

        available_translations_list = self.read_translations_list()

        return translation_name, available_translations_list

    def read_preferred_language_setting(self):
        temp = self.database.read_settings_data('basic', 'item', 'preferred_language')
        temp = temp[0]
        http_language_code = temp[2]
        language_name = self.show_language_name(http_language_code)

        temp = list(zip(*self.languages_list))
        available_languages_list = temp[1]

        return http_language_code, language_name, available_languages_list

    def change_ui_translation_setting(self, language_name):
        locale_code, _ = self.language_name_to_language_code(language_name)
        self.database.update_settings_data('basic', 'item', 'ui_translation', 'value', locale_code)

    def change_preferred_language_setting(self, language_name):
        _, http_language_code = self.language_name_to_language_code(language_name)
        self.database.update_settings_data('basic', 'item', 'preferred_language', 'value', http_language_code)


class WindowSettings:
    def __init__(self):
        super(WindowSettings, self).__init__()

        self.environ_config = EnvironConfig()

    def save_window_size(self, width, height):
        self.environ_config.update_configuration_file_setting('Width', width)
        self.environ_config.update_configuration_file_setting('Height', height)

    def read_window_size(self, available_width, available_height):
        width = self.environ_config.read_configuration_file_setting('Width')
        height = self.environ_config.read_configuration_file_setting('Height')

        if width == '':
            width = 1116
        if height == '':
            height = 690

        try:
            width = int(width)
        except ValueError:
            width = 1116

        try:
            height = int(height)
        except ValueError:
            height = 690

        if width > available_width:
            width = available_width

        if height > available_height * 0.97:
            height = available_height * 0.97

        window_maximized_status = False
        if width == available_width and height == available_height * 0.97:
            window_maximized_status = True

        return width, height, window_maximized_status
