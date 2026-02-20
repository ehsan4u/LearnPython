#!/bin/bash

echo "Starting simulations..."

python filteration_simulation.py &
PID1=$!

python environmental_simulation.py &
PID2=$!

echo "Simulations running..."
echo "PID1: $PID1"
echo "PID2: $PID2"
