#!/bin/bash

# Crosswalk-app-tools for Android
export CROSSWALK_APP_TOOLS_HOME="/home/banana/xwalk/android/crosswalk-app-tools"

# Crosswalk-app-tools for Linux
#export CROSSWALK_APP_TOOLS_HOME="/home/banana/xwalk/linux/crosswalk-app-tools"

# export PATH=$PATH:$CROSSWALK_APP_TOOLS_HOME/src
export CROSSWALK_APP_TOOLS_CACHE_DIR="/home/banana/pkg_tools_zip"

export JAVA_HOME="/home/banana/xwalk/android/java/jdk1.8.0_91"
export JRE_HOME=$JAVA_HOME/jre
export PATH=$PATH:$JAVA_HOME/bin:$JRE_home/bin
export CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar

export ANDROID_HOME="/home/banana/xwalk/android/android-sdk-linux"
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools:$ANDROID_HOME/build-tools/23.0.3
export GRADLE_HOME="/home/banana/xwalk/android/java/gradle-2.4"
export ANT_HOME="/home/banana/xwalk/android/java/apache-ant-1.9.6"
export PATH=$PATH:$GRADLE_HOME/bin:$ANT_HOME/bin

export EDITOR=vim

export NODE_PATH=/usr/local/lib/node_modules
