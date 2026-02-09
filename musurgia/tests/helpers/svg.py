import unittest
from pathlib import Path

import cairosvg
import svg
from PIL import Image

from musurgia.graphics.page import Page

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
    def create_test_path(
        test_file_path: Path, post_fix: str, extension: str, directory: str = ""
    ) -> Path:
        if directory:
            return (
                test_file_path.parent
                / directory
                / f"{test_file_path.stem}_{post_fix}.{extension}"
            )
        return test_file_path.parent / f"{test_file_path.stem}_{post_fix}.{extension}"

    def compare_svg_to_png(
        self,
        svg_path: Path,
        png_path: Path,
        width=int(210 * 96 / 25.4),
        height=int(297 * 96 / 25.4),
        tolerance=0.0,
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

        percentage_diff, images_are_same, tolerance = self.compare_images(
            img1, img2, tolerance=tolerance
        )

        if images_are_same:
            return True

        raise AssertionError(
            f"Rendered SVG differs from golden PNG.\n"
            f"""The comparison failed. The actual difference of
            {percentage_diff:05.3f}% exceeds the tolerance of {tolerance:05.3f}%."""
        )

    def compare_images(self, im1: Image.Image, im2: Image.Image, tolerance=0.002):
        """
        https://rowannicholls.github.io/python/image_analysis/comparing_two_images.html

        Compare two images.
        If tolerance is defined the outcome will compared with the accepted
        tolerance. The tolerance is a percentage difference calculated using
        https://rosettacode.org/wiki/Percentage_difference_between_images#Python
        """
        # Remove alpha layer if it exists
        if im1.getbands() == ("R", "G", "B", "A"):
            im1 = im1.convert("RGB")
        if im2.getbands() == ("R", "G", "B", "A"):
            im2 = im2.convert("RGB")
        if im1.getbands() == ("L", "A"):
            im1 = im1.convert("L")
        if im2.getbands() == ("L", "A"):
            im2 = im2.convert("L")

        # Check that the images can be compared
        if im1.mode != im2.mode:
            raise Exception(f"Different kinds of images: {im1.mode} != {im2.mode}")
        if im1.size != im2.size:
            raise Exception(f"Different sizes of images: {im1.size} != {im2.size}")

        # Pixel-by-pixel comparison
        pairs = zip(im1.get_flattened_data(), im2.get_flattened_data())
        # If the image is greyscale
        if len(im1.getbands()) == 1:
            # Total difference
            diff = sum(abs(pixel1 - pixel2) for pixel1, pixel2 in pairs)
        # If the image is RGB
        else:
            # Total difference
            diff = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

        # Total number of colour components
        N = im1.size[0] * im1.size[1] * len(im1.getbands())

        # Calculate the percentage difference
        percentage_diff = diff / 255 / N * 100

        # Assess if the difference falls within the tolerance
        if percentage_diff <= tolerance:
            images_are_same = True
        else:
            images_are_same = False

        return percentage_diff, images_are_same, tolerance

    def compare_page(
        self,
        page: Page,
        post_fix: str,
        this_path: Path,
        width=None,
        height=None,
        tolerance=0.0,
    ):
        svg_path = SVG(page.convert_to_svg_string()).write_to_path(
            self.create_test_path(this_path, post_fix, "svg")
        )

        png_path = self.create_test_path(this_path, post_fix, "png", "golden_pngs")
        width = width or int(page.layout.get_size().width * 96 / 25.4)
        height = height or int(page.layout.get_size().height * 96 / 25.4)

        self.compare_svg_to_png(
            svg_path,
            png_path,
            width,
            height,
            tolerance=tolerance,
        )
