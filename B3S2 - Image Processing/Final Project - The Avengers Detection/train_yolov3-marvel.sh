#!/bin/sh
./darknet detector train ./marvel_cfg/marvel.data ./marvel_cfg/yolov3-marvel.cfg ./darknet53.conv.74 -dont_show
