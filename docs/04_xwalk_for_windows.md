# Crosswalk for Windows environment setup
## Prerequisites:
* Windows 8+

### Notice:
In this guide, we will install all the tools (except for the node) at
**C:\xwalk**

## Install NodeJS
* Get nodejs executable from [NodeJS Website](https://nodejs.org/en/download/)
* Install NodeJS for Windows, make sure add NodeJS in the PATH when installing. (**C:\Program Files\

## Install WiX Toolset
* Download WiX Toolset from: http://wixtooset.org
* Install WiX Toolset
* Add the WiX Toolset in your PATH environment variable, append **C:\Program Files (x86)\Wix Toolset v3.10\bin** to PATH

## Install Github for Windows(Supported only for Windows 8+)
This step is optional, but I recommend you to install it as this utility provides
more powerful shell environment for you.

## Install Crosswalk-app-tools
Install crosswalk-app-tools for Windows to build MSI
Launch Github Shell
```
C:
cd xwalk
C:\xwalk>git clone https://github.com/crosswalk-project/crosswalk-app-tools.git
C:\xwalk>cd crosswalk-app-tools
C:\xwalk\crosswalk-app-tools>npm install --verbose
```

Add **C:\xwalk\crosswalk-app-tools\src** to PATH.

## Check environment is ready:
```
crosswalk-app --help
candle --version
```
