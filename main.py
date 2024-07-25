import logging
import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import webbrowser
from file_run import (basicSimulator, cameraSimulator, planetSimulator, playgroundSimulator, pendulumSimulator, atwoodMacSimulator, collisionSimulator, secondcollisionSimulator, rotationalMotionSimulator)

logging.basicConfig(level=logging.DEBUG)

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.2, 0.2, 0.2, 1)
        self.color = (1, 1, 1, 1)
        self.size_hint = (None, None)
        # self.size = (300, 50)  # Default size

def run_simulation(simulation_func):
    threading.Thread(target=simulation_func).start()

class BoxLayoutExample(FloatLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.initialize_buttons()

    def initialize_buttons(self):
        self.clear_widgets()

        b2 = RoundedButton(text="Simulator with Graphs", size=(300, 50), pos_hint={'center_x': 0.5, 'center_y': 0.65})
        b3 = RoundedButton(text="Simulator without Graphs", size=(300, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        b4 = RoundedButton(text="About Physiolab", size=(300, 50), pos_hint={'center_x': 0.5, 'center_y' : .35})
        b2.bind(on_press=self.on_button2_press)
        b3.bind(on_press=self.on_button3_press)
        b4.bind(on_press=self.on_button4_press)

        self.add_widget(b2)
        self.add_widget(b3)
        self.add_widget(b4)

    def on_button2_press(self, instance):
        self.create_initial_buttons()

    def on_button3_press(self, instance):
        self.create_noGraph_buttons()

    def on_button4_press(self, instance):
        url = "https://linktr.ee/physio_lab" 
        webbrowser.open(url)

    def create_initial_buttons(self):
        self.clear_widgets()
        button_texts = [
            "Single Object Simulation",
            "Atwoods Simulation",
            "Pendulum Simulation",
            "Planetary Motion Simulation",
            "Collision Simulation",
            "Rotational Motion Simulation",
            "Go Back"
        ]
        button_callbacks = [
            self.onButton1_press,
            self.onButton4_press,
            self.onButton5_press,
            self.onButton6_press,
            self.onButton9_press,
            self.rotMotion_press,
            self.on_home_button_press
        ]
        y_pos = 0.8
        for text, callback in zip(button_texts, button_callbacks):
            if text == "Go Back":
                new_button = RoundedButton(text=text, size=(80, 30), pos_hint={'center_x': 0.5, 'center_y': y_pos})
            else:
                new_button = RoundedButton(text=text, size=(400, 50), pos_hint={'center_x': 0.5, 'center_y': y_pos})
            new_button.bind(on_press=callback)
            self.add_widget(new_button)
            y_pos -= 0.1
    
    def create_noGraph_buttons(self):
        self.clear_widgets()
        button_texts1 = [
            "Physics Playground",
            "Camera Simulation",
            "Go Back"
        ]
        button_callbacks1 = [
            self.onButton7_press,
            self.onButton2_press,
            self.on_home_button_press
        ]
        y_pos = 0.8
        for text, callback in zip(button_texts1, button_callbacks1):
            if text == "Go Back":
                new_button = RoundedButton(text=text, size=(80, 30), pos_hint={'center_x': 0.5, 'center_y': y_pos})
            else:
                new_button = RoundedButton(text=text, size=(400, 50), pos_hint={'center_x': 0.5, 'center_y': y_pos})
            new_button.bind(on_press=callback)
            self.add_widget(new_button)
            y_pos -= 0.15
    
    def collisionButtons(self):    
        self.clear_widgets()
        button_texts1 = [
            "Elastic Collision",
            "Inelastic Collision",
            "Go Back"
        ]
        button_callbacks1 = [
            self.onButton10_press,
            self.onButton11_press,
            self.on_back_button_press
        ]
        y_pos = 0.8
        for text, callback in zip(button_texts1, button_callbacks1):
            if text == "Go Back":
                new_button = RoundedButton(text=text, size=(80, 30), pos_hint={'center_x': 0.5, 'center_y': y_pos})
            else:
                new_button = RoundedButton(text=text, size=(400, 50), pos_hint={'center_x': 0.5, 'center_y': y_pos})
            new_button.bind(on_press=callback)
            self.add_widget(new_button)
            y_pos -= 0.15

    def onButton1_press(self, instance):
        run_simulation(basicSimulator)

    def onButton2_press(self, instance):
        run_simulation(cameraSimulator)

    def onButton4_press(self, instance):
        run_simulation(atwoodMacSimulator)

    def onButton5_press(self, instance):
        run_simulation(pendulumSimulator)

    def onButton6_press(self, instance):
        run_simulation(planetSimulator)
    
    def onButton7_press(self, instance):
        run_simulation(playgroundSimulator)

    def on_home_button_press(self, instance):
        self.initialize_buttons()
    
    def on_back_button_press(self, instance):
        self.create_initial_buttons()

    def onButton9_press(self, instance):
        self.collisionButtons()
    
    def onButton10_press(self, instance):
        run_simulation(collisionSimulator)
    
    def onButton11_press(self, instance):
        run_simulation(secondcollisionSimulator)

    def rotMotion_press(self, instance):
        run_simulation(rotationalMotionSimulator)

class FirstScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayoutExample(screen_manager)
        float_layout = FloatLayout()
        with float_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg_image_size, pos=self.update_bg_image_pos)
        float_layout.add_widget(self.layout)
        self.add_widget(float_layout)

    def update_bg_image_size(self, *args):
        self.rect.size = self.size

    def update_bg_image_pos(self, *args):
        self.rect.pos = self.pos

class SecondScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg_image_size, pos=self.update_bg_image_pos)

        label = Label(text="This is the second screen", color=(1, 1, 1, 1), size_hint=(0.6, 0.2), pos_hint={'center_x': 0.5, 'top': 1})
        button = RoundedButton(text="Go Back", size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button.bind(on_press=self.on_button_press)

        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)

    def update_bg_image_size(self, *args):
        self.rect.size = self.size

    def update_bg_image_pos(self, *args):
        self.rect.pos = self.pos

    def on_button_press(self, instance):
        self.screen_manager.current = 'first'

class PhysicsApp(App):
    def build(self):
        screen_manager = ScreenManager()
        first_screen = FirstScreen(screen_manager, name='first')
        screen_manager.add_widget(first_screen)
        second_screen = SecondScreen(screen_manager, name='second')
        screen_manager.add_widget(second_screen)

        Window.fullscreen = 'auto'
        
        return screen_manager

if __name__ == "__main__":
    PhysicsApp().run()
