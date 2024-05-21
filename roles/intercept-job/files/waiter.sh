#!/bin/bash
set -eu
INTERCEPT_STOP_FILE=${1:-}
if [ -z "${INTERCEPT_STOP_FILE}" ] ; then
  echo usage: $0 intercept_stop_file
  exit 1
fi
echo "to continue job:"
echo touch ${INTERCEPT_STOP_FILE}
echo
echo "to cancel job:"
echo kill $BASHPID

while ! [ -e "${INTERCEPT_STOP_FILE}" ] ; do
  sleep 5
done
