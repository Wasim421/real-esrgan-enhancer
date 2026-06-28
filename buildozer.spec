[app]
title = ESRGAN Enhancer
package.name = esrganenhancer
package.domain = org.esrgan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,onnx
version = 1.0
requirements = python3,kivy==2.3.0,numpy,pillow
orientation = portrait
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
[buildozer]
log_level = 2
