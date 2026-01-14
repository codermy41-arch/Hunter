[app]
title = Hungry Hunter Pro
package.name = hunterpro
package.domain = org.mojhunter.ai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js
version = 1.0
orientation = portrait
fullscreen = 0

# Zaroori Permissions
android.permissions = INTERNET, SYSTEM_ALERT_WINDOW, FOREGROUND_SERVICE

# Android SDK/NDK Settings (Ultra Stable)
android.api = 33
android.minapi = 23
android.sdk = 33
android.ndk = 25b
android.ndk_api = 23

# Requirements (Ab 'google-generativeai' hata diya hai)
requirements = python3,kivy==2.3.0,requests,certifi,urllib3,idna,charset-normalizer,pyjnius,android

[buildozer]
log_level = 2
