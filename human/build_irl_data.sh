#!/bin/bash
rm data/subj26/*.dis
for f in data/subj26/*;
do
  echo "Processing $f file..."
  python world.py $f 
done
for f in data/subj26/*_1.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> data/subj26/task1
done
for f in data/subj26/*_2.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> data/subj26/task2
done
for f in data/subj26/*_3.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> data/subj26/task3
done
for f in data/subj26/*_4.data.dis;
do
  echo "concatenate $f file..."
  cat $f >> data/subj26/task4
done

