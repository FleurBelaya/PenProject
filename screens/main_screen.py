from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty

class MainScreen(Screen):
    goal_done = BooleanProperty(False)

    def toggle_goal(self):
        self.goal_done = not self.goal_done
        goal_btn = self.ids.goal_button
        if self.goal_done:
            goal_btn.text = "Цель выполнена"
            goal_btn.background_color = (1, 0.6, 0.8, 1)
        else:
            goal_btn.text = "Цель не выполнена"
            goal_btn.background_color = (1, 1, 1, 1)
