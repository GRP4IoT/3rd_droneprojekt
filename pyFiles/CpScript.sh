#!bin/bash

z=1
x=/home/g4py/code/billeder/pic_2022-11-15-13:27:10.png


for i in {1..1000];

do
    cp $x /home/g4py/code/billeder/${z}.png
    let z=z+1
    sleep 0.3
done
