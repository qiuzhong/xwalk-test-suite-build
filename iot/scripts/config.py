#!/usr/bin/env python3

OSTRO_CONFIG_FILE = "ostro_build_number.json"
OSTRO_LATEST_IMAGE_URL = "https://download.ostroproject.org/builds/ostro-os/latest/version"

OSTRO_XT_CONFIG_FILE = "ostro_xt_build_number.json"
OSTRO_XT_LATEST_IMAGE_URL = "http://download.ostroproject.org/builds/ostro-os-xt/latest"

proxies = {
    "http": "http://child-prc.intel.com:913",
    "https": "http://child-prc.intel.com:913",
    "all_proxy": "socks5://proxy-prc.intel.com:1080"
}

SMTP_SERVER = 'smtp.intel.com'
FROM_ADDR = 'zhongx.qiu@intel.com'
TO_ADDR = 'zhongx.qiu@intel.com'
CC_ADDR = ''


OSTRO_RELEASE_NOTIFICATION = 'Ostro image Release Notification!'
