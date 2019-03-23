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
            <SidebarItem text='Contribute' />
            <SidebarItem text='About' />
        </div>;
    }
}


export default Sidebar;
