#!/bin/bash
rm ../data/subj28/*.dis
rm ../data/subj28/task*
for f in ../data/subj28/*.data;
do
  echo "Processing $f file..."
  python ../world.py $f b
done
for f in ../data/subj28/*_1.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj28/task1
done
for f in ../data/subj28/*_2.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj28/task2
done
for f in ../data/subj28/*_3.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj28/task3
done
for f in ../data/subj28/*_4.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> ../data/subj28/task4
done

