import React, { Component } from 'react';
import './Sidebar.css';

import Logo from './Logo';


class Sidebar extends Component {
    render() {
        return <div className='Sidebar'>
            <Logo />
        </div>;
    }
}


export default Sidebar;
