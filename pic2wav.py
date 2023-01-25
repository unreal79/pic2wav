import sys
import time
import getopt
import array
import math
import wave

from PIL import Image
from PIL import ImageOps

import ProgressBar


def main(picture_file, wav_file, duration, resolution, invert_image, equalize_image):
    img = Image.open(picture_file)

    print(f"Preparing picture '{picture_file}'...")
    sample_rate = 44100
    channels = 1
    sample_size = 2
    img_max_sampling = 32767

    num_samples = int(sample_rate * duration)
    tmp_buff = [0.0] * num_samples
    data = array.array('h')

    l_image: Image = img.convert('L').resize((num_samples, resolution))
    img.close()
    if equalize_image:
        l_image = ImageOps.equalize(l_image)
    if invert_image:
        l_image = ImageOps.invert(l_image)
    width, height = l_image.size
    px = l_image.load()
    a_const = 100 / 765
    b_const = 22000 * math.pi * 2 / height / sample_rate
    c_const = height + 1

    print("Processing picture...")
    start_time = time.time()

    for x in range(num_samples):
        rez = 0.0
        d_const = b_const * x

        for y in range(height):
            rez += px[x, y] * a_const * math.sin(d_const * (c_const - y))

        tmp_buff[x] = rez

        if x % 1024 == 0:
            ProgressBar.PrintProgressBar(x, num_samples, length=50,
                                         suffix="(" + str(int(time.time() - start_time)) + " secs)")

    ProgressBar.PrintProgressBar(x + 1, num_samples, length=50,
                                 suffix="(" + str(int(time.time() - start_time)) + " secs)")

    max_freq = max(max(tmp_buff), abs(min(tmp_buff)))

    for i in range(len(tmp_buff)):
        data.append(int(img_max_sampling * tmp_buff[i] / max_freq))

    with wave.open(wav_file, 'w') as f:
        f.setparams((channels, sample_size, sample_rate, num_samples, "NONE", "Uncompressed"))
        f.writeframes(data.tobytes())
    print(f"File '{wav_file}' saved")


if __name__ == '__main__':
    picture_file = 'picture.png'
    wav_file = picture_file + '.wav'
    duration = 2
    resolution = 0
    invert_image = False
    equalize_image = False
    help = "  Convert picture to spectrogrammed sound-file (WAV).\n  Run command:\n    python " + sys.argv[0]\
        + " [[-p] <picture>] [-w <output.wav>] [-d <seconds>] [-r <resolution>] [-e] [-i]\n\
        Options:\n\
        -p - input picture file name (PNG, JPEG, etc.) (default is 'picture.png')\n\
        -w - output WAV file name (default is 'input picture file' + '.wav')\n\
        -d - output sound file duration in seconds (float) (default is 2)\n\
        -r - spectrogram resolution (height) in pixels; affects work time (default is 256)\n\
        -e - equalize image (enhances contrast)\n\
        -i - invert image colors"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:w:d:r:ei")
    except getopt.GetoptError:
        print(help)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt == "-p":
            picture_file = arg
            wav_file = picture_file + '.wav'
        elif opt == "-w":
            wav_file = arg
        elif opt == "-d":
            duration = float(arg)
        elif opt == "-r":
            resolution = int(float(arg))
        elif opt == "-e":
            equalize_image = True
        elif opt == "-i":
            invert_image = True
    if resolution == 0:
        resolution = 256
    if len(opts) == 0 and len(sys.argv) > 1:
        if len(sys.argv) == 2:
            picture_file = sys.argv[1]
        else:
            print(help)
            sys.exit(2)

    print(f"Using Python {sys.version}.")
    start_time = time.time()
    main(picture_file, wav_file, duration, resolution, invert_image, equalize_image)
    print(f"Done in {time.time() - start_time} secs\n")
