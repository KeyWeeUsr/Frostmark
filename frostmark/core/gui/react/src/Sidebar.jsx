import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

import Logo from './Logo';
import SidebarItem from './SidebarItem';


class Sidebar extends Component {
    createImportBody() {
        return <form
            enctype='multipart/form-data'
            method='post'
            action='/api/import_bookmarks'
        >
            <select name='browser'>
                <option value='firefox' selected={true}>Firefox</option>
                <option value='chrome'>Chrome</option>
                <option value='opera'>Opera</option>
            </select>
            <input name='file' type='file' />
            <input type='submit' value='submit' />
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
            <SidebarItem text='About' className='not-implemented' />
        </div>;
    }
}


export default Sidebar;
