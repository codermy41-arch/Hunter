from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.clock import Clock
import os
import json
import requests # AI ke liye ab hum iska use karenge

HUNGRY_ITEMS = ["Chai", "Samosa", "Softy", "Popcorn", "Chocolate", "Laddu", "Burger", "Pizza"]

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    Color = autoclass('android.graphics.Color')
else:
    class WebView:
        def __init__(self, *args, **kwargs): pass
        def loadUrl(self, url): pass
        def evaluateJavascript(self, js, callback): pass

class HungryHunterApp(App):
    auto_mode = False
    prediction_timer = None

    def build(self):
        self.layout = FloatLayout()
        if platform == 'android':
            request_permissions([Permission.INTERNET, Permission.SYSTEM_ALERT_WINDOW, Permission.FOREGROUND_SERVICE])
            Clock.schedule_once(self.create_webview, 0)

        # START/STOP Button
        self.btn_main = Button(text="START AUTO-SCAN", size_hint=(0.45, 0.08), pos_hint={'center_x': 0.3, 'y': 0.05}, background_color=(0, 0.8, 0.4, 0.9), bold=True)
        self.btn_main.bind(on_press=self.toggle_auto_mode)
        self.layout.add_widget(self.btn_main)

        # PREDICT Button
        self.btn_predict = Button(text="AI PREDICT", size_hint=(0.4, 0.08), pos_hint={'center_x': 0.75, 'y': 0.05}, background_color=(0, 0.6, 1, 0.9), bold=True)
        self.btn_predict.bind(on_press=self.manual_predict)
        self.layout.add_widget(self.btn_predict)
        return self.layout

    def toggle_auto_mode(self, instance):
        self.auto_mode = not self.auto_mode
        self.btn_main.text = "STOP SCANNING" if self.auto_mode else "START AUTO-SCAN"
        self.btn_main.background_color = (1, 0.2, 0.2, 0.9) if self.auto_mode else (0, 0.8, 0.4, 0.9)
        if self.auto_mode: Clock.schedule_interval(self.check_game_round, 5)
        else: Clock.unschedule(self.check_game_round)

    def check_game_round(self, dt):
        self.manual_predict(None)

    def manual_predict(self, instance):
        self.run_js_safe("updatePrediction('ANALYZING...', 0, 'Fetching round data...')")
        if platform == 'android':
            from jnius import PythonJavaClass, java_method
            class KeyCallback(PythonJavaClass):
                __javainterfaces__ = ['android/webkit/ValueCallback']
                @java_method('(Ljava/lang/Object;)V')
                def onReceiveValue(self, value):
                    key = str(value).replace('"', '')
                    if key and key != "null": Clock.schedule_once(lambda dt: self.outer.call_gemini_api(key), 0)
                def __init__(self, outer):
                    super().__init__(); self.outer = outer
            self.webview.evaluateJavascript("(function(){return localStorage.getItem('gh_key');})();", KeyCallback(self))
        else:
            self.call_gemini_api("DESKTOP_KEY")

    def call_gemini_api(self, api_key):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            prompt = f"Predict next winner for Moj Hungry Game (Items: {', '.join(HUNGRY_ITEMS)}). Response JSON format: {{\"item\": \"NAME\", \"confidence\": %, \"strategy\": \"...\"}}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            # Background request
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            res_data = response.json()
            text_response = res_data['candidates'][0]['content']['parts'][0]['text']
            data = json.loads(text_response.strip().replace('```json', '').replace('```', ''))
            
            self.run_js_safe(f"updatePrediction('{data['item'].upper()}', {data['confidence']}, '{data['strategy']}')")
            if self.prediction_timer: self.prediction_timer.cancel()
            self.prediction_timer = Clock.schedule_once(self.reset_ui, 10)
        except Exception as e:
            self.run_js_safe(f"updatePrediction('ERROR', 0, 'Link Error: Check Internet/Key')")

    def reset_ui(self, dt):
        self.run_js_safe("updatePrediction('WAITING', 0, 'Scanning round history...')")

    @run_on_ui_thread if platform == 'android' else lambda x: x
    def create_webview(self, *args):
        self.webview = WebView(Activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.setBackgroundColor(Color.TRANSPARENT)
        self.webview.setWebViewClient(WebViewClient())
        self.webview.loadUrl("file://" + os.path.join(os.getcwd(), "index.html"))
        Activity.addContentView(self.webview, LayoutParams(-1, -1))

    def run_js_safe(self, js):
        if platform == 'android': Clock.schedule_once(lambda dt: self.webview.evaluateJavascript(js, None), 0)
        else: print(f"JS: {js}")

if __name__ == '__main__':
    HungryHunterApp().run()
