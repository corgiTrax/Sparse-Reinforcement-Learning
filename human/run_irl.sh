#!/bin/bash
rm result/subj26/*
#for f in data/subj26/*.data.dis;
#do
#  echo "running sparse irl on $f file..."
#  python sparse-inverseRL.py $f 0
#done  
for f in data/subj26/task*;
do
  echo "running sparse irl on $f file..."
  python3 sparse-inverseRL.py $f 0
done  

