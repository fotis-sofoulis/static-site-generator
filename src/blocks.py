def markdown_to_blocks(md):
    if not md:
        return []
    blocks = md.strip().split("\n\n")
    return [block.strip() for block in blocks if block.strip()]
