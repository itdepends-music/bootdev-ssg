def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = (block.strip() for block in blocks)
    blocks = filter(lambda block: block != "", blocks)
    return list(blocks)
