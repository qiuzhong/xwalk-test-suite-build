#!/bin/bash

set -e

source env.sh
source custom_config.sh

XWALK_BRANCH=$1
XWALK_VERSION=$2
MODE=$3
ARCH=$4
PACKAGE_TYPE=$5
TESTSUITE_NAME=$6
PUTON_JIAJIA=$7
PUTON_OTCQA=$8

PWD=$(pwd)
BRANCH_NUM=$(${PWD}/print_xwalk_branch_num.py ${XWALK_VERSION})
ARCH_BIT=$(${PWD}/print_xwalk_arch_bit.py ${ARCH})

CTS_DIR=""
CTS_TOOLS_DIR=""
CTS_BUILD_DIR=""
CTS_BRANCH=""
DATA_VERSION_DIR=""
OTCQA_VERSION_DIR=""

printBoldLine() {

    echo "********************************************************************************"
}

initDir() {

    if [ "${PUTON_JIAJIA}" == "true" ]; then
        DATA_VERSION_DIR=${DATA_DIR_PREFIX}/${XWALK_BRANCH}/${XWALK_VERSION}
        if [ ! -d ${DATA_VERSION_DIR} ]; then
            mkdir -pv ${DATA_VERSION_DIR}/testsuites-{embedded,shared}/{arm,x86,arm64,x86_64}
            mkdir -pv ${DATA_VERSION_DIR}/cordova4.x-{embedded,shared}/{arm,x86,arm64,x86_64}
        fi
    fi

    if [ "${PUTON_OTCQA}" == "true" ]; then
        OTCQA_VERSION_DIR=${OTCQA_DIR_PREFIX}/${XWALK_BRANCH}/${XWALK_VERSION}
        if [ ! -d ${OTCQA_VERSION_DIR} ]; then
            mkdir -pv ${OTCQA_VERSION_DIR}/testsuites-{embedded,shared}/{arm,x86,arm64,x86_64}
            mkdir -pv ${OTCQA_VERSION_DIR}/cordova4.x-{embedded,shared}/{arm,x86,arm64,x86_64}
        fi
    fi
}


configBranchVariables() {

    if [ ${BRANCH_NUM} == ${MASTER_XWALK_BRANCH_NUM} ] && [ ${XWALK_BRANCH} == "master" ]; then

        CTS_DIR=${MASTER_CTS_DIR}
        CTS_TOOLS_DIR=${MASTER_CTS_TOOLS_DIR}
        CTS_BUILD_DIR=${MASTER_CTS_BUILD_DIR}
        CTS_BRANCH=${MASTER_CTS_BRANCH}

    elif [ ${BRANCH_NUM} == "20" ]; then

        CTS_DIR=${BETA20_CTS_DIR}
        CTS_TOOLS_DIR=${BETA20_CTS_TOOLS_DIR}
        CTS_BUILD_DIR=${BETA20_CTS_BUILD_DIR}
        CTS_BRANCH=${BETA20_CTS_BRANCH}

    elif [ ${BRANCH_NUM} == "21" ]; then

        CTS_DIR=${BETA21_CTS_DIR}
        CTS_TOOLS_DIR=${BETA21_CTS_TOOLS_DIR}
        CTS_BUILD_DIR=${BETA21_CTS_BUILD_DIR}
        CTS_BRANCH=${BETA21_CTS_BRANCH}

    elif [ ${BRANCH_NUM} == "22" ]; then

        CTS_DIR=${BETA22_CTS_DIR}
        CTS_TOOLS_DIR=${BETA22_CTS_TOOLS_DIR}
        CTS_BUILD_DIR=${BETA22_CTS_BUILD_DIR}
        CTS_BRANCH=${BETA22_CTS_BRANCH}

    else
        echo "Wrong branch number:${BRANCH_NUM}!"
        exit 1
    fi

    CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR="${CTS_TOOLS_DIR}/cordova_plugins/cordova-plugin-crosswalk-webview"
    CORDOVA_PLUGIN_XWALK_WEBVIEW_GRADLE="${CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR}/platforms/android/xwalk.gradle"    
}

