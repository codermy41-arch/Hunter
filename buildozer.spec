[app]
title = Hungry Hunter AI
package.name = hungryhunter
package.domain = org.ai.hunter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js
version = 1.0

# Permissions
android.permissions = INTERNET, SYSTEM_ALERT_WINDOW, FOREGROUND_SERVICE, FOREGROUND_SERVICE_MEDIA_PROJECTION, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Modern Android Settings
android.api = 34
android.minapi = 23
android.sdk = 34
android.ndk = 25b
android.ndk_api = 23
orientation = portrait
fullscreen = 0

# Requirements
requirements = python3,kivy==2.3.0,pillow,requests,certifi,google-generativeai,pyjnius,android

# (Optional) For high performance video/image processing if needed later
# requirements = python3,kivy,opencv,numpy,google-generativeai,pyjnius,android

[buildozer]
log_level = 2
warn_on_root = 1
