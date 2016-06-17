# Cordova for Android on Linux host environment setup
## Prerequisites:
* Ubuntu Linux 14.04 x86_64
* [Crosswalk for Android on Linux environment ready](https://github.com/qiuzhong/xwalk-test-suite-build/docs/01_xwalk_for_android_on_linux_host.md)

## Notice:
In this guide, we will install all the tools (except for the node) at **~/xwalk/**
```Bash
$ mkdir -pv ~/xwalk
```

All the tools are supposed to stored at **~/Downloads**

## Install Maven build tool
```
$ cd ~/Downloads
$ tar -xvf apache-maven-3.3.9-bin.tar.gz
$ mv -fv apache-maven-3.3.9 ~/xwalk/
$ vim ~/.bashrc
export MAVEN_HOME=~/xwalk/apache-maven-3.3.9
export PATH=$PATH:$MAVEN_HOME/bin
```

## Install Cordova CLI
```
$ sudo npm install -g cordova --verbose
$ cordova -v
6.2.0
```

## Build a simple cordova app
```
$ cordova create org.xwalk.foo
$ cd org.xwalk.foo
$ cordova platform add android
$ cordova build android
ANDROID_HOME=<path/to/ANDROID_HOME>
JAVA_HOME=<path/to/JAVA_HOME>
Downloading http://services.gradle.org.distribution/gradle-2.2.1-all.zip
```

For the first time cordova building application, it will try to download the gradle-2.2.1-all.zip. But if you didn't set the correct proxy for it, you may encounter the error log like this:
```
ANDROID_HOME=/home/andersqiu/xwalk/android/android-sdk-linux
JAVA_HOME=/home/andersqiu/xwalk/android/java/jdk1.8.0_74
Downloading http://services.gradle.org/distributions/gradle-2.2.1-all.zip

Exception in thread "main" java.lang.RuntimeException: java.net.ConnectException: Connection timed out
	at org.gradle.wrapper.ExclusiveFileAccessManager.access(ExclusiveFileAccessManager.java:78)
	at org.gradle.wrapper.Install.createDist(Install.java:47)
	at org.gradle.wrapper.WrapperExecutor.execute(WrapperExecutor.java:129)
	at org.gradle.wrapper.GradleWrapperMain.main(GradleWrapperMain.java:48)
Caused by: java.net.ConnectException: Connection timed out
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:589)
	at java.net.Socket.connect(Socket.java:538)
	at sun.net.NetworkClient.doConnect(NetworkClient.java:180)
	at sun.net.www.http.HttpClient.openServer(HttpClient.java:432)
	at sun.net.www.http.HttpClient.openServer(HttpClient.java:527)
	at sun.net.www.http.HttpClient.<init>(HttpClient.java:211)
	at sun.net.www.http.HttpClient.New(HttpClient.java:308)
	at sun.net.www.http.HttpClient.New(HttpClient.java:326)
	at sun.net.www.protocol.http.HttpURLConnection.getNewHttpClient(HttpURLConnection.java:1169)
	at sun.net.www.protocol.http.HttpURLConnection.plainConnect0(HttpURLConnection.java:1105)
	at sun.net.www.protocol.http.HttpURLConnection.plainConnect(HttpURLConnection.java:999)
	at sun.net.www.protocol.http.HttpURLConnection.connect(HttpURLConnection.java:933)
	at sun.net.www.protocol.http.HttpURLConnection.getInputStream0(HttpURLConnection.java:1513)
	at sun.net.www.protocol.http.HttpURLConnection.getInputStream(HttpURLConnection.java:1441)
	at org.gradle.wrapper.Download.downloadInternal(Download.java:59)
	at org.gradle.wrapper.Download.download(Download.java:45)
	at org.gradle.wrapper.Install$1.call(Install.java:60)
	at org.gradle.wrapper.Install$1.call(Install.java:47)
	at org.gradle.wrapper.ExclusiveFileAccessManager.access(ExclusiveFileAccessManager.java:65)
	... 3 more
Error: Error code 1 for command: /tmp/org.xwalk.foo/platforms/android/gradlew with args: cdvBuildDebug,-b,/tmp/org.xwalk.foo/platforms/android/build.gradle,-Dorg.gradle.daemon=true,-Pandroid.useDeprecatedNdk=true
```

### Solution to fix this issue:
```
$ vim ~/.bashrc
export JAVA_OPTS="-Dhttp.proxyHost=child-prc.intel.com -Dhttp.proxyPort=913 -Dhttps.proxyHost=child-prc.intel.com -Dhttps.proxyPort=913"
```

Gradle now can be downloaded successfully, then it will download a lot of other necessary files.
```
Downloading http://services.gradle.org/distributions/gradle-2.2.1-all.zip
..................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
Unzipping /home/andersqiu/.gradle/wrapper/dists/gradle-2.2.1-all/2m8005s69iu8v0oiejfej094b/gradle-2.2.1-all.zip to /home/andersqiu/.gradle/wrapper/dists/gradle-2.2.1-all/2m8005s69iu8v0oiejfej094b
Set executable permissions for: /home/andersqiu/.gradle/wrapper/dists/gradle-2.2.1-all/2m8005s69iu8v0oiejfej094b/gradle-2.2.1/bin/gradle
Download https://repo1.maven.org/maven2/com/android/tools/build/gradle/1.5.0/gradle-1.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/build/gradle-core/1.5.0/gradle-core-1.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/build/builder/1.5.0/builder-1.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/lint/lint/24.5.0/lint-24.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/build/transform-api/1.5.0/transform-api-1.5.0.pom
Download https://repo1.maven.org/maven2/com/android/databinding/compilerCommon/1.0-rc5/compilerCommon-1.0-rc5.pom
Download https://repo1.maven.org/maven2/net/sf/proguard/proguard-gradle/5.2.1/proguard-gradle-5.2.1.pom
Download https://repo1.maven.org/maven2/net/sf/proguard/proguard-parent/5.2.1/proguard-parent-5.2.1.pom
Download https://repo1.maven.org/maven2/org/jacoco/org.jacoco.core/0.7.4.201502262128/org.jacoco.core-0.7.4.201502262128.pom
Download https://repo1.maven.org/maven2/org/jacoco/org.jacoco.build/0.7.4.201502262128/org.jacoco.build-0.7.4.201502262128.pom
Download https://repo1.maven.org/maven2/com/android/tools/build/builder-model/1.5.0/builder-model-1.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/build/builder-test-api/1.5.0/builder-test-api-1.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/sdklib/24.5.0/sdklib-24.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/sdk-common/24.5.0/sdk-common-24.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/common/24.5.0/common-24.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/build/manifest-merger/24.5.0/manifest-merger-24.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/ddms/ddmlib/24.5.0/ddmlib-24.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/jack/jack-api/0.9.0/jack-api-0.9.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/jill/jill-api/0.9.0/jill-api-0.9.0.pom
Download https://repo1.maven.org/maven2/com/squareup/javawriter/2.5.0/javawriter-2.5.0.pom
Download https://repo1.maven.org/maven2/org/sonatype/oss/oss-parent/7/oss-parent-7.pom
Download https://repo1.maven.org/maven2/org/bouncycastle/bcpkix-jdk15on/1.48/bcpkix-jdk15on-1.48.pom
Download https://repo1.maven.org/maven2/org/bouncycastle/bcprov-jdk15on/1.48/bcprov-jdk15on-1.48.pom
Download https://repo1.maven.org/maven2/org/ow2/asm/asm/5.0.3/asm-5.0.3.pom
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-parent/5.0.3/asm-parent-5.0.3.pom
Download https://repo1.maven.org/maven2/org/ow2/ow2/1.3/ow2-1.3.pom
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-tree/5.0.3/asm-tree-5.0.3.pom
Download https://repo1.maven.org/maven2/org/antlr/antlr-runtime/3.5.2/antlr-runtime-3.5.2.pom
Download https://repo1.maven.org/maven2/org/antlr/antlr-master/3.5.2/antlr-master-3.5.2.pom
Download https://repo1.maven.org/maven2/org/sonatype/oss/oss-parent/9/oss-parent-9.pom
Download https://repo1.maven.org/maven2/org/antlr/antlr/3.5.2/antlr-3.5.2.pom
Download https://repo1.maven.org/maven2/com/android/tools/lint/lint-checks/24.5.0/lint-checks-24.5.0.pom
Download https://repo1.maven.org/maven2/org/eclipse/jdt/core/compiler/ecj/4.4.2/ecj-4.4.2.pom
Download https://repo1.maven.org/maven2/com/android/tools/annotations/24.5.0/annotations-24.5.0.pom
Download https://repo1.maven.org/maven2/com/google/guava/guava/17.0/guava-17.0.pom
Download https://repo1.maven.org/maven2/com/google/guava/guava-parent/17.0/guava-parent-17.0.pom
Download https://repo1.maven.org/maven2/com/android/databinding/baseLibrary/1.0-rc5/baseLibrary-1.0-rc5.pom
Download https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.3.2/commons-lang3-3.3.2.pom
Download https://repo1.maven.org/maven2/org/apache/commons/commons-parent/33/commons-parent-33.pom
Download https://repo1.maven.org/maven2/org/apache/apache/13/apache-13.pom
Download https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4/4.5/antlr4-4.5.pom
Download https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4-master/4.5/antlr4-master-4.5.pom
Download https://repo1.maven.org/maven2/commons-io/commons-io/2.4/commons-io-2.4.pom
Download https://repo1.maven.org/maven2/org/apache/commons/commons-parent/25/commons-parent-25.pom
Download https://repo1.maven.org/maven2/org/apache/apache/9/apache-9.pom
Download https://repo1.maven.org/maven2/com/googlecode/juniversalchardet/juniversalchardet/1.0.3/juniversalchardet-1.0.3.pom
Download https://repo1.maven.org/maven2/net/sf/proguard/proguard-base/5.2.1/proguard-base-5.2.1.pom
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-debug-all/5.0.1/asm-debug-all-5.0.1.pom
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-parent/5.0.1/asm-parent-5.0.1.pom
Download https://repo1.maven.org/maven2/com/android/tools/layoutlib/layoutlib-api/24.5.0/layoutlib-api-24.5.0.pom
Download https://repo1.maven.org/maven2/com/android/tools/dvlib/24.5.0/dvlib-24.5.0.pom
Download https://repo1.maven.org/maven2/com/google/code/gson/gson/2.2.4/gson-2.2.4.pom
Download https://repo1.maven.org/maven2/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.pom
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.1.1/httpclient-4.1.1.pom
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcomponents-client/4.1.1/httpcomponents-client-4.1.1.pom
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/project/4.1.1/project-4.1.1.pom
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpmime/4.1/httpmime-4.1.pom
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcomponents-client/4.1/httpcomponents-client-4.1.pom
Download https://repo1.maven.org/maven2/net/sf/kxml/kxml2/2.3.0/kxml2-2.3.0.pom
Download https://repo1.maven.org/maven2/org/antlr/ST4/4.0.8/ST4-4.0.8.pom
Download https://repo1.maven.org/maven2/com/android/tools/lint/lint-api/24.5.0/lint-api-24.5.0.pom
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-analysis/5.0.3/asm-analysis-5.0.3.pom
Download https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4-runtime/4.5/antlr4-runtime-4.5.pom
Download https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4-annotations/4.5/antlr4-annotations-4.5.pom
Download https://repo1.maven.org/maven2/com/intellij/annotations/12.0/annotations-12.0.pom
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcore/4.1/httpcore-4.1.pom
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcomponents-core/4.1/httpcomponents-core-4.1.pom
Download https://repo1.maven.org/maven2/commons-logging/commons-logging/1.1.1/commons-logging-1.1.1.pom
Download https://repo1.maven.org/maven2/org/apache/commons/commons-parent/5/commons-parent-5.pom
Download https://repo1.maven.org/maven2/org/apache/apache/4/apache-4.pom
Download https://repo1.maven.org/maven2/commons-codec/commons-codec/1.4/commons-codec-1.4.pom
Download https://repo1.maven.org/maven2/org/apache/commons/commons-parent/11/commons-parent-11.pom
Download https://repo1.maven.org/maven2/com/android/tools/external/lombok/lombok-ast/0.2.3/lombok-ast-0.2.3.pom
Download https://repo1.maven.org/maven2/org/abego/treelayout/org.abego.treelayout.core/1.0.1/org.abego.treelayout.core-1.0.1.pom
Download https://repo1.maven.org/maven2/com/android/tools/build/gradle/1.5.0/gradle-1.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/build/gradle-core/1.5.0/gradle-core-1.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/build/builder/1.5.0/builder-1.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/lint/lint/24.5.0/lint-24.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/build/transform-api/1.5.0/transform-api-1.5.0.jar
Download https://repo1.maven.org/maven2/com/android/databinding/compilerCommon/1.0-rc5/compilerCommon-1.0-rc5.jar
Download https://repo1.maven.org/maven2/net/sf/proguard/proguard-gradle/5.2.1/proguard-gradle-5.2.1.jar
Download https://repo1.maven.org/maven2/org/jacoco/org.jacoco.core/0.7.4.201502262128/org.jacoco.core-0.7.4.201502262128.jar
Download https://repo1.maven.org/maven2/com/android/tools/build/builder-model/1.5.0/builder-model-1.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/build/builder-test-api/1.5.0/builder-test-api-1.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/sdklib/24.5.0/sdklib-24.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/sdk-common/24.5.0/sdk-common-24.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/common/24.5.0/common-24.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/build/manifest-merger/24.5.0/manifest-merger-24.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/ddms/ddmlib/24.5.0/ddmlib-24.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/jack/jack-api/0.9.0/jack-api-0.9.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/jill/jill-api/0.9.0/jill-api-0.9.0.jar
Download https://repo1.maven.org/maven2/com/squareup/javawriter/2.5.0/javawriter-2.5.0.jar
Download https://repo1.maven.org/maven2/org/bouncycastle/bcpkix-jdk15on/1.48/bcpkix-jdk15on-1.48.jar
Download https://repo1.maven.org/maven2/org/bouncycastle/bcprov-jdk15on/1.48/bcprov-jdk15on-1.48.jar
Download https://repo1.maven.org/maven2/org/ow2/asm/asm/5.0.3/asm-5.0.3.jar
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-tree/5.0.3/asm-tree-5.0.3.jar
Download https://repo1.maven.org/maven2/org/antlr/antlr-runtime/3.5.2/antlr-runtime-3.5.2.jar
Download https://repo1.maven.org/maven2/org/antlr/antlr/3.5.2/antlr-3.5.2.jar
Download https://repo1.maven.org/maven2/com/android/tools/lint/lint-checks/24.5.0/lint-checks-24.5.0.jar
Download https://repo1.maven.org/maven2/org/eclipse/jdt/core/compiler/ecj/4.4.2/ecj-4.4.2.jar
Download https://repo1.maven.org/maven2/com/android/tools/annotations/24.5.0/annotations-24.5.0.jar
Download https://repo1.maven.org/maven2/com/google/guava/guava/17.0/guava-17.0.jar
Download https://repo1.maven.org/maven2/com/android/databinding/baseLibrary/1.0-rc5/baseLibrary-1.0-rc5.jar
Download https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.3.2/commons-lang3-3.3.2.jar
Download https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4/4.5/antlr4-4.5.jar
Download https://repo1.maven.org/maven2/commons-io/commons-io/2.4/commons-io-2.4.jar
Download https://repo1.maven.org/maven2/com/googlecode/juniversalchardet/juniversalchardet/1.0.3/juniversalchardet-1.0.3.jar
Download https://repo1.maven.org/maven2/net/sf/proguard/proguard-base/5.2.1/proguard-base-5.2.1.jar
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-debug-all/5.0.1/asm-debug-all-5.0.1.jar
Download https://repo1.maven.org/maven2/com/android/tools/layoutlib/layoutlib-api/24.5.0/layoutlib-api-24.5.0.jar
Download https://repo1.maven.org/maven2/com/android/tools/dvlib/24.5.0/dvlib-24.5.0.jar
Download https://repo1.maven.org/maven2/com/google/code/gson/gson/2.2.4/gson-2.2.4.jar
Download https://repo1.maven.org/maven2/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.1.1/httpclient-4.1.1.jar
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpmime/4.1/httpmime-4.1.jar
Download https://repo1.maven.org/maven2/net/sf/kxml/kxml2/2.3.0/kxml2-2.3.0.jar
Download https://repo1.maven.org/maven2/org/antlr/ST4/4.0.8/ST4-4.0.8.jar
Download https://repo1.maven.org/maven2/com/android/tools/lint/lint-api/24.5.0/lint-api-24.5.0.jar
Download https://repo1.maven.org/maven2/org/ow2/asm/asm-analysis/5.0.3/asm-analysis-5.0.3.jar
Download https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4-runtime/4.5/antlr4-runtime-4.5.jar
Download https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4-annotations/4.5/antlr4-annotations-4.5.jar
Download https://repo1.maven.org/maven2/com/intellij/annotations/12.0/annotations-12.0.jar
Download https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcore/4.1/httpcore-4.1.jar
Download https://repo1.maven.org/maven2/commons-logging/commons-logging/1.1.1/commons-logging-1.1.1.jar
Download https://repo1.maven.org/maven2/commons-codec/commons-codec/1.4/commons-codec-1.4.jar
Download https://repo1.maven.org/maven2/com/android/tools/external/lombok/lombok-ast/0.2.3/lombok-ast-0.2.3.jar
Download https://repo1.maven.org/maven2/org/abego/treelayout/org.abego.treelayout.core/1.0.1/org.abego.treelayout.core-1.0.1.jar
:preBuild UP-TO-DATE
:preDebugBuild UP-TO-DATE
:checkDebugManifest
:CordovaLib:preBuild UP-TO-DATE
:CordovaLib:preDebugBuild UP-TO-DATE
:CordovaLib:compileDebugNdk UP-TO-DATE
:CordovaLib:compileLint
:CordovaLib:copyDebugLint UP-TO-DATE
:CordovaLib:mergeDebugProguardFiles
:CordovaLib:packageDebugRenderscript UP-TO-DATE
:CordovaLib:checkDebugManifest
:CordovaLib:prepareDebugDependencies
:CordovaLib:compileDebugRenderscript
:CordovaLib:generateDebugResValues
:CordovaLib:generateDebugResources
:CordovaLib:packageDebugResources
:CordovaLib:compileDebugAidl
:CordovaLib:generateDebugBuildConfig
:CordovaLib:generateDebugAssets UP-TO-DATE
:CordovaLib:mergeDebugAssets
:CordovaLib:processDebugManifest
:CordovaLib:processDebugResources
:CordovaLib:generateDebugSources
:CordovaLib:compileDebugJavaWithJavacNote: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

:CordovaLib:processDebugJavaRes UP-TO-DATE
:CordovaLib:transformResourcesWithMergeJavaResForDebug
:CordovaLib:transformClassesAndResourcesWithSyncLibJarsForDebug
:CordovaLib:mergeDebugJniLibFolders
:CordovaLib:transformNative_libsWithMergeJniLibsForDebug
:CordovaLib:transformNative_libsWithSyncJniLibsForDebug
:CordovaLib:bundleDebug
:prepareAndroidCordovaLibUnspecifiedDebugLibrary
:prepareDebugDependencies
:compileDebugAidl
:compileDebugRenderscript
:generateDebugBuildConfig
:generateDebugAssets UP-TO-DATE
:mergeDebugAssets
:generateDebugResValues
:generateDebugResources
:mergeDebugResources
:processDebugManifest
:processDebugResources
:generateDebugSources
:compileDebugJavaWithJavac
:compileDebugNdk UP-TO-DATE
:compileDebugSources
:transformClassesWithDexForDebug
:mergeDebugJniLibFolders
:transformNative_libsWithMergeJniLibsForDebug
:processDebugJavaRes UP-TO-DATE
:transformResourcesWithMergeJavaResForDebug
:validateDebugSigning
:packageDebug
:zipalignDebug
:assembleDebug
:cdvBuildDebug

BUILD SUCCESSFUL

Total time: 11 mins 39.442 secs
Built the following apk(s):
	/tmp/org.xwalk.foo/platforms/android/build/outputs/apk/android-debug.apk
```



## Build a Cordova app with cordova-plugin-crosswalk-webview
Here our local cordova-plugin-crosswalk-webview is at ~/00-workspace/github/crosswalk-project/cordova-plugin-crosswalk-webview/, we'll build the cordova app with the latest beta version of Crosswalk: 20.50.533.5
```
$ cordova create org.xwalk.bar
$ cd org.xwalk.bar
$  cordova plugin add ~/00-workspace/github/crosswalk-project/cordova-plugin-crosswalk-webview/ --variable XWALK_MODE="embedded" --variable XWALK_VERSION="org.xwalk:xwalk_core_library_beta:20.50.533.5"
$ cordova build android
ANDROID_HOME=/home/andersqiu/xwalk/android/android-sdk-linux
JAVA_HOME=/home/andersqiu/xwalk/android/java/jdk1.8.0_74
null
org.xwalk:xwalk_core_library_beta:20.50.533.5
Download https://download.01.org/crosswalk/releases/crosswalk/android/maven2/org/xwalk/xwalk_core_library_beta/20.50.533.5/xwalk_core_library_beta-20.50.533.5.pom
Download https://download.01.org/crosswalk/releases/crosswalk/android/maven2/org/xwalk/xwalk_core_library_beta/20.50.533.5/xwalk_core_library_beta-20.50.533.5.aar
...
```

For cordova-plugin-crosswalk-webview beta branch, it will download the aar files from **download.01.org**, after apks are build, they are located at
```
$ find . -name "*.apk"
./platforms/android/build/outputs/apk/android-x86-debug.apk
./platforms/android/build/outputs/apk/android-x86-debug-unaligned.apk
./platforms/android/build/outputs/apk/android-armv7-debug-unaligned.apk
./platforms/android/build/outputs/apk/android-armv7-debug.apk
```