prepareCode() {
    if [ ! -d ${CTS_DIR} ]; then
        printBoldLine
        cd ${RELEASE_WORKSPACE}
        echo $CTS_DIR
        DEST_DIR=$(echo ${CTS_DIR} | awk -F/ '{ print $NF }')
        echo ${DEST_DIR}
        cp -a crosswalk-test-suite ${DEST_DIR}
        cd -
        printBoldLine
    fi

    USECASE_CORDOVA_EXTRA_PLUGINS_DIR="${CTS_DIR}/usecase/usecase-cordova-android-tests/extra_plugins"
    if [ ! -d ${USECASE_CORDOVA_EXTRA_PLUGINS_DIR}/cordova-admob ]; then
        printBoldLine
        cd ${USECASE_CORDOVA_EXTRA_PLUGINS_DIR}
        git clone https://github.com/floatinghotpot/cordova-admob-pro.git cordova-admob
        cd -
        printBoldLine
    fi

    if [ ! -d ${USECASE_CORDOVA_EXTRA_PLUGINS_DIR}/cordova-screenshot ]; then
        printBoldLine
        cd ${USECASE_CORDOVA_EXTRA_PLUGINS_DIR}
        git clone https://github.com/gitawego/cordova-screenshot.git cordova-screenshot
        cd -
        printBoldLine
    fi

    WEBAPI_APPSECURITY_EXTRA_PLUGINS_DIR="${CTS_DIR}/webapi/webapi-appsecurity-external-tests/extra_plugins"
    if [ ! -d ${WEBAPI_APPSECURITY_EXTRA_PLUGINS_DIR} ]; then
        printBoldLine
        mkdir -pv ${WEBAPI_APPSECURITY_EXTRA_PLUGINS_DIR}
        printBoldLine
    fi

    if [ ! -d ${WEBAPI_APPSECURITY_EXTRA_PLUGINS_DIR}/com-intel-security-cordova-plugin ]; then
        printBoldLine
        cd ${WEBAPI_APPSECURITY_EXTRA_PLUGINS_DIR}
        git clone https://github.com/AppSecurityApi/com-intel-security-cordova-plugin.git 
        cd -
        printBoldLine
    fi

    if [ ! -d ${CTS_TOOLS_DIR}/crosswalk-samples ]; then
        printBoldLine
        cd ${CTS_TOOLS_DIR}
        git clone https://github.com/crosswalk-project/crosswalk-samples.git
        cd -
        printBoldLine
    fi

    if [ ! -d ${CTS_TOOLS_DIR}/sample-my-private-notes ]; then
        printBoldLine
        cd ${CTS_TOOLS_DIR}
        git clone https://github.com/gomobile/sample-my-private-notes.git
        cd -
        printBoldLine
    fi

    if [ ! -d ${CTS_TOOLS_DIR}/mobilespec ]; then
        printBoldLine
        mkdir -pv ${CTS_TOOLS_DIR}/mobilespec
        printBoldLine
    fi

    if [ ! -d ${CTS_TOOLS_DIR}/mobilespec/cordova-mobile-spec ]; then
        printBoldLine
        cd ${CTS_TOOLS_DIR}/mobilespec
        git clone https://github.com/apache/cordova-mobile-spec.git
        cd -
        printBoldLine
    fi

    if [ ! -d ${CTS_TOOLS_DIR}/mobilespec/cordova-coho ]; then
        printBoldLine
        cd ${CTS_TOOLS_DIR}/mobilespec
        git clone https://github.com/apache/cordova-coho.git
        cd -
        printBoldLine
    fi

    if [ ! -d ${CTS_TOOLS_DIR}/circ ]; then
        printBoldLine
        cd ${CTS_TOOLS_DIR}
        git clone https://github.com/flackr/circ.git
        cd -
        printBoldLine
    fi

    if [ ! -d ${CTS_TOOLS_DIR}/workshop-cca-eh ]; then
        printBoldLine
        cd ${CTS_TOOLS_DIR}
        git clone https://github.com/MobileChromeApps/workshop-cca-eh.git
        cd -
        printBoldLine
    fi     
}

updateRepo() {
    repodir=$1
    gotobranch=$2

    printBoldLine

    cd ${repodir}

    git reset --hard HEAD
    git checkout ${gotobranch}
    git pull
    
    cd -
    printBoldLine
}

updateCode() {
    updateRepo ${DEMO_EXPRESS_DIR} ${DEMO_EXPRESS_BRANCH}
    updateRepo ${CTS_DIR} ${CTS_BRANCH}

    printBoldLine
    cd ${CTS_DIR}
    
    for extra_plugin in ${EXTRA_PLUGINS}
    do
        updateRepo ${CTS_DIR}/${extra_plugin} master  
    done

    cd -
    printBoldLine

    updateRepo ${CTS_TOOLS_DIR}/circ
    updateRepo ${CTS_TOOLS_DIR}/workshop-cca-eh
}

