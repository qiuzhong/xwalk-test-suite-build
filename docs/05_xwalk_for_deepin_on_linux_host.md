# Crosswalk for Deepin on Linux host environment setup
## Prerequisites:
* Ubuntu Linux 14.04 x86_64

## Notice:
In this guide, we will install all the tools (except for the node) at **~/xwalk/**

```Bash
$ mkdir -pv ~/xwalk
```

## Assume
All the tools are supposed to stored at **~/Downloads**


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

## Install crosswalk-app-tools for Linux
```Bash
$ cd ~/xwalk/
$ git clone https://github.com/crosswalk-project/crosswalk-app-tools.git
$ cd crosswalk-app-tools
$ sudo npm install --verbose
$ cd node_modules
$ git clone https://github.com/crosswalk-project/crosswalk-app-tools-deb.git crosswalk-app-tools-backend-deb
$ cd crosswalk-app-tools-backend-deb
$ sudo npm install --verbose
```

## Error fixes
If you encounter this error:
> debuild: not found

You can fix it by:

```Bash
$ sudo apt-get install devscripts
```

When you encounter this error:
> debuild: fatal error at line 1364:
> dpkg-buildpackage -rfakeroot -D -us -uc failed

You can fix it by:

```Bash
$ sudo apt-get install debhelper
```
