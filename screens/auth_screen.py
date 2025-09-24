from kivy.uix.screenmanager import Screen
import sqlite3
from kivy.app import App

class AuthScreen(Screen):

    def ensure_users_table(self):
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT,
                name TEXT,
                favorite_genre TEXT,
                goal INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def register_user(self):
        self.ensure_users_table()

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not email or not password:
            self.ids.error_label.text = 'Введите email и пароль'
            conn.close()
            return

        try:
            cursor.execute(
                'INSERT INTO users (email, password, points) VALUES (?, ?, 0)',
                (email, password)
            )
            conn.commit()
            user_id = cursor.lastrowid
            App.get_running_app().current_user_id = user_id
            self.manager.current = 'main'
        except sqlite3.IntegrityError:
            self.ids.error_label.text = 'Пользователь с таким email уже существует'
        finally:
            conn.close()

    def login_user(self):
        self.ensure_users_table()

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text.strip()
        cursor.execute(
            'SELECT id FROM users WHERE email = ? AND password = ?',
            (email, password)
        )
        row = cursor.fetchone()
        if row:
            App.get_running_app().current_user_id = row[0]
            self.manager.current = 'main'
        else:
            self.ids.error_label.text = 'Неверный email или пароль'
        conn.close()
