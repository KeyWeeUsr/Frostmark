import React, { Component } from 'react';


/**
 * Custom react-treeview/TreeView nodeLabel property element.
 */
class BookmarkLabel extends Component {
    createIconLabel() {
        return <span><img
            // data:image/png;base64,encodedstring
            src={this.props.icon}
            alt={this.props.text}
        /> {this.props.text}</span>;
    }

    getHyperlink() {
        return <a
            href={this.props.url}
            target="_blank"
            rel="noopener noreferrer"
        >{
            this.props.icon ? this.createIconLabel() : this.props.text
        }</a>;
    }

    render() {
        return <div
            className='info'
            key={'bookmark|' + this.props.text}
        >{this.getHyperlink()}</div>
    }
}


export default BookmarkLabel;
