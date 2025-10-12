from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3

class ProfileScreen(Screen):
    def on_pre_enter(self):
        self.ensure_columns_exist()
        self.load_user_data()
        self.apply_improvements()
        self.load_upgrades()

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
            self.ids.name_value.text = name if name else ''
            self.ids.favorite_genre_spinner.text = genre if genre else 'Выберите жанр'
            self.ids.goal_value.text = str(goal) if goal else ''
            self.ids.points_label.text = f"Баллы: {points}"

    def save_user_data(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        name = self.ids.name_value.text.strip()
        genre = self.ids.favorite_genre_spinner.text.strip()
        goal = self.ids.goal_value.text.strip()
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET name=?, favorite_genre=?, goal=? WHERE id=?', (name, genre, goal, user_id))
        conn.commit()
        conn.close()
        self.load_user_data()

    def prompt_edit(self, field):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button
        from kivy.uix.label import Label

        content = BoxLayout(orientation='vertical', spacing=6, padding=10)
        lbl = Label(text='Введите значение:')
        ti = TextInput(text=self.ids.name_value.text if field == 'name' else self.ids.goal_value.text, multiline=False)
        ok_btn = Button(text='OK', size_hint_y=None, height=40)
        content.add_widget(lbl)
        content.add_widget(ti)
        content.add_widget(ok_btn)
        popup = Popup(title='Изменение', content=content, size_hint=(0.8, 0.4))

        def on_save(*_):
            if field == 'name':
                self.ids.name_value.text = ti.text.strip()
            elif field == 'goal':
                self.ids.goal_value.text = ti.text.strip()
            self.save_user_data()
            popup.dismiss()

        ok_btn.bind(on_press=on_save)
        
        popup.open()

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

    def load_upgrades(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('SELECT upgrade_id FROM user_upgrades WHERE user_id = ?', (user_id,))
        upgrades = {row[0] for row in cursor.fetchall()}
        conn.close()

        if 1 in upgrades:
            self.ids.back_button.background_color = (0.8, 0.9, 1, 1)
        if 2 in upgrades:
            self.ids.save_button.background_color = (0.9, 0.8, 1, 1)
        if 3 in upgrades:
            self.ids.shop_button.background_color = (0.8, 1, 0.9, 1)
        # map former emoji upgrades to colors too
        if 4 in upgrades:
            self.ids.back_button.background_color = (1, 0.95, 0.7, 1)
        if 5 in upgrades:
            self.ids.save_button.background_color = (0.95, 0.85, 1, 1)

    def logout(self):
        app = App.get_running_app()
        app.current_user_id = None
        try:
            auth_screen = self.manager.get_screen('auth')
            if hasattr(auth_screen, 'clear_fields'):
                auth_screen.clear_fields()
        except Exception:
            pass
        self.manager.current = 'auth'