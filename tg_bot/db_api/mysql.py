
import pymysql
from pymysql.cursors import DictCursor
from tg_bot.misc.formatters import format_todo
from tg_bot.settings import load_db_cnf


class Database:
    def __init__(self):
        self.config = load_db_cnf(".env")

    @property
    def connection(self):
        return pymysql.connect(host=self.config.host,
                               user=self.config.user,
                               password=self.config.password,
                               database=self.config.database,
                               charset='utf8mb4',
                               cursorclass=DictCursor)

    def execute(self, command, *args, commit: bool = False, fetch: bool = False, fetchall: bool = False):
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(command, args)

        data = None

        if commit:
            connection.commit()
        elif fetch:
            data = cursor.fetchone()
        elif fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def creaete_tables(self):
        querys = (
            """
                CREATE TABLE IF NOT EXISTS `User` (
                    id BIGINT UNSIGNED NOT NULL,
                    full_name VARCHAR(255) NOT NULL,
                    username VARCHAR(255),
                    
                    PRIMARY KEY (id)
                );
            """,
            """
                CREATE TABLE IF NOT EXISTS `Todo` (
                    id SERIAL,
                    todo_text TEXT NOT NULL,
                    todo_once BOOL NOT NULL,
                    status BOOL NOT NULL,
                    user_id BIGINT UNSIGNED NOT NULL,
                    
                    PRIMARY KEY (id),
                    FOREIGN KEY (user_id) REFERENCES `User` (id)    
                );
            """
        )

        for sql in querys:
            self.execute(sql, commit=True)

    def add_user(self, user_id: int, fullname: str, username: str | None = None):
        sql = """
        INSERT INTO `User` (id, full_name, username) VALUES (%s, %s, %s);
        """
        self.execute(sql, user_id, fullname, username, commit=True)

    def add_task(self, text: str, user_id: int, once: bool = True, status: bool = False):
        sql = """
        INSERT INTO `Todo` (todo_text, todo_once, status, user_id)
        VALUES (%s, %s, %s, %s);
        """
        self.execute(sql, text, once, status,  user_id, commit=True)

    def get_task(self, fetch: bool = False, fetchall: bool = False, **kwargs):
        sql = """
            SELECT * FROM `Todo` WHERE
        """
        sql, params = format_todo(sql, **kwargs)

        return self.execute(sql, *params, fetch=fetch, fetchall=fetchall)

    def get_user(self, user_id: int = None, fetch: bool = False, fetchall: bool = False):
        params = tuple()
        where = " WHERE user_id = %s"
        sql = """
            SELECT * FROM `User`
        """
        if user_id:
            sql += where
            params = (user_id,)

        return self.execute(sql, *params, fetch=fetch, fetchall=fetchall)
