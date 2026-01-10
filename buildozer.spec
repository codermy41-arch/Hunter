[app]
title = Hungry Hunter AI
package.name = hungryhunter
package.domain = org.ai.hunter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js
version = 1.0

# Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SYSTEM_ALERT_WINDOW

# Modern Android Settings
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
orientation = portrait
fullscreen = 0

# Requirements
requirements = python3,kivy,pandas,opencv-python,google-generativeai,numpy

[buildozer]
log_level = 2
warn_on_root = 1
