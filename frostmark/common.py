import json
from pprint import pprint
from anytree import Node, RenderTree, Walker
from frostmark.db import BASE
from frostmark.models import Folder, Bookmark
from ensure import ensure_annotations


@ensure_annotations
def assemble_folder_tree(items: list, key: str, node_type) -> Node:
    '''
    Assemble a folder tree, return a root node.

    Using the behavior that the parent node keeps a hard reference
    to the children therefore removing a local ref won't cripple
    the tree and returning just the root node is fine.
    '''
    nodes = []
    parents = {}
    root_node = None

    for item in items:
        assert 'parent' not in item, item
        node = Node(
            name=item['id'],
            node_type=node_type,
            **{k: v for k, v in item.items()}
        )
        nodes.append(node)
        parents[item['id']] = node

    for node in nodes:
        if node.parent_folder_id is None:
            root_node = node
            continue
        node.parent = parents[getattr(node, key)]

    return root_node


@ensure_annotations
def assemble_bookmark_tree(
        items: list, key: str, folder_tree_root: Node, node_type
) -> Node:
    '''
    Assemble a folder tree, return a root node.

    Using the behavior that the parent node keeps a hard reference
    to the children therefore removing a local ref won't cripple
    the tree and returning just the root node is fine.
    '''
    nodes = []
    folders = {}

    def walk_tree(node):
        folders[node.id] = node

        if not node.children:
            return

        for child in node.children:
            walk_tree(child)

    walk_tree(folder_tree_root)

    for item in items:
        assert 'parent' not in item, item
        node = Node(
            name=item['id'],
            node_type=node_type,
            **{k: v for k, v in item.items()}
        )
        nodes.append(node)

    for node in nodes:
        node.parent = folders[getattr(node, key)]

    return folder_tree_root


@ensure_annotations
def print_bookmark_tree(root: Node):
    for pre, fill, node in RenderTree(root):
        if node.node_type == Folder:
            required = ('folder_name', )
            args = [getattr(node, key) for key in required]
            args[0] = '[F] ' + args[0]

        elif node.node_type == Bookmark:
            required = ('title', 'url')
            args = [getattr(node, key) for key in required]
            args[0] = '[B] ' + args[0]

        print(f'{pre}{" ".join(args)}')


@ensure_annotations
def traverse(root: Node) -> list:
    '''
    Traverse an anytree tree recursively from the root node down to the last
    child and return a flat list of tree nodes.
    '''

    nodes = []
    nodes.append(root)
    for child in root.children:
        nodes += traverse(child)
    return nodes
