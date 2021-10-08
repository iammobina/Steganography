import random
import shutil
import cv2
import numpy as np
import os
from subprocess import call, STDOUT

global count


def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder = "./tmp"

    vidcap = cv2.VideoCapture(video)
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1


def encode_image(root="./tmp/"):
    img2 = cv2.imread("theme.png")
    # img 1 how img 2 umbrela

    for k in range(0, len(img2)):
        f_name = "{}{}.png".format(root, k)
        img1 = cv2.imread(f_name)
        for i in range(img2.shape[0]):
            for j in range(img2.shape[1]):
                for l in range(3):
                    v1 = format(img1[i][j][l], '08b')
                    v2 = format(img2[i][j][l], '08b')
                    v3 = v1[:4] + v2[:4]

                    img1[i][j][l] = int(v3, 2)
        cv2.imwrite(f_name, img1)
        print("frame img1 {} img2{}".format(img1, img2[i], k))


def decode_image(video):
    frame_extraction(video)
    root = "./tmp/"
    sample = cv2.imread("./tmp/0.png")
    width = sample.shape[0]
    height = sample.shape[1]
    logowidth = sample.shape[0]
    logoheight = sample.shape[1]
    image_decode = np.zeros((width, height, 3), np.uint8)
    logo_decode = np.zeros((logowidth, logoheight, 3), np.uint8)
    for k in range(len(logo_decode)):
        f_name = "{}{}.png".format(root, k)
        img = cv2.imread(f_name)
        for i in range(width):
            for j in range(height):
                for l in range(3):
                    v1 = format(img[i][j][l], '08b')
                    if v1 is None:
                        break
                    v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                    v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4
                    image_decode[i][j][l] = int(v2, 2)
                    logo_decode[i][j][l] = int(v3, 2)

        cv2.imwrite('last_image_decode.png', image_decode)
        cv2.imwrite('theme_image_decode.png', logo_decode)
        print("frame img {} decrypt {}, k {}".format(img, image_decode[i], k))
        clean_tmp()


def clean_tmp(path="./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("tmp files are deleted")


def main():
    f_name = input("Enter the name of video with its format")
    frame_extraction(f_name)
    call(["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"], stdout=open(os.devnull, "w"),
         stderr=STDOUT)

    encode_image()
    call(["ffmpeg", "-i", "tmp/%d.png", "-vcodec", "png", "tmp/video.mp4", "-y"], stdout=open(os.devnull, "w"),
         stderr=STDOUT)

    call(["ffmpeg", "-i", "tmp/video.mp4", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],
         stdout=open(os.devnull, "w"), stderr=STDOUT)
    clean_tmp()


if __name__ == "__main__":
    while True:
        print("1.Hide a message in video 2.Reveal the secret from video")
        print("press any key to exit")
        choice = input()
        if choice == '1':
            main()
        elif choice == '2':
            decode_image(input("Enter name of video with its format"))
        else:
            break
