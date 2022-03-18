import yaml


class Configure():
    def __init__(self):
        with open("config.yaml", 'r', encoding='utf-8') as f:
            self._conf = yaml.load(f.read(), Loader=yaml.FullLoader)

    def get_db_config(self):
        host = self._conf['db_config']['host']
        port = self._conf['db_config']['port']
        username = self._conf['db_config']['username']
        password = self._conf['db_config']['password']
        charset = self._conf['db_config']['charset']
        db_names = self._conf['db_config']['db_names']
        return host, port, username, password, charset, db_names

    def get_excel_title(self):
        title = self._conf['excel_conf']['column_name']
        save_dir = self._conf['excel_conf']['save_dir']
        return title, save_dir