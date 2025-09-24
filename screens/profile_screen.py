from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3


class ProfileScreen(Screen):
    def on_pre_enter(self):
        self.load_user_data()

    def load_user_data(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT,
                name TEXT,
                favorite_genre TEXT,
                goal INTEGER,
                points INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

        cursor.execute(
            'SELECT name, favorite_genre, goal, points FROM users WHERE id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            name, genre, goal, points = row
            self.ids.name_input.text = name if name else ''
            self.ids.favorite_genre_spinner.text = genre if genre else 'Выберите жанр'
            self.ids.goal_input.text = str(goal) if goal else ''
            self.ids.points_label.text = f"Баллы: {points}"

    def save_user_data(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return

        name = self.ids.name_input.text.strip()
        genre = self.ids.favorite_genre_spinner.text.strip()
        goal = self.ids.goal_input.text.strip()

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET name = ?, favorite_genre = ?, goal = ? WHERE id = ?',
            (name, genre, goal, user_id)
        )
        conn.commit()
        conn.close()

        self.load_user_data()
