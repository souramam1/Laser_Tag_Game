#!/bin/bash
echo "Starting application..."
nohup python3 ./blueberry_pi.py > ../game_logs/game_process.log 2>&1&
echo $! > ../game_logs/game.pid
echo "Application Running"