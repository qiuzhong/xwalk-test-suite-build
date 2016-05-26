# Crosswalk for Android on Mac OS X host environment setup

## Prerequisites:
* Mac OS X 10.11+

## Notice:
In this guide, we will install all the tools (except for the node) at ~/xwalk/
```Bash
$ mkdir -pv ~/xwalk
```
All the tools are supposed to stored at ~/Downloads

## Install JDK
* Get **jdk-8u91-macosx-x64.dmg** from [Oracle Site](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* Install the dmg file and make sure **javac** and **java** are in the PATH

## Install ant
```Bash
$ cd ~/Downloads
$ tar -xvf apache-ant-1.9.6-bin.tar.gz
$ mv -fv apache-ant-1.9.6 ~/
$ vim ~/.bashrc
export ANT_HOME=~/xwalk/apache-ant-1.9.6
export PATH=$PATH:$ANT_HOME/bin
```

## Install Node
* Get **node-v<X.Y.Z>.pkg** from [NodeJS Site](https://nodejs.org/en/download/)
* Install the pkg file and make sure **node** and **npm** are in the PATH

Set npm proxy:
```Bash
$ npm config set proxy http://child-prc.intel.com:913
$ npm config set https_proxy http://child-prc.intel.com:913
```

Set NODE_PATH environment variable
```Bash
$ vim ~/.bash_profile
export NODE_PATH=/usr/local/lib/node_modules
```

## Install Android SDK for Mac OS X host:
```Bash
$ cd ~/Downloads
$ unzip android-sdk_r24.4.1-macosx.zip
$ mkdir -pv ~/xwalk/android
$ mv -fv android-sdk-macosx/ ~/xwalk/android/
```

Now you need to install Android SDK online.
```Bash
$ source ~/.bash_profile
$ cd ~/xwalk/android/android-sdk-macosx/tools
$ ./android
```

This will launch the Android SDK manager, check in the following options in tools:

* Android SDK Platform-tools
* Android SDK Build-tools
* And other Android API levels, then install them all.

After that, reload the Android SDK manager.

Set the Android SDK releated environment variables
```Bash
$ vim ~/.bashrc
export ANDROID_HOME=~/xwalk/android-sdk-linux
export BUILD_TOOLS_VERSIN="23.0.3"
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/build-tools:$ANDROID_HOME/build-tools/$BUILD_TOOLS_VERSION:$ANDROID_HOME/platform-tools
```

## Install Crosswalk-app-tools
```Bash
$ cd ~/xwalk/android/
$ git clone https://github.com/crosswalk-project/crosswalk-app-tools.git
$ cd crosswalk-app-tools
$ sudo npm install --verbose
```

Set the crosswalk-app-tools related environment variables
```Bash
$ vim ~/.bash_profile
export CROSSWALK_APP_TOOLS_CACHE_DIR=~/xwalk/android/xwalk_zip
export CROSSWALK_APP_TOOLS_HOME=~/xwalk/android/crosswalk-app-tools
export PATH=$PATH:$CROSSWALK_APP_TOOLS_HOME/src
```

## Check if the environment is ready
```Bash
$ crosswalk-app check android
```
