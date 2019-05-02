import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

import Logo from './Logo';
import SidebarItem from './SidebarItem';


class Sidebar extends Component {
    constructor() {
        super();
        this.createImportBody = this.createImportBody.bind(this);
    }

    createImportBody() {
        return <form
            enctype='multipart/form-data'
            method='post'
            action='/api/import_bookmarks'
        >
            <h4>Choose bookmark browser type:</h4>
            <p className='bookmarkLabelParagraph'>
                <select name='browser'>
                    <option value='firefox' selected={true}>Firefox</option>
                    <option value='chrome'>Chrome</option>
                    <option value='opera'>Opera</option>
                </select>
            </p>
            <h4>Select a bookmark profile:</h4>
            <p className='bookmarkLabelParagraph'>
                <input name='file' type='file' />
            </p>
            <p className='bookmarkLabelParagraph'>
                <input type='submit' value='Import' />
                <button
                    onClick={this.props.appRef.closeModal}
                    style={{ float: 'right' }}
                >
                    Cancel
                </button>
            </p>
        </form>;
    }

    render() {
        return <div className='sidebar'>
            <Logo />
            <SidebarItem
                text='Import'
                action={event => {
                    this.props.appRef.openModal(
                        'Import bookmarks', this.createImportBody
                    );
                }}
            />
            <SidebarItem
                text='Export'
                action={event => {
                    const win = window.open(
                        '/api/export_bookmarks',
                        '_blank'
                    );
                    win.focus();
                }}
            />
            <Link to='/bookmark-list'>
                <SidebarItem text='Bookmarks' />
            </Link>
            <Link to='/profile-list'>
                <SidebarItem text='Profiles' />
            </Link>
            <SidebarItem
                text='Contribute'
                action={event => {
                    const win = window.open(
                        'https://github.com/KeyWeeUsr/frostmark',
                        '_blank'
                    );
                    win.focus();
                }}
            />
            <Link to='/about'>
                <SidebarItem text='About' />
            </Link>
        </div>;
    }
}


export default Sidebar;
