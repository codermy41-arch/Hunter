from kivy.app import App
from kivy.uix.webview import WebView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.utils import platform
import os
import google.generativeai as genai

class HungryHunterApp(App):
    def build(self):
        layout = FloatLayout()
        
        # Path logic for Android vs Desktop
        if platform == 'android':
            index_path = os.path.join(os.getcwd(), "index.html")
        else:
            index_path = os.path.abspath("index.html")
            
        # 1. High-Performance WebView
        self.web = WebView(url="file://" + index_path)
        layout.add_widget(self.web)
        
        # 2. Premium Floating AI Button
        self.btn = Button(
            text="AI PREDICT",
            size_hint=(0.3, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.03},
            background_normal='',
            background_color=(0, 0.9, 1, 0.8),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        self.btn.bind(on_press=self.trigger_ai)
        layout.add_widget(self.btn)
        
        return layout

    def trigger_ai(self, instance):
        # This will be replaced by real screen capture logic
        prediction = "CHAI (5x)"
        confidence = 92
        strategy = "High stability detected. Safe bet on Chai/Samosa."
        
        # Bridge to Javascript
        js = f"updatePrediction('{prediction}', {confidence}, '{strategy}')"
        self.web.eval_js(js)

if __name__ == '__main__':
    HungryHunterApp().run()
