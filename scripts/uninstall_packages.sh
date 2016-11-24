#!/bin/bash

PACKAGES="
org.xwalk.usecase_webapi_xwalk_tests
org.xwalk.viewport
org.xwalk.embedded.api.sample
org.xwalk.embedded.api.asyncsample
org.xwalk.tct_mediacapture_w3c_tests
org.xwalk.embedded.api.permission
org.xwalk.extensions_ad
org.xwalk.core
org.xwalk.tct_fileapi_w3c_tests
org.xwalk.embedded.api.silentdownloadwithlzma
org.xwalk.webaudio
org.xwalk.assembly
org.xwalk.webapi_webrtc_w3c_tests
org.xwalk.webrtc
org.xwalk.embedded.api.silentdownload
org.xwalk.color_picker_crash
"

for package in $PACKAGES
do
	adb uninstall $package
done