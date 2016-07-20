#!/bin/bash
rm ../data/subj$1/*.dis
rm ../data/subj$1/task*
for f in ../data/subj$1/*.data;
do
  echo "Processing $f file..."
  python ../world.py $f b
done
for f in ../data/subj$1/*_1.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj$1/task1
done
for f in ../data/subj$1/*_2.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj$1/task2
done
for f in ../data/subj$1/*_3.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj$1/task3
done
for f in ../data/subj$1/*_4.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj$1/task4
done

