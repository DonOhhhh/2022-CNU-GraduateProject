#!/bin/bash

path=$1
cd $path;
sudo chmod -R 777 .;
make clobber;
. build/envsetup.sh;
lunch sdk_phone_x86_64;
m -j16;
emulator;