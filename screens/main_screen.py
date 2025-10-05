import datetime
import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty


class MainScreen(Screen):
    goal_done = BooleanProperty(False)
    CHALLENGES = {
        1: "Написать 10000 слов",
        2: "История из 100 предложений",
        3: "История без диалогов",
        4: "Написать сюжет в 100 слов",
        5: "Диалог без глаголов действия",
    }

    def on_pre_enter(self):
        self.apply_improvements()
        self.update_active_challenge()

    def apply_improvements(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT main_color, emoji_main FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            color, emoji = row
            if color:
                rgba = tuple(map(float, color.split(',')))
                for btn_id in ['profile_button', 'challenges_button', 'exercises_button', 'articles_button', 'goal_button']:
                    self.ids[btn_id].background_color = rgba
            if emoji:
                for btn_id in ['profile_button', 'challenges_button', 'exercises_button', 'articles_button']:
                    self.ids[btn_id].text = emoji + " " + self.ids[btn_id].text

    def toggle_goal(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        today = datetime.date.today().isoformat()
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN last_goal_date TEXT")
        except sqlite3.OperationalError:
            pass
        cursor.execute("SELECT last_goal_date FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row and row[0] == today:
            conn.close()
            return
        self.goal_done = not self.goal_done
        goal_btn = self.ids.goal_button
        if self.goal_done:
            goal_btn.text = "Цель выполнена"
            goal_btn.background_color = (1, 0.6, 0.8, 1)
            self.add_points(50)
            cursor.execute("UPDATE users SET last_goal_date = ? WHERE id = ?", (today, user_id))
            conn.commit()
        else:
            goal_btn.text = "Цель не выполнена"
            goal_btn.background_color = (1, 1, 1, 1)
        conn.close()

    def update_active_challenge(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT active_challenge FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            cid = row[0]
            challenge_name = self.CHALLENGES.get(cid, f"Челлендж {cid}")
            self.ids.current_challenge_label.text = f"{challenge_name}"
            self.ids.complete_challenge_button.text = "Завершить"
        else:
            self.ids.current_challenge_label.text = "Нет активного"
            self.ids.complete_challenge_button.text = ""

    def complete_challenge(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT active_challenge FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row or not row[0]:
            conn.close()
            return
        cursor.execute("UPDATE users SET active_challenge = NULL WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        self.add_points(100)
        self.ids.current_challenge_label.text = "Нет активного"
        self.ids.complete_challenge_button.text = ""

    def add_points(self, points):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if user_id:
            conn = sqlite3.connect('articles.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET points = points + ? WHERE id = ?', (points, user_id))
            conn.commit()
            conn.close()
            try:
                profile = self.manager.get_screen('profile')
                if hasattr(profile, 'load_user_data'):
                    profile.load_user_data()
            except Exception:
                pass

    def go_to_profile(self):
        self.manager.current = 'profile'
