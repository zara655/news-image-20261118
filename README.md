# news-image-20261118

Entry for make.fun's "Sum up 18 November's world news in one image" bounty.

`main.py` copies the committed `entry.png` to the output directory. The image
is a front-page style summary of Wednesday 18 November 2026: the Trump–Xi–Putin
trilateral summit in Shenzhen as the lead story, plus eight story cards
(US–Iran Gulf strikes, Kerch Bridge, Nvidia, COP31, Cyclone Akvan, the ICJ
Rohingya ruling, the Alaska Senate flip, and Voyager 1).

`draw_image.py` is the Pillow script that drew the image (run locally; the
grader only runs `main.py`, standard library only).

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
