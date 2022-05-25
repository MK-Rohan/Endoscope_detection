#! /bin/bash

input_path="/home/mk/python-docker/static/images"

for img in $input_path;
do
    python /home/mk/python-docker/test_image/yolov5/detect.py --project /home/mk/python-docker/static/out_img --weights /home/mk/python-docker/test_image/output_imgyolov5/runs/train/gun_yolov5s_results5/weights/best.pt --img 416 --conf 0.15 --source $img
done