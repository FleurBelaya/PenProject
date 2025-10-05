from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3


class ChallengesScreen(Screen):
    def start_challenge(self, challenge_id):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN active_challenge INTEGER")
        except sqlite3.OperationalError:
            pass
        cursor.execute("SELECT active_challenge FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row and row[0]:
            conn.close()
            return
        cursor.execute("UPDATE users SET active_challenge = ? WHERE id = ?", (challenge_id, user_id))
        conn.commit()
        conn.close()
        try:
            main = self.manager.get_screen('main')
            main.update_active_challenge()
            self.manager.current = 'main'
        except Exception:
            pass

    def cancel_challenge(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET active_challenge = NULL WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
