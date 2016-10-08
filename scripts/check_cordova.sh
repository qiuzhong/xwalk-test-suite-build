#!/bin/bash


MODES="
embedded
shared
"

ARCHES="
arm
arm64
"

check_cordova_apps() {

    VERSION=$1

    for mode in ${MODES}; do
        for arch in ${ARCHES}; do
            ./complete_cordova_apps.py -v ${VERSION} -m ${mode} -a ${arch} -q
        done
    done
}

check_cordova_tc() {

    VERSION=$1

    for mode in ${MODES}; do
        for arch in ${ARCHES}; do
            ./complete_cordova_tc.py -v ${VERSION} -m ${mode} -a ${arch} -q
        done
    done
}

check_cordova_apps $1
check_cordova_tc $1
