
#!/bin/bash

MASTER_XWALK_BRANCH_NUM="23"
RELEASE_WORKSPACE="/home/banana/00_jiajia/work_space/custom_release"
MASTER_CTS_DIR="${RELEASE_WORKSPACE}/crosswalk-test-suite"
MASTER_CTS_TOOLS_DIR="${MASTER_CTS_DIR}/tools"
MASTER_CTS_BUILD_DIR="${MASTER_CTS_TOOLS_DIR}/build"

BETA20_CTS_DIR="${RELEASE_WORKSPACE}/crosswalk-test-suite-20"
BETA20_CTS_TOOLS_DIR="${BETA20_CTS_DIR}/tools"
BETA20_CTS_BUILD_DIR="${BETA20_CTS_TOOLS_DIR}/build"

BETA21_CTS_DIR="${RELEASE_WORKSPACE}/crosswalk-test-suite-21"
BETA21_CTS_TOOLS_DIR="${BETA21_CTS_DIR}/tools"
BETA21_CTS_BUILD_DIR="${BETA21_CTS_TOOLS_DIR}/build"

BETA22_CTS_DIR="${RELEASE_WORKSPACE}/crosswalk-test-suite-22"
BETA22_CTS_TOOLS_DIR="${BETA22_CTS_DIR}/tools"
BETA22_CTS_BUILD_DIR="${BETA22_CTS_TOOLS_DIR}/build"


DEMO_EXPRESS_DIR="${RELEASE_WORKSPACE}/demo-express"
PKG_TOOLS="${RELEASE_WORKSPACE}/pkg_tools"
PKG_TOOLS64="${RELEASE_WORKSPACE}/pkg_tools_64"

EMBEDDING_PACK_TYPES="ant"

DATA_DIR_PREFIX="/mnt/suites_storage/live/customizedPackages/crosswalk/android"
OTCQA_DIR_PREFIX="/mnt/otcqa/2016/customizedPackages/crosswalk/android"

MASTER_CTS_BRANCH="master"
MASTER_XWALK_BRANCH="master"

BETA20_CTS_BRANCH="Crosswalk-20"
BETA20_XWALK_BRANCH="beta"

BETA21_CTS_BRANCH="Crosswalk-21"
BETA21_XWALK_BRANCH="beta"

BETA22_CTS_BRANCH="Crosswalk-22"
BETA22_XWALK_BRANCH="beta"

CORDOVA_PLUGIN_XWALK_WEBVIEW_BRANCH="master"
CORDOVA_PLUGIN_XWALK_WEBVIEW_STABLE="release-testing"
DEMO_EXPRESS_BRANCH="master"

CORDOVA_APPS_LIST="
helloworld
loadExtension
mobilespec
privateNotes
remotedebugging
renamePkg
sampleRelease
setBackgroundColor
setUserAgent
spacedodge
statusbar
xwalkCommandLine
"

CCA_CORDOVA_APPS_LIST="
CIRC
Eh
"


BUILD_MODES="
embedded
shared
"

APK_ARCHES="
x86
x86_64
"

CORDOVA_ARCHES="
arm
arm64
"

EXTRA_PLUGINS="
usecase/usecase-cordova-android-tests/extra_plugins/cordova-admob
usecase/usecase-cordova-android-tests/extra_plugins/cordova-screenshot
webapi/webapi-appsecurity-external-tests/extra_plugins/com-intel-security-cordova-plugin
"

XWALK_TC_BUILD_DIR="/home/banana/01_qiuzhong/01-github/qiuzhong/xwalk-test-suite-build"
XWALK_EXTENSION_DIR="/home/banana/01_qiuzhong/release/xwalk_extension"

CTS_PATCH_DIR="/home/banana/00_jiajia/release_build/patch"
AIO_PATCH_DIR32="${CTS_PATCH_DIR}/aio/32"
AIO_PATCH_DIR64="${CTS_PATCH_DIR}/aio/64"
AIO_SERVICE_PACK_SCRIPT="misc/webapi-service-tests/pack.sh"
AIO_NONESERVICE_PACK_SCRIPT="misc/webapi-noneservice-tests/pack.sh"

AIO_TESTSUITE_LIST="
webapi-service-tests
webapi-noneservice-tests
webapi-service-docroot-tests
"

MASTER_USECASE_EMBEDDING_PATCH_DIR="${CTS_PATCH_DIR}/usecase-embedding/master"
USECASE_EMBEDDING_SILENT_MANIFEST="usecase/usecase-embedding-android-tests/embeddingapi-silentdownload/AndroidManifest.xml"
USECASE_EMBEDDING_SILENT_LZMA_MANIFEST="usecase/usecase-embedding-android-tests/embeddingapi-silentdownload-lzma/AndroidManifest.xml"

BETA20_EMBEDDINGAPI_API_PATCH_DIR="${CTS_PATCH_DIR}/embeddingapi/20"
BETA20_EMBEDDINGAPI_API_SUITE_JSON="embeddingapi/embedding-api-android-tests/suite.json"

XWALK_BINRARY_DIR="/home/banana/pkg_tools_android/canary"

CTS_URL="https://github.com/crosswalk-project/crosswalk-test-suite.git"