mergeUsecaseTC() {

    cd ${CTS_DIR}

    # if [ ${CTS_BRANCH} == "master" ]; then
        cp -dpRv ${DEMO_EXPRESS_DIR}/samples/* ${CTS_DIR}/usecase/usecase-webapi-xwalk-tests/samples/
        cp -dpRv ${DEMO_EXPRESS_DIR}/res/* ${CTS_DIR}/usecase/usecase-webapi-xwalk-tests/samples/
        unzip -o ${XWALK_EXTENSION_DIR}/fingerprint/v6/fingerprint.zip -d ${CTS_DIR}/usecase/usecase-webapi-xwalk-tests/samples/FingerPrint/fingerprint/
        unzip -o ${XWALK_EXTENSION_DIR}/iap/v6/iap.zip -d ${CTS_DIR}/usecase/usecase-webapi-xwalk-tests/samples/IAPGooglePlay/googleplay/iap/
        unzip -o ${XWALK_EXTENSION_DIR}/iap/v6/iap.zip -d ${CTS_DIR}/usecase/usecase-webapi-xwalk-tests/samples/IAPXiaomiStore/xiaomistore/iap/

        unzip -o ${XWALK_EXTENSION_DIR}/iap/v6/iap.zip -d ${CTS_DIR}/webapi/webapi-iap-xwalk-tests/iap/iap/

        cp -dpRv ${DEMO_EXPRESS_DIR}/samples-wrt/*  ${CTS_DIR}/usecase/usecase-wrt-android-tests/samples/

        cp -dpRv ${DEMO_EXPRESS_DIR}/samples-cordova/* ${CTS_DIR}/usecase/usecase-cordova-android-tests/samples

    # fi
    cd -
}

prepareTools32() {
    arch=$1
    packtype=$2
    mode=$3

    cd ${CTS_TOOLS_DIR}

    XWALK_SHELL_APK=${PKG_TOOLS}/crosswalk-test-apks-${XWALK_VERSION}-${arch}/XWalkCoreShell.apk
    if [ -f ${XWALK_SHELL_APK} ]; then
        rm -fv ${CTS_TOOLS_DIR}/XWalkCoreShell.apk
        cp -fv ${XWALK_SHELL_APK} ${CTS_TOOLS_DIR}/
    else
        echo "[tools] ${XWALK_SHELL_APK} does not exits!" 
        return 1
    fi

    if [ ${packtype} == "apk" ]; then
        XWALK_RT_APK=${PKG_TOOLS}/crosswalk-apks-${XWALK_VERSION}-${arch}/XWalkRuntimeLib.apk
        if [ -f ${XWALK_RT_APK} ]; then
            rm -fv ${CTS_TOOLS_DIR}/XWalkRuntimeLib.apk
            cp -fv ${XWALK_RT_APK} ${CTS_TOOLS_DIR}/
        else
            echo "[tools] ${XWALK_RT_APK} does not exists!" 
            return 1
        fi

        XWALK_DIR=${PKG_TOOLS}/crosswalk-${XWALK_VERSION}
        if [ -d ${XWALK_DIR} ]; then
            rm -fr ${CTS_TOOLS_DIR}/crosswalk
            cp -fr ${XWALK_DIR} ${CTS_TOOLS_DIR}/crosswalk
        else
            echo "[tools] ${XWALK_DIR} does not exits!" 
            return 1
        fi
    fi

    if [ ${packtype} == "cordova4.x" ]; then
        if [ -d ${CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR} ]; then
            if [ ${XWALK_BRANCH} == "stable" ]; then
                updateRepo ${CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR} ${CORDOVA_PLUGIN_XWALK_WEBVIEW_STABLE}
            else
                updateRepo ${CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR} ${CORDOVA_PLUGIN_XWALK_WEBVIEW_BRANCH}
            fi
        else
            echo "[cordova-plugin] cordova-plugin-crosswalk-webview does not exists!" 
            return 1
        fi

        if [ ${XWALK_BRANCH} == "master" ]; then
            begin_line=`sed -n "/maven {/ =" ${CORDOVA_PLUGIN_XWALK_WEBVIEW_GRADLE}`
            end_line=$[$begin_line + 2]

            sed -i "${begin_line},${end_line} d" ${CORDOVA_PLUGIN_XWALK_WEBVIEW_GRADLE}
            sed -i "${begin_line} i\      mavenLocal()" ${CORDOVA_PLUGIN_XWALK_WEBVIEW_GRADLE}

            if [ ${mode} == "embedded" ]; then
                EMBEDED_XWALK_AAR=${PKG_TOOLS}/crosswalk-${XWALK_VERSION}.aar
                if [ -f ${EMBEDED_XWALK_AAR} ]; then
                    mvn install:install-file -DgroupId=org.xwalk -DartifactId=xwalk_core_library -Dversion=${XWALK_VERSION} -Dpackaging=aar -Dfile=${EMBEDED_XWALK_AAR} -DgeneratePom=true
                else
                    echo "[tools] ${EMBEDED_XWALK_AAR} does not exists!" 
                    return 1
                fi
            elif [ ${mode} == "shared" ]; then
                SHARED_XWALK_AAR=${PKG_TOOLS}/crosswalk-shared-${XWALK_VERSION}.aar
                if [ -f ${SHARED_XWALK_AAR} ]; then
                    mvn install:install-file -DgroupId=org.xwalk -DartifactId=xwalk_shared_library -Dversion=${XWALK_VERSION} -Dpackaging=aar -Dfile=${SHARED_XWALK_AAR} -DgeneratePom=true
                else
                    echo "[tools] ${SHARED_XWALK_AAR} does not exists!" 
                    return 1
                fi
            else
                echo "[params] Unsupported cordova app mode with cordova-plugin-crosswalk-webview: ${mode}" 
                return 1
            fi
        fi
    fi

    if [ ${packtype} == "embeddingapi" ]; then
        XWALK_ARCH_WEBVIEW=${PKG_TOOLS}/crosswalk-webview-${XWALK_VERSION}-${arch}
        XWALK_CORE_LIBRARY=${PKG_TOOLS}/crosswalk-${XWALK_VERSION}/xwalk_core_library
        XWALK_SHARED_LIB=${PKG_TOOLS}/crosswalk-${XWALK_VERSION}/xwalk_shared_library
        if [ -d ${XWALK_ARCH_WEBVIEW} ]; then
            rm -fr ${CTS_TOOLS_DIR}/crosswalk-webview
            if [ ${mode} == "embedded" ]; then
                cp -fr ${XWALK_ARCH_WEBVIEW} ${CTS_TOOLS_DIR}/crosswalk-webview
            elif [ ${mode} == "shared" ]; then
                cp -fr ${XWALK_SHARED_LIB} ${CTS_TOOLS_DIR}/crosswalk-webview
                if [ ${TESTSUITE_NAME} != "usecase-embedding-android-tests" ]; then
                    rm -fv ${CTS_TOOLS_DIR}/crosswalk-webview/libs/*.jar
                    cp -fv ${XWALK_CORE_LIBRARY}/libs/*.jar ${CTS_TOOLS_DIR}/crosswalk-webview/libs/
                fi
            else
                echo "Unsupported building mode: ${mode}!"
                return 1
            fi
        else
            echo "[tools] ${XWALK_ARCH_WEBVIEW} does not exists!" 
            return 1
        fi
    fi   
}

prepareTools64() {
    arch=$1
    packtype=$2
    mode=$3

    cd ${CTS_TOOLS_DIR}

    XWALK_SHELL_APK=${PKG_TOOLS64}/crosswalk-test-apks-${XWALK_VERSION}-${arch}/XWalkCoreShell.apk
    if [ -f ${XWALK_SHELL_APK} ]; then
        rm -fv ${CTS_TOOLS_DIR}/XWalkCoreShell.apk
        cp -fv ${XWALK_SHELL_APK} ${CTS_TOOLS_DIR}/
    else
        echo "[tools] ${XWALK_SHELL_APK} does not exits!" 
        return 1
    fi

    if [ ${packtype} == "apk" ]; then
        XWALK_RT_APK=${PKG_TOOLS64}/crosswalk-apks-${XWALK_VERSION}-${arch}/XWalkRuntimeLib.apk
        if [ -f ${XWALK_RT_APK} ]; then
            rm -fv ${CTS_TOOLS_DIR}/XWalkRuntimeLib.apk
            cp -fv ${XWALK_RT_APK} ${CTS_TOOLS_DIR}/
        else
            echo "[tools] ${XWALK_RT_APK} does not exists!" 
            return 1
        fi

        XWALK_DIR64=${PKG_TOOLS64}/crosswalk-${XWALK_VERSION}-64bit
        if [ -d ${XWALK_DIR} ]; then
            rm -fr ${CTS_TOOLS_DIR}/crosswalk
            cp -fr ${XWALK_DIR64} ${CTS_TOOLS_DIR}/crosswalk
        else
            echo "[tools] ${XWALK_DIR} does not exits!" 
            return 1
        fi
    fi

    if [ ${packtype} == "cordova4.x" ]; then
        if [ -d ${CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR} ]; then
            if [ ${XWALK_BRANCH} == "stable" ]; then
                updateRepo ${CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR} ${CORDOVA_PLUGIN_XWALK_WEBVIEW_STABLE}
            else
                updateRepo ${CORDOVA_PLUGIN_XWALK_WEBVIEW_DIR} ${CORDOVA_PLUGIN_XWALK_WEBVIEW_BRANCH}
            fi
        else
            echo "[cordova-plugin] cordova-plugin-crosswalk-webview does not exists!" 
            return 1
        fi

        if [ ${XWALK_BRANCH} == "master" ]; then
            begin_line=`sed -n "/maven {/ =" ${CORDOVA_PLUGIN_XWALK_WEBVIEW_GRADLE}`
            end_line=$[$begin_line + 2]

            sed -i "${begin_line},${end_line} d" ${CORDOVA_PLUGIN_XWALK_WEBVIEW_GRADLE}
            sed -i "${begin_line} i\      mavenLocal()" ${CORDOVA_PLUGIN_XWALK_WEBVIEW_GRADLE}

            if [ ${mode} == "embedded" ]; then
                EMBEDED_XWALK_AAR=${PKG_TOOLS64}/crosswalk-${XWALK_VERSION}-64bit.aar
                if [ -f ${EMBEDED_XWALK_AAR} ]; then
                    mvn install:install-file -DgroupId=org.xwalk -DartifactId=xwalk_core_library -Dversion=${XWALK_VERSION} -Dpackaging=aar -Dfile=${EMBEDED_XWALK_AAR} -DgeneratePom=true -Dclassifier=64bit
                else
                    echo "[tools] ${EMBEDED_XWALK_AAR} does not exists!" 
                    return 1
                fi
            elif [ ${mode} == "shared" ]; then
                SHARED_XWALK_AAR=${PKG_TOOLS64}/crosswalk-shared-${XWALK_VERSION}.aar
                if [ -f ${SHARED_XWALK_AAR} ]; then
                    echo "mvn install:install-file -DgroupId=org.xwalk -DartifactId=xwalk_shared_library -Dversion=${XWALK_VERSION} -Dpackaging=aar -Dfile=${SHARED_XWALK_AAR} -DgeneratePom=true"
                else
                    echo "[tools] ${SHARED_XWALK_AAR} does not exists!" 
                    return 1
                fi
            else
                echo "[params] Unsupported cordova app mode with cordova-plugin-crosswalk-webview: ${mode}" 
                return 1
            fi
        fi
    fi

    if [ ${packtype} == "embeddingapi" ]; then
        
        XWALK_ARCH_WEBVIEW=${PKG_TOOLS64}/crosswalk-webview-${XWALK_VERSION}-${arch}
        XWALK_CORE_LIBRARY=${PKG_TOOLS64}/crosswalk-${XWALK_VERSION}-64bit/xwalk_core_library
        XWALK_SHARED_LIB=${PKG_TOOLS64}/crosswalk-${XWALK_VERSION}-64bit/xwalk_shared_library
        if [ -d ${XWALK_ARCH_WEBVIEW} ]; then
            rm -fr ${CTS_TOOLS_DIR}/crosswalk-webview
            if [ ${mode} == "embedded" ]; then
                cp -fr ${XWALK_ARCH_WEBVIEW} ${CTS_TOOLS_DIR}/crosswalk-webview
            elif [ ${mode} == "shared" ]; then
                cp -fr ${XWALK_SHARED_LIB} ${CTS_TOOLS_DIR}/crosswalk-webview
                if [ ${TESTSUITE_NAME} != "usecase-embedding-android-tests" ]; then
                    rm -fv ${CTS_TOOLS_DIR}/crosswalk-webview/libs/*.jar
                    cp -fv ${XWALK_CORE_LIBRARY}/libs/*.jar ${CTS_TOOLS_DIR}/crosswalk-webview/libs/
                fi
            else
                echo "Unsupported building mode: ${mode}!"
                return 1
            fi
        else
            echo "[tools] ${XWALK_ARCH_WEBVIEW} does not exists!" 
            return 1
        fi
    fi
}

patchTestSuite() {

    if [ ${ARCH_BIT} == "32" ]; then

        cp -fv ${AIO_PATCH_DIR32}/${AIO_SERVICE_PACK_SCRIPT} ${CTS_DIR}/${AIO_SERVICE_PACK_SCRIPT}
        cp -fv ${AIO_PATCH_DIR32}/${AIO_NONESERVICE_PACK_SCRIPT} ${CTS_DIR}/${AIO_NONESERVICE_PACK_SCRIPT}

    elif [ ${ARCH_BIT} == "64" ]; then

        cp -fv ${AIO_PATCH_DIR64}/${AIO_SERVICE_PACK_SCRIPT} ${CTS_DIR}/${AIO_SERVICE_PACK_SCRIPT}
        cp -fv ${AIO_PATCH_DIR64}/${AIO_NONESERVICE_PACK_SCRIPT} ${CTS_DIR}/${AIO_NONESERVICE_PACK_SCRIPT}

    fi

    cp -fv ${MASTER_USECASE_EMBEDDING_PATCH_DIR}/${USECASE_EMBEDDING_SILENT_MANIFEST} ${CTS_DIR}/${USECASE_EMBEDDING_SILENT_MANIFEST}
    cp -fv ${MASTER_USECASE_EMBEDDING_PATCH_DIR}/${USECASE_EMBEDDING_SILENT_LZMA_MANIFEST} ${CTS_DIR}/${USECASE_EMBEDDING_SILENT_LZMA_MANIFEST}


    if [ ${BRANCH_NUM} == "20" ]; then
        cp -fv ${BETA20_EMBEDDINGAPI_API_PATCH_DIR}/${BETA20_EMBEDDINGAPI_API_SUITE_JSON} ${CTS_DIR}/${BETA20_EMBEDDINGAPI_API_SUITE_JSON}
    fi
}

copyDemoExpress() {

    echo "Copying demo-express/sampes/* to usecase-webapi-xwalk-tests/samples/..."
    cp -dpRv ${}

}

packApk() {
    arch=$1
    mode=$2
    apk=$3

    cd ${CTS_DIR}
    if [ ${apk} == "usecase-extension-android-tests" ]; then
        cp -fv ${CTS_PATCH_DIR}/tools/build/build_extension.py ./tools/build/
    fi
    apk_tc_dir=`find ${CTS_DIR} -name ${apk} -type d`
    ${CTS_BUILD_DIR}/pack.py -t apk -a ${arch} -m ${mode} -s ${apk_tc_dir} -d ${DATA_VERSION_DIR}/testsuites-${mode}/${arch} --tools=${CTS_TOOLS_DIR}
    [ $? -ne 0 ] && echo "[Apk] [${arch}] [${mode}] ${apk}"

    if [ "${PUTON_OTCQA}" == "true" ]; then
        cp -fv ${DATA_VERSION_DIR}/testsuites-${mode}/${arch}/${TESTSUITE_NAME}-${XWALK_VERSION}-1.apk.zip ${OTCQA_VERSION_DIR}/testsuites-${mode}/${arch}/
    fi

    cd -
}

packCordova() {
    arch=$1
    mode=$2
    cordova=$3

    cd ${CTS_DIR}

    cordova_tc_dir=`find ${CTS_DIR} -name ${cordova} -type d`
    ${CTS_BUILD_DIR}/pack.py -t cordova -a ${arch} -m ${mode} -s ${cordova_tc_dir} -d ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch} --tools=${CTS_TOOLS_DIR}
    [ $? -ne 0 ] && echo "[Cordova] [${arch}] [${mode}] ${cordova}" 

    if [ "${PUTON_OTCQA}" == "true" ]; then
        cp -fv ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}/${TESTSUITE_NAME}-${XWALK_VERSION}-1.cordova.zip ${OTCQA_VERSION_DIR}/cordova4.x-${mode}/${arch}/
    fi

    cd -
}

packCordovaSampleApp() {
    arch=$1
    mode=$2
    cordovaapp=$3

    cd ${CTS_BUILD_DIR}

    rm -fv *.apk
    rm -fv *.zip

    ${CTS_BUILD_DIR}/pack_cordova_sample.py -t cordova -a ${arch} -m ${mode}
    [ $? -ne 0 ] && echo "[Cordova] [${arch}] [${mode}] ${cordova}" 

    if [ -f ${cordovasample}.apk ]; then
        if [ ! -d ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch} ]; then
            mkdir -pv ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}
        fi
        mv -fv ${cordovaapp}.apk ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}/
    fi

    if [ "${PUTON_OTCQA}" == "true" ]; then
        cp -fv ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}/${cordovaapp}.apk ${OTCQA_VERSION_DIR}/cordova4.x-${mode}/${arch}/
    fi

    cd -
}

packCordovaSampleApp() {
    arch=$1
    mode=$2
    cordova_app=$3

    cd ${CTS_BUILD_DIR}

    rm -fv *.apk

    sed -i "s|DEFAULT_CMD_TIMEOUT * 5|DEFAULT_CMD_TIMEOUT * 10|g" ./pack_cordova_sample.py
    ./pack_cordova_sample.py -n ${cordova_app} -a ${arch} -m ${mode} -p 000 --tools=${CTS_TOOLS_DIR}
    mv -fv ${cordova_app}.apk ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}
    [ $? -ne 0 ] && echo "[CordovaApp] [${arch}] [${mode}] ${cordova_app}" 

    if [ "${PUTON_OTCQA}" == "true" ]; then
        cp -fv ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}/${cordova_app}.apk ${OTCQA_VERSION_DIR}/cordova4.x-${mode}/${arch}/
    fi   

    cd -
}

packEmbeddingApi() {
    arch=$1
    mode=$2
    embeddingapi=$3

    cd ${CTS_DIR}

    embeddingapi_tc_dir=`find ${CTS_DIR} -name ${embeddingapi} -type d`
    if [ ${mode} == "shared" ]; then
        # find ${CTS_TOOLS_DIR}/crosswalk-webview/ -name "libxwalkcore.so" -exec rm -fv {} \;
        ${CTS_BUILD_DIR}/pack.py -t embeddingapi --pack-type ant -s ${embeddingapi_tc_dir} -d ${DATA_VERSION_DIR}/testsuites-${mode}/${arch} --tools=${CTS_TOOLS_DIR}
    elif [ ${mode} == "embedded" ]; then
            ${CTS_BUILD_DIR}/pack.py -t embeddingapi --pack-type ant -s ${embeddingapi_tc_dir} -d ${DATA_VERSION_DIR}/testsuites-${mode}/${arch} --tools=${CTS_TOOLS_DIR}
    fi

    [ $? -ne 0 ] && echo "[EmbeddingApi] [${arch}] [${mode}] ${embeddingapi}" 

    if [ "${PUTON_OTCQA}" == "true" ]; then
        cp -fv ${DATA_VERSION_DIR}/testsuites-${mode}/${arch}/${TESTSUITE_NAME}-${XWALK_VERSION}-1.embeddingapi-${EMBEDDING_PACK_TYPES}.zip ${OTCQA_VERSION_DIR}/testsuites-${mode}/${arch}/
    fi

    cd -
}

packAio() {
    arch=$1
    mode=$2
    packtype=$3
    aio=$4

    cd ${CTS_DIR}

    aio_dir=`find ${CTS_DIR} -name ${aio} -type d`
    cd ${aio_dir}
    cp -a ${CTS_TOOLS_DIR}/resources/webrunner ./webrunner
    rm -fv *.zip

    if [ ${packtype} == "apk" ]; then
        ./pack.sh -t apk -a ${arch} -m ${mode} -d ${DATA_VERSION_DIR}/testsuites-${mode}/${arch}
        [ $? -ne 0 ] && echo "[ApkAio] [${arch}] [${mode}] ${aio}" 

        if [ "${PUTON_OTCQA}" == "true" ]; then
            cp -fv ${DATA_VERSION_DIR}/testsuites-${mode}/${arch}/${TESTSUITE_NAME}-${XWALK_VERSION}-1.apk.zip ${OTCQA_VERSION_DIR}/testsuites-${mode}/${arch}/
        fi

    elif [ ${packtype} == "cordova" ]; then
        ./pack.sh -t cordova -a ${arch} -m ${mode} -d ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}
        [ $? -ne 0 ] && echo "[CordovaAio] [${arch}] [${mode}] ${aio}"

        if [ "${PUTON_OTCQA}" == "true" ]; then
            cp -fv ${DATA_VERSION_DIR}/cordova4.x-${mode}/${arch}/${TESTSUITE_NAME}-${XWALK_VERSION}-1.cordova.zip ${OTCQA_VERSION_DIR}/cordova4.x-${mode}/${arch}/
        fi        
    fi
}

updateXwalkVersion() {
    printBoldLine
    cd ${XWALK_TC_BUILD_DIR}/scripts
    ./update_cts_version.py -v ${XWALK_VERSION} -d ${CTS_DIR}
    if [ ${XWALK_BRANCH} == "stable" ]; then
        sed -i "s/beta/stable/g" ${CTS_DIR}/VERSION
    fi
    cd -
    printBoldLine
}

checkXWalkZip() {

    printBoldLine
    cd ${XWALK_TC_BUILD_DIR}/scripts

    if [ ${ARCH_BIT} == "32" ]; then
        ./download_xwalk_zip.py -v ${XWALK_VERSION} -a
    elif [ ${ARCH_BIT} == "64" ]; then
        ./download_xwalk_zip.py -v ${XWALK_VERSION} -a -l
    fi
    cd -
    printBoldLine
}


main() {

    initDir
    configBranchVariables
    prepareCode
    updateCode
    updateXwalkVersion
    mergeUsecaseTC
    patchTestSuite

    checkXWalkZip

    case ${PACKAGE_TYPE} in 
    apk) 
        if [ ${ARCH_BIT} == "32" ]; then
            prepareTools32 ${ARCH} apk
        elif [ ${ARCH_BIT} == "64" ]; then
            prepareTools64 ${ARCH} apk
        else
            echo "Unsupported packing type"
            exit 1
        fi

        packApk ${ARCH} ${MODE} ${TESTSUITE_NAME}
        ;;
    cordova)
        if [ ${ARCH_BIT} == "32" ]; then
            prepareTools32 ${ARCH} cordova4.x ${MODE}
        elif [ ${ARCH_BIT} == "64" ]; then
            prepareTools64 ${ARCH} cordova4.x ${MODE}
        else
            echo "Unsupported packing type"
            exit 1
        fi

        packCordova ${ARCH} ${MODE} ${TESTSUITE_NAME}
        ;;
    cordovasampleapp)
        if [ ${ARCH_BIT} == "32" ]; then
            prepareTools32 ${ARCH} cordova4.x ${MODE}
        elif [ ${ARCH_BIT} == "64" ]; then
            prepareTools64 ${ARCH} cordova4.x ${MODE}
        else
            echo "Unsupported packing type"
            exit 1
        fi

        packCordovaSampleApp ${ARCH} ${MODE} ${TESTSUITE_NAME}
        cd -
        ;;       
    embeddingapi)
        if [ ${ARCH_BIT} == "32" ]; then
            prepareTools32 ${ARCH} embeddingapi ${MODE}
        elif [ ${ARCH_BIT} == "64" ];then
            prepareTools64 ${ARCH} embeddingapi ${MODE}
        else
            echo "Unsupported packing type"
            exit 1
        fi

        packEmbeddingApi ${ARCH} ${MODE} ${TESTSUITE_NAME}
        ;;
    apk-aio)
        if [ ${ARCH_BIT} == "32" ]; then
            prepareTools32 ${ARCH} apk
        elif [ ${ARCH_BIT} == "64" ]; then
            prepareTools64 ${ARCH} apk
        else
            echo "Unsupported packing type"
            exit 1
        fi

        packAio ${ARCH} ${MODE} apk ${TESTSUITE_NAME}                
        ;;
    cordova-aio)
        if [ ${ARCH_BIT} == "32" ]; then
            prepareTools32 ${ARCH} apk
        elif [ ${ARCH_BIT} == "64" ]; then
            prepareTools64 ${ARCH} apk
        else
            echo "Unsupported packing type"
            exit 1
        fi

        packAio ${ARCH} ${MODE} cordova ${TESTSUITE_NAME}    
        ;;

    *)
        exit 1
        ;;
    esac
}


main
