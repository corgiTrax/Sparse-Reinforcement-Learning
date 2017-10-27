#!/bin/bash
for subj in 26 27 28 31 32 33 34 35 36 37 38 39 42 43 44 45 46 47 48 54 56 59 61 63 64
do
    echo "Subj: " $subj
    grep angular ${subj}_*.out > diffs_${subj}.txt
    python calc_avg_angles.py diffs_${subj}.txt    
    echo
done

echo "Total: " 
grep angular *.out > diffs_all.txt
python calc_avg_angles.py diffs_all.txt    
