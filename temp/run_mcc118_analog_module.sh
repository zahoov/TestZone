#!/bin/sh

CANtype="RBP17"
codeDir="/home/pi/Desktop/PiDAQ/"
outDir="/home/pi/Desktop/out/"
truckname="hydraFL"

mkdir -p $outDir

sudo python3 ${codeDir}mcc118_analog_module_SDsig.py $outDir $CANtype $truckname
#python3 ${codeDir}mcc118_analog_module.py $outDir $CANtype $truckname


