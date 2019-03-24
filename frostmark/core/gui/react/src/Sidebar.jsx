import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

import Logo from './Logo';
import SidebarItem from './SidebarItem';


class Sidebar extends Component {
    render() {
        return <div className='sidebar'>
            <Logo />
            <SidebarItem text='Import' className='not-implemented' />
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
