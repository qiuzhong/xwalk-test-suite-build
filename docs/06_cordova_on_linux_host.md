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

```
