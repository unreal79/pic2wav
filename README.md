# pic2wav - Spectrogram from picture
Encode an image to sound (WAV file) and view it as a spectrogram in audio player.

# Example
`python3 pic2wav.py picture.png -d8 -r200`

Source picture:

<img src="picture.png" alt="drawing" width="300"/>

Spectrogram of created WAV file:

<img src="picture.png.wav.spectrogram.png" alt="drawing" width="300"/>

## Options
    pic2wav.py [[-p] <picture>] [-w <output.wav>] [-d <seconds>] [-r <resolution>] [-e] [-i]
    Options:
      -p - input picture file name (PNG, JPEG, etc.) (default is 'picture.png')
      -w - output WAV file name (default is 'input picture file' + '.wav')
      -d - output sound file duration in seconds (float) (default is 2)
      -r - spectrogram resolution (height) in pixels; affects work time (default is 256)
      -e - equalize image (enhances contrast)
      -i - invert image colors

## Optimisation
The code is optimized for pefromance in Python 3 with _math_ and _Pillow_ (PIL) libraries.

I recommend running it under [PyPy](https://www.pypy.org/) -- this gives about 30% speedup.

## Thanks
* Based on [alexadam's img-encode](https://github.com/alexadam/img-encode/tree/master/v1-python) (MIT license)
