#!/bin/bash
echo "Stopping Application..."
kill -9 `cat ../game_logs/game.pid`
echo "Process Killed."