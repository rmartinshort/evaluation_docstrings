from llama_index.core.schema import TextNode


def get_metadata_node(metadata_to_add):
    text = "Here we describe the metadata for this document, which can be used to answer questions about the document's topics, title, authers or history"
    for k, v in metadata_to_add.items():
        text += "\n" + k + ": " + str(v)

    node_metadata = metadata_to_add.copy()
    node_metadata["page_label"] = "undefined"
    node = TextNode(text=text)
    node.metadata = node_metadata
    return node
