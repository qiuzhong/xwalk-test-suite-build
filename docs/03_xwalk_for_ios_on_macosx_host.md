# Crosswalk for iOS environment setup
This document aims to give the readers an complete guide to setup the Crosswalk for iOS environment. After reading and following the steps in this document, any readers should be able to create/build an Crosswalk application for iOS platform.

## Prerequisites
* Mac OS X EI Captain, Version 10.11.4
* Xcode 7.3

## Install necessary packages
You need to install some necessary packages first.

## Install NodeJS
Please install NodeJS that can comply the ECMAScript 6 standard, which introduces the **Promise** builtin type. As some ES6 features are used in **crosswalk-app-tools**, we suggest to install the latest stable NodeJS.

If your NodeJS version is too low, you may encounter the following error when creating an iOS project via crosswalk-app-tools:

> Promise not defined

This is because crosswalk-app-tools will use Promise while Promise had not been introduced in that NodeJS runtime environment.


### Install Git
Git should be installed with Xcode.

### Install Ruby & Gem
Ruby and Gem should be pre-installed with the Mac OS X system.

### Install CocoaPods
It's for installing the dependency modules when creating an iOS project via the crosswalk-app-tools.

```sh
$ sudo gem install cocoapods
```

You may encounter the following error:

> ERROR: While executing gem ... (Errno::EPERM)
>
> Operation not permitted - /usr/bin/pod

In that case, you can fix it via the command:

```sh
$ sudo gem install -n /usr/local/bin cocoapods
```

### Install crosswalk-app-tools
Suggest to install it locally, first clone it from [github](https://github.com/crosswalk-project/crosswalk-app-tools):

```sh
$ mkdir -pv ~/xwalk/ios
$ cd ~/xwalk/ios
$ git clone https://github.com/crosswalk-project/crosswalk-app-tools.git
$ cd crosswalk-app-tools
$ npm install --verbose
```

For iOS platform, you need to config the iOS backend of crosswalk-app-tools:

```sh
$ cd crosswalk-app-tools/node_modules
$ git clone https://github.com/crosswalk-project/crosswalk-app-tools-ios.git crosswalk-app-tools-backend-ios
$ cd crosswalk-app-tools-backend-ios
$ npm install --verbose
```

## Build and install iOS applications via Xcode
To ensure the certificate is available for the environments, we need to make sure we can build and install an iOS application via Xcode

1. Configure the certificates:

  * iPhone developer certificate
  * iPhone distribution certificate
  * Apple Worldwide Developer Relations Certification Authority(You can download it from Apple developer website)

  Install these 3 certificates to Keychain(From **Utility -> Keychain access**).

  * If WWDRCA certificate is expired, remove it.(To see if an certificate is expired, open Keychain, in left panel, choose **System** in **Keychain**, then choose  **Certificates** in **Category**, in menu **View -> Show Expired Certificates**)

2. New a simple swift-based iOS project.
3. Connect your iOS device to MacBook Pro retina, choose device for build type, In **Build Settings** tap, choose

  > Embedded Content Contains Swift Code

  Set it to **Yes**

4. In menu **Product->Run**, it will build the iOS project for device and install it on the device.

  If the iOS application crashes with the following errors:
  > dyld: Library not loaded: @rpath/libswiftCore.dylib

  > Referenced from: /private/var/mobile/Containers/Bundle/Application/LONGSERIALNUMBER/AppName.app/AppName
  > Reason: no suitable image found.  

  > Did find:
      /private/var/mobile/Containers/Bundle/Application/LONGSERIALNUMBER/AppName.app/Frameworks/libswiftCore.dylib: mmap() error 1 at address=0x008A1000, size=0x001A4000 segment=\__TEXT in Segment::map() mapping /private/var/mobile/Containers/Bundle/Application/LONGSERIALNUMBER/APPLICATION_NAME/Frameworks/libswiftCore.dylib

  The issue is very common for developers, and there're a lot of solutions on **StackOverflow**, but that may not be suitable for you. The most likely reason is about the certificates. See the reference:

  [Technical Q&A QA1886
  Swift app crashes when trying to reference Swift library libswiftCore.dylib.](https://developer.apple.com/library/ios/qa/qa1886/_index.html)

  > To correct this problem, you will need to sign your app using code signing certificates with the Subject Organizational Unit (OU) set to your Team ID. All Enterprise and standard iOS developer certificates that are created after iOS 8 was released have the new Team ID field in the proper place to allow Swift language apps to run.

  If you tried all the solutions on **StackOverflow** but still can't fix this issue, you may need to try to change the **Trust Level** of the iOS developer.

  In **Kaychain**, choose **Login**, then **Certificates**, double-click the iOS developer certificate item, click **Trust**, for **When using this certificate:**, select **Use System Defaults**

  In Xcode **Build Settings** tab **Code Signing** section, you need to choose proper certificates and profile for code signing.

  * Code Signing Identity: iPhone Developer certificate
  * Debug: iPhone Developer certificate
  * Release: iPhone Developer certificate
  * Provisioning Profile: iOS Team Provisioning Profile: *

  Then you can rebuild the application for device, you should have good luck.

## Build and export iap files via crosswalk-app-tools
If you can build and install an iOS project via Xcode, it means basically your your have no certificate issue for iOS platform.
It's ready to use crosswalk-app-tools to create and build ipa files.

* Make sure pod works:
  ```sh
  $ which pod
  /usr/local/bin/pod
  ```

* Make sure your network is available as pod will install some packages from github when creating an iOS project.

If everything is fine, you can create an iOS project:

```sh
$ <path/to/crosswalk-app> create org.xwwalk.bar --platforms=ios
  + Copying app template from ...hub/qiuzhong/crosswalk-app-tools/app-template
  + Loading 'ios' platform backend
  + Clone project [done] Cloned.
  + CocoaPods install [done] Installed.
```

This may take a few minutes, as it will first clone some repos from github, then calling pod to install some dependency packages for the Crosswalk iOS project.

If your Crosswalk iOS project created successfully, you can build it:

```sh
$ cd org.xwalk.bar
$ <path/to/crosswalk-app> build
  + Loading 'ios' platform backend
  + Update web resources.
  + Generate manifest.plist file.
  + Build application [done] Built.
  + Sign and export package [done] Exported.
```

When build successfully, you will see a new bar.ipa in the root directory of org.xwalk.bar, you can install it on your iOS device via iTunes.

That's it!
