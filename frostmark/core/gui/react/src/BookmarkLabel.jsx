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
        return <form className='bookmarkLabelForm' action='./tbd'>
            <p className='bookmarkLabelParagraph'>
                <label>Title</label>
                <input
                    className='bookmarkLabelInput'
                    type='text'
                    name='title'
                    value={this.props.text}
                />
            </p>
            <p className='bookmarkLabelParagraph'>
                <label>URL</label>
                <input
                    className='bookmarkLabelInput'
                    type='url'
                    name='url'
                    value={this.props.url}
                />
            </p>
            <p className='bookmarkLabelParagraph'>
                <label>Folder</label>
                <select
                    className='bookmarkLabelInput'
                    name='folder'
                >
                    <option>1</option>
                    <option>2</option>
                    <option>3</option>
                </select>
            </p>
            <p className='bookmarkLabelParagraph'>
                <input type='submit' value='Save' />
                <button
                    onClick={this.props.appRef.closeModal}
                    style={{ float: 'right' }}
                >
                    Cancel
                </button>
            </p>
        </form>;
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
                        'Edit bookmark', this.createModalBody
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
