'''
Export bookmarks from internal database into various formats.
'''
from textwrap import dedent

from ensure import ensure_annotations

from frostmark.common import fetch_bookmark_tree, traverse
from frostmark.models import Folder, Bookmark


class Exporter:
    '''
    Interface for retrieving and exporting bookmarks from local storage
    to multiple backends.
    '''
    # pylint: disable=too-few-public-methods

    @staticmethod
    @ensure_annotations
    def export_to(path: str):
        '''
        Export bookmarks from internal storage to particular path.
        '''

        xml = dedent('''
            <!DOCTYPE NETSCAPE-Bookmark-file-1>
            <!-- This is an automatically generated file.
                It will be read and overwritten.
                DO NOT EDIT!
            -->
            <META
                HTTP-EQUIV="Content-Type"
                CONTENT="text/html; charset=UTF-8"
            />
            <TITLE>Bookmarks</TITLE>
            <H1>Bookmarks</H1>
        ''')
        xml = xml[1:]  # strip first \n character

        tree = traverse(fetch_bookmark_tree())
        tree_len = len(tree)
        sep = ' ' * 4
        folder_stack = []

        for idx, node in enumerate(tree):
            if node.node_type == Folder:
                # root folder for internal DB
                if node.id == 0:
                    xml += f'{sep * len(folder_stack)}<DL><p>\n'

                elif [node.parent_folder_id] == folder_stack[-2:-1]:
                    # child folder of a second last folder on stack
                    # stack = [parent, child1]
                    # F parent
                    # |-- F child
                    # +-- F child <- this

                    # pop the sister folder from stack
                    # close the previous folder
                    folder_stack = folder_stack[:-1]
                    xml += f'{sep * len(folder_stack)}</DL><p>\n'

                    xml += (
                        f'{sep * len(folder_stack)}'
                        f'<DT><H3>{node.folder_name}</H3>\n'
                    )
                    xml += f'{sep * len(folder_stack)}<DL><p>\n'
                else:
                    xml += (
                        f'{sep * len(folder_stack)}'
                        f'<DT><H3>{node.folder_name}</H3>\n'
                    )
                    xml += f'{sep * len(folder_stack)}<DL><p>\n'

                # completely new folder, append to stack
                folder_stack.append(node.id)

                if node.id == 0:
                    continue

                # empty folder, close DL, pop from stack
                if not node.children and idx != tree_len - 1:
                    # pop from stack and close the folder
                    if node.id in folder_stack:
                        folder_stack = folder_stack[:-1]
                    xml += f'{sep * len(folder_stack)}</DL><p>\n'
                    continue

                # last element, in case it's folder close the DL
                if idx == tree_len - 1:
                    folder_stack = folder_stack[:-1]
                    xml += f'{sep * len(folder_stack)}</DL><p>\n'
                    continue

            elif node.node_type == Bookmark:
                # bookmark of a second folder on the stack
                # F
                # |-- F
                # |   +-- B
                # +-- B <- this
                if [node.folder_id] != folder_stack[-1:]:
                    folder_stack = folder_stack[:-1]
                    xml += (
                        f'{sep * len(folder_stack)}</DL><p>\n'
                        f'{sep * len(folder_stack)}<HR>\n'
                    )
                xml += (
                    f'{sep * len(folder_stack)}'
                    f'<DT><A HREF="{node.url}" '
                    f'ICON="{node.icon.decode("utf-8")}">{node.title}</A>\n'
                )

        # if there are remaining folders, those don't have
        # any children remaining, so the whole tree can be
        # closed with multiple dedented DL closings
        while folder_stack:
            folder_stack = folder_stack[:-1]
            xml += f'{sep * len(folder_stack)}</DL><p>\n'

        with open(path, 'rb') as output:
            output.write(xml.encode('utf-8'))
