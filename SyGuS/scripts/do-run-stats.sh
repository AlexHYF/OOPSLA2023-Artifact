#!/usr/bin/env bash

tsp -C
echo Processes currently in queue: $( tsp | wc -l )
echo

echo Processes dequeued: $( find impls -name 'run.log' | wc -l )
echo Processes successfully finished: $( find impls -name 'run.log' | xargs grep 'Exit status' | grep ': 0$' | wc -l )
echo Processes timed out: $( find impls -name 'run.log' | xargs grep 'Exit status' | grep ': 124$' | wc -l )
echo Processes with errors: $( find impls -name 'run.log' | xargs grep 'Exit status' | grep ': 1$' | wc -l )
echo

echo Holes processed: $( find impls -name 'run.log' | xargs grep 'Hole Summary' | wc -l )
echo Unconstrained holes: $( find impls -name 'run.log' | xargs grep 'Unconstrained hole!' | wc -l )
echo Inconsistent holes: $( find impls -name 'run.log' | xargs grep 'Inconsistent subspec!' | wc -l )
