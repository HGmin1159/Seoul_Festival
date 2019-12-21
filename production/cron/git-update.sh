#!/bin/bash
git -C /home/ubuntu/web pull
git -C /home/ubuntu/web add .
git -C /home/ubuntu/web commit -m"auto update"
git -C /home/ubuntu/web push