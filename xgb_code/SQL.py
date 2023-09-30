class SQL_configs:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'chipsSQL@1'
        self.database = 'XGB_project'
        self.table = 'credit_card_fraud'
        self.auth_plugin = 'mysql_native_password'

class SQL_queries:
    def __init__(self) -> None:
        self.sql_configs = SQL_configs()

        self.drop_query = f"""
            DROP TABLE {self.sql_configs.table};
        """

        self.insert_query = f"""
            INSERT INTO {self.sql_configs.table} 
            (ID, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.initial_query = f"""
            CREATE TABLE {self.sql_configs.table}(
            ID MEDIUMINT,
            V1 FLOAT(24, 20),
            V2 FLOAT(24, 20),
            V3 FLOAT(24, 20),
            V4 FLOAT(24, 20),
            V5 FLOAT(24, 20),
            V6 FLOAT(24, 20),
            V7 FLOAT(24, 20),
            V8 FLOAT(24, 20),
            V9 FLOAT(24, 20),
            V10 FLOAT(24, 20),
            V11 FLOAT(24, 20),
            V12 FLOAT(24, 20),
            V13 FLOAT(24, 20),
            V14 FLOAT(24, 20),
            V15 FLOAT(24, 20),
            V16 FLOAT(24, 20),
            V17 FLOAT(24, 20),
            V18 FLOAT(24, 20),
            V19 FLOAT(24, 20),
            V20 FLOAT(24, 20),
            V21 FLOAT(24, 20),
            V22 FLOAT(24, 20),
            V23 FLOAT(24, 20),
            V24 FLOAT(24, 20),
            V25 FLOAT(24, 20),
            V26 FLOAT(24, 20),
            V27 FLOAT(24, 20),
            V28 FLOAT(24, 20),
            Amount FLOAT(10, 2),
            Class TINYINT,
            PRIMARY KEY (ID)
            );
        """

        self.select_query = f"""
            SELECT V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class
            FROM {self.sql_configs.table}
        """