import argparse
import numpy as np
import os
from PIL import Image, ImageStat


def getMean_Std(root_path: str,
                image_format: tuple = ('.png', '.jpg', '.jpeg', '.JPG', '.PNG')):
    sum_mean, sum_std, sum_files = np.zeros(3), np.zeros(3), np.zeros(3)
    for root, dirs, files in os.walk(root_path):
        if not dirs:
            for file in files:
                if os.path.splitext(file)[-1] in image_format:
                    img = Image.open(os.path.join(root, file))
                    stat = ImageStat.Stat(img)
                    sum_mean += np.array(stat.mean) / 255
                    sum_std += np.array(stat.stddev) / 255
                    sum_files += 1

    return sum_mean / sum_files, sum_std / sum_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Options for calculation.')
    parser.add_argument('-rp', '--root_path', type=str, default='./data')
    args = parser.parse_args()
    print(args)
    print(getMean_Std(args.root_path))
