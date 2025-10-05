from kivy.app import App
from kivy.uix.screenmanager import Screen
import sqlite3

class ShopScreen(Screen):
    def buy_item(self, item_id, cost):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_upgrades (
                user_id INTEGER NOT NULL,
                upgrade_id INTEGER NOT NULL,
                PRIMARY KEY(user_id, upgrade_id)
            )
        ''')

        profile = self.manager.get_screen('profile')
        profile.load_user_data()

        cursor.execute(
            "SELECT 1 FROM user_upgrades WHERE user_id = ? AND upgrade_id = ?",
            (user_id, item_id)
        )
        if cursor.fetchone():
            conn.close()
            print("Улучшение уже куплено!")
            return

        cursor.execute('SELECT points FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if not row or row[0] < cost:
            conn.close()
            print("Недостаточно очков")
            return

        cursor.execute('UPDATE users SET points = points - ? WHERE id = ?', (cost, user_id))
        cursor.execute(
            "INSERT INTO user_upgrades (user_id, upgrade_id) VALUES (?, ?)",
            (user_id, item_id)
        )

        conn.commit()
        conn.close()

        try:
            profile = self.manager.get_screen('profile')
            if hasattr(profile, 'load_user_data'):
                profile.load_user_data()
            if hasattr(profile, 'load_upgrades'):
                profile.load_upgrades()
        except Exception:
            pass

    def load_user_data(self):
        app = App.get_running_app()
        user_id = getattr(app, 'current_user_id', None)
        if not user_id:
            return

        conn = sqlite3.connect('articles.db')
        cursor = conn.cursor()
        cursor.execute('SELECT upgrade_id FROM user_upgrades WHERE user_id = ?', (user_id,))
        upgrades = {row[0] for row in cursor.fetchall()}

        if hasattr(self.ids, 'main_button') and hasattr(self.ids, 'profile_button'):
            main_btn = self.ids.main_button
            profile_btn = self.ids.profile_button

            if 1 in upgrades:
                main_btn.background_color = (0, 1, 0, 1)
            if 2 in upgrades:
                profile_btn.background_color = (0, 0, 1, 1)
            if 3 in upgrades:
                main_btn.text = "(´ о *) " + main_btn.text
            if 4 in upgrades:
                profile_btn.text = "(* ^ о ^)" + profile_btn.text

        conn.close()
