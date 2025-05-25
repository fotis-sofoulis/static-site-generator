from textnode import TextType, TextNode


def main():
    textnode = TextNode("This is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(textnode)


if __name__ == "__main__":
    main()
