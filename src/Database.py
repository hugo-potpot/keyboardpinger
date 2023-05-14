import sqlite3


class Database:
    def __init__(self, database_path: str):
        self.conn = sqlite3.connect(database=database_path, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS USERS "
            "(id BIGINT PRIMARY KEY, "
            "username VARCHAR(32) NOT NULL, "
            "join_date DATE NOT NULL)")
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS FAVORIS(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_sneakers VARCHAR(64) NOT NULL,
                    secondary_name VARCHAR(64) NOT NULL,
                    size_sneakers VARCHAR(32) NOT NULL,
                    sku VARCHAR(32) DEFAULT NULL,
                    status VARCHAR(3) NOT NULL,
                    id_user BIGINT REFERENCES USERS(id) NOT NULL
                )   
            """)
        self.conn.commit()

    def clear(self):
        self.cur.execute("DELETE FROM USERS")
        self.cur.execute("DELETE FROM FAVORIS")
        self.conn.commit()

    def add_user(self, id, username):
        self.cur.execute("INSERT INTO USERS VALUES (?, ?, CURRENT_DATE)", (id, username))
        self.conn.commit()

    def remove_user(self, id):
        self.cur.execute("DELETE FROM USERS WHERE id=?", (id,))
        self.conn.commit()

    def add_favoris(self, name_sneakers, secondary_name, size_sneakers, status, id_user, sku= None):
        self.cur.execute("INSERT INTO FAVORIS (name_sneakers, secondary_name, size_sneakers, sku, status, id_user) VALUES (?, ?, ?, ?, ?, ?)",
                         (name_sneakers, secondary_name, size_sneakers, sku, status, id_user))
        self.conn.commit()

    def remove_favoris(self, id_user, id, status):
        self.cur.execute("DELETE FROM FAVORIS WHERE id_user=? AND id=? AND status=?", (id_user, id, status))
        self.conn.commit()

    def get_user(self, id):
        if self.cur.execute("SELECT * FROM USERS WHERE id=?", (id,)).fetchone() is None:
            return False
        return True

    def get_message_content(self, content, status):
        print(content)
        self.cur.execute(
            "SELECT id_user FROM FAVORIS WHERE (name_sneakers LIKE '%' || ? || '%' "
            "AND secondary_name LIKE '%' || ? || '%' AND status != ?) "
            "OR sku LIKE '%' || ? || '%'", (content, content, status, content))
        return self.cur.fetchall()

    def __del__(self):
        self.conn.close()


