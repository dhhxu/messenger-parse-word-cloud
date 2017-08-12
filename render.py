"""
Render simple word cloud images from text.
"""

import argparse
import json
import os
import re

import matplotlib.pyplot as plt
from wordcloud import WordCloud

stopwords_path = "stopwords/en.json"

with open(stopwords_path) as f:
    stopwords = json.load(f)
    stopwords_pattern = r"\b({})\b".format("|".join(stopwords))


def clean_text(text):
    """Remove stopwords from text and convert to lowercase."""
    stopwords_regex = re.compile(stopwords_pattern, re.UNICODE)
    cleaned = text.lower()
    cleaned = re.sub(r"https?:\/\/.*[\r\n]*", "", cleaned)
    cleaned = stopwords_regex.sub("", cleaned)
    return cleaned


def render(path, out_path, font_size, show):
    """
    Render word cloud PNG image generated from input text.

    Args:
        path (str): Path to text file to be used to generate word cloud
        out_path (str): Path to save word cloud image
        font_size (int): Maximum font size in word cloud
        show (bool): If True, display word cloud only. Otherwise, do not display
                     and instead save to file.
    """
    with open(path, "r") as f:
        text = clean_text(f.read())
        wordcloud = WordCloud(max_font_size=font_size).generate(text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        if show:
            plt.show()
        else:
            plt.savefig(out_path)   


def main():
    parser = argparse.ArgumentParser(description="Generate word cloud image from text")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="Path to text file")
    parser.add_argument("-o", "--output", type=str, default="renders",
                        help="Path to output directory (default: renders/")
    parser.add_argument("-s", dest="font_size", default=40, type=int,
                        help="Max font size (default: 40)")
    parser.add_argument("--show", action="store_true",
                        help="Display word cloud image only")
    args = parser.parse_args()

    basename = args.input.split("/")[-1].split(".")[0]
    out_path = os.path.join(args.output, "{}.png".format(basename))
    render(args.input, out_path, args.font_size, args.show)


if __name__ == "__main__":
    main()
