import React, { Component } from 'react';
import './Sidebar.css';

import Logo from './Logo';
import SidebarItem from './SidebarItem';


class Sidebar extends Component {
    render() {
        return <div className='Sidebar'>
            <Logo />
            <SidebarItem text='Import' />
            <SidebarItem text='Export' />
            <SidebarItem text='List profiles' />
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
            <SidebarItem text='About' />
        </div>;
    }
}


export default Sidebar;
