from kivy.uix.screenmanager import Screen
from kivy.app import App
import sqlite3

class ShopScreen(Screen):
    def buy_item(self, item_id, cost):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return
        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('SELECT points FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if row and row[0] >= cost:
            cursor.execute('UPDATE users SET points = points - ? WHERE id = ?', (cost, user_id))
            conn.commit()
        conn.close()
        try:
            profile = self.manager.get_screen('profile')
            if hasattr(profile, 'load_user_data'):
                profile.load_user_data()
        except Exception:
            pass
