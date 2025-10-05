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

        cursor.execute('SELECT points FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()

        if row and row[0] >= cost:
            cursor.execute('UPDATE users SET points = points - ? WHERE id = ?', (cost, user_id))

            try:
                cursor.execute("ALTER TABLE users ADD COLUMN main_color TEXT")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN profile_color TEXT")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN emoji_main TEXT")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN emoji_profile TEXT")
            except sqlite3.OperationalError:
                pass

            if item_id == 1:
                cursor.execute("UPDATE users SET main_color = ? WHERE id = ?", ("0,1,0,1", user_id))
            elif item_id == 2:
                cursor.execute("UPDATE users SET profile_color = ? WHERE id = ?", ("0,0,1,1", user_id))
            elif item_id == 3:
                cursor.execute("UPDATE users SET emoji_main = ? WHERE id = ?", ("(´ ∀ ` *) ", user_id))
            elif item_id == 4:
                cursor.execute("UPDATE users SET emoji_profile = ? WHERE id = ?", ("(* ^ ω ^)", user_id))

            conn.commit()

        conn.close()

        try:
            profile = self.manager.get_screen('profile')
            if hasattr(profile, 'load_user_data'):
                profile.load_user_data()
        except Exception:
            pass


