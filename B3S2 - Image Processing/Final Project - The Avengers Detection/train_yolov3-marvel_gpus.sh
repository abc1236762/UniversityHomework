#!/bin/sh
./darknet detector train ./marvel_cfg/marvel.data ./marvel_cfg/yolov3-marvel.cfg ./marvel_weights/yolov3-marvel_last.weights -gpus 0,1,2,3 -dont_show
