#!/bin/bash
if [[ "$EUID" != 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

SCRIPT_PATH="$( cd "$( dirname "$0" )" && pwd)"
PROJECT_PATH="$( cd "$SCRIPT_PATH/.." && pwd )"
TARGET_DIRECTORY="/opt/indi-lite-tools"

PYTHON_VERSION=2
ASSUME_YES=false

usage() {
    echo "Usage: $0 options"
    echo "Options:"
    echo "-y|--yes                    Assume yes to all questions"
    echo "-3|--python3                Use python3 instead of python2"
    echo "-d|--distribution <distro>  Distribution type to setup (currently supported: ubuntu, raspbian"
    echo "-u|--user <user>            User for services like indiwebmanager, indi-dashboard, etc"
    exit 1
}

while [[ -n "$1" ]]; do

    case "$1" in
        --yes|-y)
            ASSUME_YES=true
            ;;
        --python3|-3)
            PYTHON_VERSION=3
            ;;
        -d|--distribution)
            distribution="$2"; shift
            ;;
        -u|--user)
            indi_user="$2"; shift
            ;;
        *)
            usage
            ;;
    esac
    shift
done


if [ -r "$SCRIPT_PATH/libs/$distribution.sh" ]; then
    . "$SCRIPT_PATH/libs/$distribution.sh"
else
    usage
fi

if [ -z "$indi_user" ] || [ "$indi_user" == "root" ] || ! grep -q "$indi_user" /etc/passwd; then
    usage
fi


python_pkgname=python
[[ "$PYTHON_VERSION" == 3 ]] && python_pkgname=python3

. "$SCRIPT_PATH/libs/commons.sh"

copy_files

install_distro_steps

