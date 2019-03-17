import React, { Component } from 'react';
import './BookmarkLabel.css';


/**
 * Custom react-treeview/TreeView nodeLabel property element.
 */
class BookmarkLabel extends Component {
    constructor(props) {
        super(props);
        this.createModalBody = this.createModalBody.bind(this);
    }

    createModalBody() {
        return <button onClick={this.props.appRef.closeModal}>Close</button>;
    }

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

    getLabel() {
        return <span>
            {this.getHyperlink()}
            <span
                className='bookmarkLabel fa fa-pencil-square-o'
                style={{ float: 'right' }}
                onClick={() => {
                    this.props.appRef.openModal(
                        this.props.text, this.createModalBody
                    )
                }}
            />
        </span>;
    }

    render() {
        return <div
            className='info'
            key={'bookmark|' + this.props.text}
        >{this.getLabel()}</div>
    }
}


export default BookmarkLabel;
