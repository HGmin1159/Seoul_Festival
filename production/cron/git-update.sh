#!/bin/bash
git -C /home/web pull
git -C /home/web add .
git -C /home/web commit -m"auto update"
git -C /home/web push