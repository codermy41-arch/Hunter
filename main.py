from kivy.app import App
from kivy.utils import platform
from kivy.clock import Clock
import os, csv, time

# Master List of Items
HUNGRY_ITEMS = ["Samosa", "Chai", "Softy", "Popcorn", "Chocolate", "Laddu", "Burger", "Pizza"]

class HungryHunterBot(App):
    current_round = 0
    mode = "TRAINING"
    is_running = False

    def build(self):
        # Create storage dir
        self.data_path = "/sdcard/HungryHunter"
        if platform == 'android':
            if not os.path.exists(self.data_path):
                os.makedirs(self.data_path)
        
        # This app will primarily live in the notification/overlay
        # The main UI is for setup and key injection
        return None 

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.SYSTEM_ALERT_WINDOW,
                Permission.FOREGROUND_SERVICE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            # Start the background service
            # (In a real Buildozer setup, we define the service in spec)
            self.start_floating_dot()

    def start_floating_dot(self):
        # Logic to create the "Big Dot" Overlay using Native Android Code via PyJnius
        try:
            from jnius import autoclass, cast
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            
            # This is where we would normally call a Java Service for the Floating Window
            # For this MVP, we use the Kivy Window with transparent background if possible,
            # but usually, a native Android Service is better for "Screen Recording" styles.
            pass
        except:
            pass

    def record_winner(self, item):
        self.current_round += 1
        file_path = os.path.join(self.data_path, "history.csv")
        with open(file_path, 'a') as f:
            f.write(f"{time.time()},{self.current_round},{item}\n")
        
        # Training Logic
        if self.current_round < 100:
            self.mode = "TRAINING"
        else:
            self.mode = "BULLSEYE"

if __name__ == '__main__':
    HungryHunterBot().run()
