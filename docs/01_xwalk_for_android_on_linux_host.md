# Crosswalk for Android on Linux host environment setup

## Prerequisites:
* Ubuntu Linux 14.04 x86_64

## Notice:
In this guide, we will install all the tools (except for the node) at **~/xwalk/**

```Bash
$ mkdir -pv ~/xwalk
```

## Install necessary packages
```Bash
$ sudo apt-get install build-essential git tree openssh-server
```

All the tools are supposed to stored at **~/Downloads**

## Install JDK
```Bash
$ cd ~/Downloads
$ tar -xvf jdk-8u91-linux-x64.tar.gz
$ mkdir -pv ~/xwalk/jdk
$ mv -fv jdk1.8.0_91/ ~/xwalk/jdk/
```

Add the following environment variables like this:
```Bash
export JAVA_HOME=~/xwalk/jdk/jdk1.8.0_91
export PATH=$PATH:$JAVA_HOME/bin
```

# Install ant
```Bash
$ cd ~/Downloads
$ tar -xvf apache-ant-1.9.6-bin.tar.gz
$ mv -fv apache-ant-1.9.6 ~/
$ vim ~/.bashrc
export ANT_HOME=~/xwalk/apache-ant-1.9.6
export PATH=$PATH:$ANT_HOME/bin
```

## Install Node
```Bash
$ cd ~/Downloads
$ wget https://nodejs.org/dist/v4.4.5/node-v4.4.5.tar.gz
$ tar -xvf node-v4.4.5.tar.gz
$ cd node-v4.4.5/
$ ./configure
$ make -j 8
$ sudo make install
```

Set npm proxy:

```Bash
$ npm config set proxy http://child-prc.intel.com:913
$ npm config set https_proxy http://child-prc.intel.com:913
```

Set NODE_PATH environment variable
```Bash
$ vim ~/.bashrc
export NODE_PATH=/usr/local/lib/node_modules
```


## Install Android SDK for Linux host
Install 2 32-bit compatibility library on 64-bit system:
```Bash
$ sudo apt-get install lib32stdc++6 lib32z1
```

```Bash
$ cd ~/Downloads
$ tar -xvf android-sdk_r24.4.1-linux.tgz
$ mv -fv android-sdk-linux/ ~/xwalk/
```

Now you need to install Android SDK online.
```Bash
$ source ~/.bashrc
$ cd ~/xwalk/android-sdk-linux/tools
$ ./android
```

This will launch the Android SDK manager, check in the following options in tools:
* Android SDK Platform-tools
* Android SDK Build-tools

And other Android API levels, then install them all.

After that, reload the Android SDK manager.

Set the Android SDK releated environment variables, here we installed build-tools with version 23.0.3
```Bash
$ vim ~/.bashrc
export ANDROID_HOME=~/xwalk/android-sdk-linux
export BUILD_TOOLS_VERSIN="23.0.3"
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/build-tools:$ANDROID_HOME/build-tools/$BUILD_TOOLS_VERSION:$ANDROID_HOME/platform-tools
```


## Install Crosswalk-app-tools
```Bash
$ cd ~/xwalk/
$ git clone https://github.com/crosswalk-project/crosswalk-app-tools.git
$ cd crosswalk-app-tools
$ sudo npm install --verbose
```

Set the crosswalk-app-tools related environment variables
```Bash
export CROSSWALK_APP_TOOLS_CACHE_DIR=~/xwalk/xwalk_zip
export CROSSWALK_APP_TOOLS_HOME=~/xwalk/crosswalk-app-tools
export PATH=$PATH:$CROSSWALK_APP_TOOLS_HOME/src
```

## Check if the environment is ready
```Bash
$ crosswalk-app check android
```
