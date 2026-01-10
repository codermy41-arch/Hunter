[app]
title = Hunter AI
package.name = hunterapp
package.domain = org.ai.hunter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js
version = 1.0

# Basic Requirements
requirements = python3,kivy==2.2.1,requests,urllib3,certifi,idna,chardet

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
