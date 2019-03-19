'''
Module for common functions.
'''

import json
from anytree import Node, RenderTree, AsciiStyle
from ensure import ensure_annotations
from frostmark.db import get_session
from frostmark.models import Folder, Bookmark


@ensure_annotations
def assemble_folder_tree(items: list, key: str, node_type) -> Node:
    '''
    Assemble a folder tree, return a root node.

    Use `key` argument as a one-side parent <- child relationship
    between folder nodes.

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

    Use `key` argument as a one-side parent <- child relationship
    between folder and bookmark node.

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
def fetch_folder_tree() -> Node:
    '''
    Fetch folders only from the internal database, assemble a tree
    and return the root Node.
    '''

    session = get_session()
    folders = [vars(item) for item in session.query(Folder).all()]
    session.close()

    for folder in folders:
        if folder['id'] != 0:
            continue
        folder['parent_folder_id'] = None

    tree = assemble_folder_tree(
        items=folders,
        key='parent_folder_id',
        node_type=Folder
    )
    return tree


@ensure_annotations
def fetch_bookmark_tree() -> Node:
    '''
    Fetch folders and bookmarks from the internal database, assemble
    a bookmark tree and return the root Node
    '''

    session = get_session()
    folders = [vars(item) for item in session.query(Folder).all()]
    bookmarks = [vars(item) for item in session.query(Bookmark).all()]
    session.close()

    for folder in folders:
        if folder['id'] != 0:
            continue
        folder['parent_folder_id'] = None

    tree = assemble_bookmark_tree(
        items=bookmarks,
        key='folder_id',
        folder_tree_root=assemble_folder_tree(
            items=folders,
            key='parent_folder_id',
            node_type=Folder
        ),
        node_type=Bookmark
    )
    return tree


@ensure_annotations
def print_bookmark_tree(root: Node):
    '''
    Print a nested bookmark tree from a root tree `Node`, folders first
    bookmark with urls second.
    '''

    for pre, _, node in RenderTree(root, style=AsciiStyle()):
        if node.node_type == Folder:
            required = ('folder_name', )
            args = [getattr(node, key) for key in required]
            args[0] = f'[F] {node.id}\t{args[0]}'

        elif node.node_type == Bookmark:
            required = ('title', 'url')
            args = [getattr(node, key) for key in required]
            args[0] = f'[B] {node.id}\t{args[0]}'

        print(f'{pre}{" ".join(args)}')


@ensure_annotations
def json_bookmark_tree(root: Node):
    '''
    Assemble a nested bookmark tree from a root tree `Node`, folders first
    bookmark with urls second and put it to JSON.
    '''

    exclude = ['NodeMixin', 'sa_instance_state']
    output = []
    for item in traverse(root):
        obj = {}
        for key, value in vars(item).items():
            if any([exc in key for exc in exclude]):
                continue

            elif key == 'node_type':
                obj[key] = str(value.__name__)

            elif key == 'icon':
                # expects value for img.src i.e. url or
                # data:image/png;base64,encodedstring
                obj[key] = value.decode('utf-8')
            else:
                obj[key] = value
        output.append(obj)

    return json.dumps(output)


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
