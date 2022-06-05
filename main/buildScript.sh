#!/bin/bash

path=$1
option=$2

if [ ${option} = 1 ]; then
  cd ${path};
  echo ${path};
  sudo chmod -R 777 .;
  . build/envsetup.sh;
  lunch sdk_phone_x86_64-userdebug;
  m;
fi

emulator;