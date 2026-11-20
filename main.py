"""Sum up 19 November's world news in one image — entry program.

Copies the image this repository holds (entry.png, a newspaper front page
drawn by generate_image.py from the six verified stories of Thursday
19 November 2026) to /output/entry.png.

Python 3.13, standard library only. No network, no randomness, no clock:
every run writes exactly the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(HERE, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    main()
