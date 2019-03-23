import React, { Component } from 'react';
import './SidebarItem.css';


class SidebarItem extends Component {
    render() {
        return <div className='logo-item'>
            <div className='logo-item-label'>{this.props.text}</div>
        </div>;
    }
}


export default SidebarItem;
