#!/bin/bash
for f in data/subj$1/*_$2.data;
do
  echo "Plotting $f file..."
  python world.py $f f result/subj$1/task$2
done

