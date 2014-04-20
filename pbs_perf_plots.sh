#!/usr/bin/env bash
#PBS -l mem=8gb,walltime=00:01:00:00
#PBS -l nodes=1:ppn=1
#PBS -q hep
#PBS -o output/out.txt
#PBS -e output/error.txt
#PBS -m ae
#PBS -M luke.deoliveira@yale.edu

cd $PBS_O_WORKDIR 
mkdir -p output
echo 'submitted from: ' $PBS_O_WORKDIR 

export PYTHONPATH+=:~/TopTaggingPerf

python ./processplots.py ./tagger_6_study.yaml