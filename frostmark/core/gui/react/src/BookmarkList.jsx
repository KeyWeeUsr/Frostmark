import React, { Component } from 'react';
import fetch from 'node-fetch';


class BookmarkList extends Component {
    constructor() {
        super();
        this.state = {
            bookmarks: []
        };
    }

    componentWillMount() {
        this.getBookmarks();
    }

    getBookmarks() {
        fetch(
            './list_bookmarks', {
                mode: "cors"
            }
        ).then(response => response.json()).then(data => {
            this.setState({
                bookmarks: data
            });
        });
    }

    createBookmarkList() {
        let list = [];

        this.state.bookmarks.forEach(item => {
            list.push(
                <li style={{ wordSpacing: 10 }} key={item.node_type + item.id}>
                    {item.id} {item.node_type}
                </li>
            );
        });
        return list;
    }

    render() {
        return (
            <ul>
                {this.createBookmarkList()}
            </ul>
        );
    }
}


export default BookmarkList;
