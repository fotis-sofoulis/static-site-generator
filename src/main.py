from utils import clean_copy, generate_page


def main():
    clean_copy("static/", "public/")
    generate_page("src/content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
