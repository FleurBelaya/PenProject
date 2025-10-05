from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3


class ProfileScreen(Screen):
    def on_pre_enter(self):
        self.ensure_columns_exist()
        self.load_user_data()
        self.apply_improvements()

    def ensure_columns_exist(self):
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        for col_def in [
            ("main_color", "TEXT"),
            ("emoji_main", "TEXT"),
            ("profile_color", "TEXT"),
            ("emoji_profile", "TEXT"),
            ("active_challenge", "INTEGER"),
            ("last_goal_date", "TEXT")
        ]:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_def[0]} {col_def[1]}")
            except sqlite3.OperationalError:
                pass
        conn.commit()
        conn.close()

    def load_user_data(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, favorite_genre, goal, points FROM users WHERE id=?', (user_id,))
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
        cursor.execute('UPDATE users SET name=?, favorite_genre=?, goal=? WHERE id=?', (name, genre, goal, user_id))
        conn.commit()
        conn.close()
        self.load_user_data()

    def apply_improvements(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT profile_color, emoji_profile FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            color, emoji = row
            if color:
                rgba = tuple(map(float, color.split(',')))
                self.ids.back_button.background_color = rgba
                self.ids.shop_button.background_color = rgba
                self.ids.save_button.background_color = rgba
            if emoji:
                self.ids.back_button.text = emoji + " " + self.ids.back_button.text
                self.ids.shop_button.text = emoji + " " + self.ids.shop_button.text
                self.ids.save_button.text = emoji + " " + self.ids.save_button.text
