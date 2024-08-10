import os
import time
import random
import string
import sqlite3
import locale


class EnvironConfig:
    def __init__(self):
        super(EnvironConfig, self).__init__()

        self.profile_path = self.read_profile_path()

    @staticmethod
    def read_default_downloads_path():
        if os.name == 'nt':
            default_downloads_path = os.path.join(os.environ['homedrive'], os.environ['homepath'], 'Downloads')
        else:
            default_downloads_path = os.path.join(os.environ['HOME'], 'Downloads')

        default_downloads_path = os.path.normpath(default_downloads_path)
        return default_downloads_path

    @staticmethod
    def read_profile_path():
        if os.name == 'nt':
            profile_path = os.path.join(os.environ['homedrive'], os.environ['homepath'], 'AppData\\Local\\kBrowser')
        else:
            profile_path = os.path.join(os.environ['HOME'], '.config/kBrowser')

        profile_path = os.path.normpath(profile_path)
        if os.path.exists(profile_path) is False:
            os.mkdir(profile_path)

        return profile_path

    def read_configuration_file(self):
        configuration_file = os.path.join(self.profile_path, 'kbconfiguration')
        configuration_file = os.path.normpath(configuration_file)
        if os.path.exists(configuration_file) is False:
            with open(configuration_file, 'w') as temp:
                temp.write('Configuration for kBrowser\n')

        with open(configuration_file, 'r') as temp:
            configuration = temp.readlines()

        return configuration_file, configuration

    def read_configuration_file_setting(self, item):
        value = str()
        _, configuration = self.read_configuration_file()
        for line in configuration:
            if item in line:
                line = line.strip('\n')
                line = line.split('=')
                value = line[1]
        return value

    def update_configuration_file_setting(self, item, value):
        configuration_file, configuration = self.read_configuration_file()

        setting = None
        for line in configuration:
            if item in line:
                setting = line

        if setting:
            n = configuration.index(setting)
            configuration[n] = f'{item}={value}\n'
        else:
            configuration.append(f'{item}={value}\n')

        with open(configuration_file, 'w') as temp:
            for line in configuration:
                temp.write(line)

    @staticmethod
    def create_random_name(prefix_name):
        random_name = string.ascii_letters + string.digits
        random_name = random.sample(random_name, 6)
        random_name = ''.join(random_name)
        random_name = f'{prefix_name}{random_name}'
        return random_name

    def read_custom_profile_name(self):
        custom_profile_name = self.read_configuration_file_setting('Profile')

        not_in_filename = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', ' ']
        for character in not_in_filename:
            if character in custom_profile_name:
                custom_profile_name = ''

        if custom_profile_name == '':
            custom_profile_name = self.create_random_name('kbprofile')
            self.update_configuration_file_setting('Profile', custom_profile_name)

        return custom_profile_name

    def read_custom_profile_path(self):
        # Custom profile folder is in profile folder. It contains settings, history, cache and cookies.
        custom_profile_name = self.read_custom_profile_name()

        custom_profile_path = os.path.join(self.profile_path, custom_profile_name)
        custom_profile_path = os.path.normpath(custom_profile_path)

        if os.path.exists(custom_profile_path) is False:
            os.mkdir(custom_profile_path)

        return custom_profile_path

    def read_cache_storage_path(self):
        custom_profile_path = self.read_custom_profile_path()

        cache_path = os.path.join(custom_profile_path, 'cache')
        cache_path = os.path.normpath(cache_path)

        storage_path = os.path.join(custom_profile_path, 'storage')
        storage_path = os.path.normpath(storage_path)

        return cache_path, storage_path

    @staticmethod
    def locale_code_to_http_language_code(locale_code):
        if '_' in locale_code:
            temp = locale_code.split('_')
            http_language_code = f'{temp[0]}-{temp[1]}'
        else:
            http_language_code = locale_code
        return http_language_code

    @staticmethod
    def http_language_code_to_locale_code(http_language_code):
        if '-' in http_language_code:
            temp = http_language_code.split('-')
            locale_code = f'{temp[0]}_{temp[1]}'
        else:
            locale_code = http_language_code
        return locale_code

    @staticmethod
    def read_system_locale():
        temp = list(locale.getdefaultlocale())
        locale_code = temp[0]
        return locale_code

    @staticmethod
    def read_translations_list():
        translations_list = ['en_US']
        return translations_list

    def read_default_language_settings(self):
        translations_list = self.read_translations_list()
        default_locale = self.read_system_locale()
        default_http_language = self.locale_code_to_http_language_code(default_locale)
        if default_locale not in translations_list:
            default_locale = 'en_US'

        return default_locale, default_http_language


