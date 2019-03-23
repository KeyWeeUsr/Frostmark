import React, { Component } from 'react';
import './BookmarkList.css';

import fetch from 'node-fetch';

import TreeView from 'react-treeview';
import 'react-treeview/react-treeview.css';
import FolderLabel from './FolderLabel';
import BookmarkLabel from './BookmarkLabel';


/**
 * Component rendering the full bookmark tree with nested, collapsable
 * folders and hyperlink bookmarks.
 */
class BookmarkList extends Component {
    constructor() {
        super();
        this.className = "frostmark-bookmark-list";
        this.state = { bookmarks: [] };
    }

    /**
     * Get the required data during the component mounting.
     */
    componentWillMount() {
        this.getBookmarks();
    }

    /**
     * Fetch and store the data in the component state.
     */
    getBookmarks() {
        fetch(
            '/api/list_tree',
            { mode: "cors" }
        ).then(response => response.json()).then(data => {
            this.setState({ bookmarks: data });
        });
    }

    /**
     * Split bookmark tree into folders and bookmarks and nest them manually
     * into TreeView (folder, nested folders) and its children.
     */
    processBookmarkTree() {
        let folders = {};
        let bookmarks = {};

        this.state.bookmarks.forEach(item => {
            if (item.node_type === 'Folder') {
                folders[item.id] = {
                    id: item.id,
                    folder_name: item.folder_name,
                    children: [],
                    parent_folder_id: item.parent_folder_id,
                    node_type: item.node_type
                };
            } else if (item.node_type === 'Bookmark') {
                bookmarks[item.id] = {
                    id: item.id,
                    title: item.title,
                    url: item.url,
                    folder_id: item.folder_id,
                    node_type: item.node_type,
                    icon: item.icon
                };
            }
        });

        let item;
        Object.keys(bookmarks).forEach(key => {
            item = bookmarks[key];
            if (folders.hasOwnProperty(item.folder_id)) {
                folders[item.folder_id].children.push(item);
            }
        });

        Object.keys(folders).forEach(key => {
            item = folders[key];
            if (folders.hasOwnProperty(item.parent_folder_id)) {
                if (item.parent_folder_id !== null) {
                    folders[item.parent_folder_id].children.push(item);
                }
            }
        });

        return folders[0];
    }

    traverse(node) {
        let result;
        if (node === undefined) {
            return <BookmarkLabel text="No data found." />;
        }
        if (node.node_type === 'Folder') {
            if (!node.children.length) {
                result = (
                    <TreeView
                        key={'folder|' + node.id}
                        nodeLabel={
                            <FolderLabel text={node.folder_name}></FolderLabel>
                        }
                    />
                );
            } else {
                result = (
                    <TreeView
                        key={'folder|' + node.id}
                        nodeLabel={
                            <FolderLabel text={node.folder_name}></FolderLabel>
                        }
                    >
                        {node.children.map(child => this.traverse(child))}
                    </TreeView>
                );
            }
        } else if (node.node_type === 'Bookmark') {
            result = <BookmarkLabel
                key={'bookmark|' + node.id}
                id={node.id}
                folder_id={node.folder_id}
                url={node.url}
                icon={node.icon}
                text={node.title}
                appRef={this.props.appRef}
            />;
        }
        return result;
    }

    render() {
        return <div className={this.className}>
            {this.traverse(this.processBookmarkTree())}
        </div>;
    }
}


export default BookmarkList;
