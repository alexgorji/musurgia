from pathlib import Path
import unittest
from PIL import Image, ImageChops
import cairosvg
import svg

# On mac python does not seem to find libcairo.2.dylib which is created when hombrew installs cairo.
# A work around is to make a symlink to it: ln -s /opt/homebrew/lib/libcairo.2.dylib .


class SVG:
    def __init__(self, data: svg.SVG | str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    def write_to_path(self, path):
        print(path)
        with open(path, "w") as file:
            file.write(self.data if isinstance(self.data, str) else self.data.as_str())
        return path


class SVGTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_test_path(test_file_path: Path, post_fix: str, extension: str) -> Path:
        return test_file_path.parent / f"{test_file_path.stem}_{post_fix}.{extension}"

    def compare_svg_to_png(
        self, svg_path: Path, png_path: Path, width=400, height=400, tolerance=0
    ):
        rendered_png_path = svg_path.with_suffix(".rendered.png")
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(rendered_png_path),
            output_width=width,
            output_height=height,
        )

        img1 = Image.open(rendered_png_path).convert("RGBA")
        img2 = Image.open(png_path).convert("RGBA")

        img1 = img1.resize((width, height))
        img2 = img2.resize((width, height))

        diff = ImageChops.difference(img1, img2)

        if diff.getbbox() is None:
            return True

        if tolerance > 0:
            diff_pixels = sum(
                diff.getchannel(c).point(bool).getdata().count(1) for c in range(4)
            )
            total_pixels = width * height * 4
            if diff_pixels / total_pixels <= tolerance:
                return True

        diff_path = svg_path.with_suffix(".diff.png")
        diff.save(diff_path)
        raise AssertionError(
            f"Rendered SVG differs from golden PNG.\n"
            f"Saved diff image to {diff_path}"
        )
