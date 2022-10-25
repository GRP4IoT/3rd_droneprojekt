#!/bin/bash
#datetime=$(date '_%d_%m_%Y_%H_%M_%S');
i=1
for x in range {1..3};

do
raspistill -o picture$i-$(date +"%d-%m-%Y-%H-%M-%S").png
let i=i+1
sleep 2
done
exit 1
