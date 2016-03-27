#!/bin/bash

killall mjpg_streamer
mjpg_streamer -i "/usr/local/lib/input_uvc.so -d /dev/video0" -o "/usr/local/lib/output_http.so -p 8080 -w /var/www -c yogi:bear" &
