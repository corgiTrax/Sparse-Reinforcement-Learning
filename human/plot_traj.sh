#!/bin/bash
rm -rf data/subj$1/plots
mkdir data/subj$1/plots
for f in data/subj$1/*_$2.data;
do
  echo "Plotting $f file..."
  python world.py $f f result/subj$1/task$2
done
mv data/subj$1/*.png data/subj$1/plots/

