# Copyright (c) 2017-2020, NVIDIA CORPORATION.  All rights reserved.

"""Script to generate val dataset for Faster R-CNN tutorial.
   Modified by Simon & Gilles
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os


def parse_args(args=None):
    """parse the arguments."""
    parser = argparse.ArgumentParser(description='Generate test dataset for Faster-RCNN')

    parser.add_argument(
        "--input_image_dir",
        type=str,
        required=True,
        help="Input directory to KITTI training dataset images."
    )

    parser.add_argument(
        "--input_label_dir",
        type=str,
        required=True,
        help="Input directory to KITTI training dataset labels."
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Ouput directory to TLT test dataset."
    )

    parser.add_argument(
        "--test_split",
        type=int,
        required=False,
        default=10,
        help="Percentage of training dataset for generating test dataset"
    )

    return parser.parse_args(args)


def main(args=None):
    """Main function for data preparation."""

    args = parse_args(args)

    img_files = []
    for file_name in os.listdir(args.input_image_dir):
        if file_name.split(".")[-1] == "jpg":
            img_files.append(file_name)

    total_cnt = len(img_files)
    test_ratio = float(args.test_split) / 100.0
    test_cnt = int(total_cnt * test_ratio)
    train_cnt = total_cnt - test_cnt
    test_img_list = img_files[0:test_cnt]

    target_img_path = os.path.join(args.output_dir, "images")
    target_label_path = os.path.join(args.output_dir, "labels")

    if not os.path.exists(target_img_path):
        os.makedirs(target_img_path)
    else:
        print("This script will not run as output image path already exists.")
        return

    if not os.path.exists(target_label_path):
        os.makedirs(target_label_path)
    else:
        print("This script will not run as output label path already exists.")
        return

    print("Total {} samples in KITTI training dataset".format(total_cnt))
    print("{} for train and {} for test".format(train_cnt, test_cnt))

    for img_name in test_img_list:
        label_name = img_name.split(".")[0] + ".txt"
        os.rename(os.path.join(args.input_image_dir, img_name),
                  os.path.join(target_img_path, img_name))
        os.rename(os.path.join(args.input_label_dir, label_name),
                  os.path.join(target_label_path, label_name))


if __name__ == "__main__":
    main()
