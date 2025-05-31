from utils import clean_copy, generate_pages_recursive
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    clean_copy("static/", "docs/")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


if __name__ == "__main__":
    main()
