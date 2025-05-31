from utils import clean_copy, generate_pages_recursive


def main():
    clean_copy("static/", "public/")
    generate_pages_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
    main()
