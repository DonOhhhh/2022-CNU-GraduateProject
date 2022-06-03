#!/bin/bash

path=$1
option=$2

cd ${path};

if [ ${option} = 1 ]; then
  sudo chmod -R 777 .;
  make clobber;
  . build/envsetup.sh;
  lunch sdk_phone_x86_64;
  m -j16;
fi

emulator;