class Database:
    def __init__(self):
        super(Database, self).__init__()

        self.environ_config = EnvironConfig()
        self.custom_profile_path = self.environ_config.read_custom_profile_path()
        self.default_downloads_path = self.environ_config.read_default_downloads_path()
        self.default_locale, self.default_http_language = self.environ_config.read_default_language_settings()

        self.settings_db = None
        self.settings_cursor = None
        self.history_db = None
        self.history_cursor = None

        self.initialize_settings_db()
        self.initialize_history_db()

    def open_settings_db(self):
        settings_db_path = os.path.join(self.custom_profile_path, 'kbsettings.db')
        settings_db_path = os.path.normpath(settings_db_path)
        self.settings_db = sqlite3.connect(settings_db_path)
        self.settings_cursor = self.settings_db.cursor()

    def close_settings_db(self):
        self.settings_db.commit()
        self.settings_cursor.close()
        self.settings_db.close()

    def open_history_db(self):
        history_db_path = os.path.join(self.custom_profile_path, 'kbhistory.db')
        history_db_path = os.path.normpath(history_db_path)
        self.history_db = sqlite3.connect(history_db_path)
        self.history_cursor = self.history_db.cursor()

    def close_history_db(self):
        self.history_db.commit()
        self.history_cursor.close()
        self.history_db.close()

    def initialize_settings_db(self):
        self.open_settings_db()

        # Basic settings
        self.settings_cursor.execute('''CREATE TABLE IF NOT EXISTS basic
                                       (id INTEGER PRIMARY KEY AUTOINCREMENT, item, value)''')
        check_table = self.check_settings_table('basic')
        if len(check_table) == 0:
            self.settings_cursor.executemany('INSERT INTO basic (item, value) VALUES (?, ?)',
                                             [('download_folder', self.default_downloads_path),
                                              ('private_browsing', '0'),
                                              ('https_mode', '1'),
                                              ('ui_translation', self.default_locale),
                                              ('preferred_language', self.default_http_language)])

        # Permissions and certificates
        self.settings_cursor.execute('''CREATE TABLE IF NOT EXISTS permissions
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT, permission, status, accept, reject)''')
        check_table = self.check_settings_table('permissions')
        if len(check_table) == 0:
            self.settings_cursor.executemany('''INSERT INTO permissions (permission, status, accept, reject)
                                                VALUES (?, ?, ?, ?)''',
                                             [('Certificates', '1', '', ''),
                                              ('Notifications', '1', '', ''),
                                              ('Geolocation', '1', '', ''),
                                              ('MediaAudioCapture', '1', '', ''),
                                              ('MediaVideoCapture', '1', '', ''),
                                              ('MediaAudioVideoCapture', '1', '', ''),
                                              ('MouseLock', '1', '', ''),
                                              ('DesktopVideoCapture', '1', '', ''),
                                              ('DesktopAudioVideoCapture', '1', '', '')]
                                             )

        # Search engines
        self.settings_cursor.execute('''CREATE TABLE IF NOT EXISTS search_engines
                                       (id INTEGER PRIMARY KEY AUTOINCREMENT, provider, url, enable)''')
        check_table = self.check_settings_table('search_engines')
        if len(check_table) == 0:
            self.settings_cursor.executemany('INSERT INTO search_engines (provider, url, enable) VALUES (?, ?, ?)',
                                             [('Bing', r'https://www.bing.com/search?q=', '1'),
                                              ('Google', r'https://www.google.com/search?q=', '0'),
                                              ('Baidu', r'https://www.baidu.com/s?wd=', '0')])

        self.close_settings_db()

    def initialize_history_db(self):
        self.open_history_db()
        self.history_cursor.execute('''CREATE TABLE IF NOT EXISTS visits
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT, url, page_title, time)''')
        self.history_cursor.execute('''CREATE TABLE IF NOT EXISTS downloads
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        url, file_name, status, reference_url, time)''')
        self.close_history_db()

    def check_settings_table(self, table):
        db_command = f'SELECT * FROM {table}'
        self.settings_cursor.execute(db_command)
        settings_table = self.settings_cursor.fetchall()
        return settings_table

    def read_settings_table(self, table):
        self.open_settings_db()
        db_command = f'SELECT * FROM {table}'
        self.settings_cursor.execute(db_command)
        settings_table = self.settings_cursor.fetchall()
        self.close_settings_db()
        return settings_table

    def read_settings_data(self, table, query_column, query_column_value):
        self.open_settings_db()
        db_command = f'SELECT * FROM {table} where {query_column} = ?'
        self.settings_cursor.execute(db_command, (query_column_value,))
        settings_data = self.settings_cursor.fetchall()
        self.close_settings_db()
        return settings_data

    def update_settings_data(self, table, query_column, query_column_value, target_column, target_column_value):
        self.open_settings_db()
        db_command = f'UPDATE {table} SET {target_column} = ? WHERE {query_column} = ?'
        target_column_value = str(target_column_value)
        self.settings_cursor.execute(db_command, (target_column_value, query_column_value))
        self.close_settings_db()

    def delete_settings_data(self, table, query_column, query_column_value):
        self.open_settings_db()
        db_command = f'DELETE FROM {table} WHERE {query_column} = ?'
        self.settings_cursor.execute(db_command, (query_column_value,))
        self.close_settings_db()

    def read_history_table(self, table):
        self.open_history_db()
        db_command = f'SELECT * FROM {table} ORDER BY id DESC'
        self.history_cursor.execute(db_command)
        history_table = self.history_cursor.fetchall()
        self.close_history_db()
        return history_table

    def read_history_urls(self):
        self.open_history_db()
        db_command = f'SELECT url, page_title, MAX(id) FROM visits GROUP BY url'
        self.history_cursor.execute(db_command)
        history_urls = self.history_cursor.fetchall()
        self.close_history_db()
        return history_urls

    def read_history_data(self, table, query_column, query_column_value):
        self.open_history_db()
        db_command = f'SELECT * FROM {table} where {query_column} = ?'
        self.history_cursor.execute(db_command, (query_column_value,))
        history_data = self.history_cursor.fetchall()
        self.close_history_db()
        return history_data

    def insert_visits_history(self, url, page_title):
        self.open_history_db()
        db_command = f'INSERT INTO visits (url, page_title, time) VALUES (?, ?, ?)'
        self.history_cursor.execute(db_command, (url, page_title, time.asctime()))
        self.close_history_db()

    def insert_downloads_history(self, url, file_name, status, reference_url):
        self.open_history_db()
        db_command = f'INSERT INTO downloads (url, file_name, status, reference_url, time) VALUES (?, ?, ?, ?, ?)'
        self.history_cursor.execute(db_command, (url, file_name, status, reference_url, time.asctime()))
        self.close_history_db()

    def reset_history_table(self, table):
        self.open_history_db()
        self.history_cursor.execute(f'DROP TABLE {table}')
        if table == 'visits':
            self.history_cursor.execute(
                'CREATE TABLE IF NOT EXISTS visits (id INTEGER PRIMARY KEY AUTOINCREMENT, url, page_title, time)'
            )
        if table == 'downloads':
            self.history_cursor.execute(
                '''CREATE TABLE IF NOT EXISTS downloads (id INTEGER PRIMARY KEY AUTOINCREMENT, url, file_name,
                status, reference_url, time)'''
            )

        self.close_history_db()

    def delete_history_data(self, table, query_column, query_column_value):
        self.open_history_db()
        db_command = f'DELETE FROM {table} WHERE {query_column} = ?'
        self.history_cursor.execute(db_command, (query_column_value,))
        self.close_history_db()
