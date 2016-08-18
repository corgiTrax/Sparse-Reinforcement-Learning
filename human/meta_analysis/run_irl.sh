#!/bin/bash
#rm result/subj26/*
#for f in data/subj26/*.data.dis;
#do
#  echo "running sparse irl on $f file..."
#  python sparse-inverseRL.py $f 0
#done  
rm -rf ../result/subj$1
mkdir ../result/subj$1
for f in ../data/subj$1/task*;
do
  echo "running sparse irl on $f file..."
  python ../sparse-inverseRL.py $f 0
done  

