from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.clock import Clock
import os
import json
import google.generativeai as genai

# Specific 8 Items for Moj Hungry Game
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
    # For Screen Capture (Requires complex Intent handshake, simplified here)
    MediaProjectionManager = autoclass('android.media.projection.MediaProjectionManager')
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
            request_permissions([
                Permission.INTERNET,
                Permission.SYSTEM_ALERT_WINDOW,
                Permission.FOREGROUND_SERVICE,
                Permission.FOREGROUND_SERVICE_MEDIA_PROJECTION
            ])
            Clock.schedule_once(self.create_webview, 0)

        # 1. Main Toggle Button (ON/OFF BACKGROUND SCAN)
        self.btn_main = Button(
            text="START AUTO-SCAN",
            size_hint=(0.45, 0.08),
            pos_hint={'center_x': 0.3, 'y': 0.05},
            background_normal='',
            background_color=(0, 0.8, 0.4, 0.9),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.btn_main.bind(on_press=self.toggle_auto_mode)
        self.layout.add_widget(self.btn_main)

        # 2. Manual Predict (Secondary)
        self.btn_predict = Button(
            text="AI PREDICT",
            size_hint=(0.4, 0.08),
            pos_hint={'center_x': 0.75, 'y': 0.05},
            background_normal='',
            background_color=(0, 0.6, 1, 0.9),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.btn_predict.bind(on_press=self.manual_predict)
        self.layout.add_widget(self.btn_predict)
        
        return self.layout

    def toggle_auto_mode(self, instance):
        self.auto_mode = not self.auto_mode
        if self.auto_mode:
            self.btn_main.text = "STOP SCANNING"
            self.btn_main.background_color = (1, 0.2, 0.2, 0.9)
            self.run_js_safe("updatePrediction('AUTO SCAN ON', 100, 'Monitoring Moj Hungry Game backend...')")
            # Start background monitoring (Interval 5 sec to check round end)
            Clock.schedule_interval(self.check_game_round, 5)
        else:
            self.btn_main.text = "START AUTO-SCAN"
            self.btn_main.background_color = (0, 0.8, 0.4, 0.9)
            Clock.unschedule(self.check_game_round)
            self.run_js_safe("updatePrediction('READY', 0, 'Auto-scan stopped.')")

    def check_game_round(self, dt):
        # Simulation: In real use, this captures screen and detects "Winning Animation"
        # If round detected as finished:
        self.manual_predict(None)

    def manual_predict(self, instance):
        self.run_js_safe("updatePrediction('ANALYZING...', 0, 'Capturing round history...')")
        
        # Fetch Key and Run AI
        if platform == 'android':
            from jnius import PythonJavaClass, java_method
            class KeyCallback(PythonJavaClass):
                __javainterfaces__ = ['android/webkit/ValueCallback']
                @java_method('(Ljava/lang/Object;)V')
                def onReceiveValue(self, value):
                    key = str(value).replace('"', '')
                    if key and key != "null":
                        Clock.schedule_once(lambda dt: self.outer.run_gemini_logic(key), 0)
                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer
            
            self.webview.evaluateJavascript("(function(){return localStorage.getItem('gh_key');})();", KeyCallback(self))
        else:
            self.run_gemini_logic("DESKTOP_KEY")

    def run_gemini_logic(self, api_key):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Specialized Prompt for Moj Hungry Game
            items_str = ", ".join(HUNGRY_ITEMS)
            prompt = f"""
            You are an expert predictor for the Moj India 'Hungry Game'.
            The 8 possible items are: {items_str}.
            Analyze the current game cycle and historical patterns.
            Predict which of these 8 items will win in the NEXT round.
            Response must be JSON: {{"item": "NAME", "confidence": %, "strategy": "..."}}
            Only use items from the list provided.
            """
            
            response = model.generate_content(prompt)
            data = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            
            # Show on screen
            self.run_js_safe(f"updatePrediction('{data['item'].upper()}', {data['confidence']}, '{data['strategy']}')")
            
            # 10 SECOND TIMER: Reset UI after 10 seconds
            if self.prediction_timer:
                self.prediction_timer.cancel()
            self.prediction_timer = Clock.schedule_once(self.reset_ui, 10)
            
        except Exception as e:
            self.run_js_safe(f"updatePrediction('ERROR', 0, 'AI Error: {str(e)[:40]}')")

    def reset_ui(self, dt):
        self.run_js_safe("updatePrediction('WAITING', 0, 'Scanning for next round end...')")

    @run_on_ui_thread if platform == 'android' else lambda x: x
    def create_webview(self, *args):
        self.webview = WebView(Activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setDomStorageEnabled(True)
        self.webview.setBackgroundColor(Color.TRANSPARENT)
        self.webview.setWebViewClient(WebViewClient())
        index_path = "file://" + os.path.join(os.getcwd(), "index.html")
        self.webview.loadUrl(index_path)
        Activity.addContentView(self.webview, LayoutParams(-1, -1))

    def run_js_safe(self, js):
        if platform == 'android':
            Clock.schedule_once(lambda dt: self.webview.evaluateJavascript(js, None), 0)
        else:
            print(f"JS: {js}")

if __name__ == '__main__':
    HungryHunterApp().run()
