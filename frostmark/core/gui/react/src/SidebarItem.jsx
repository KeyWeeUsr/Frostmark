import React, { Component } from 'react';
import './SidebarItem.css';


class SidebarItem extends Component {
    render() {
        return <div
            className={
                this.props.className
                ? `logo-item ${this.props.className}`
                : 'logo-item'
            }
            onClick={this.props.action}
        >
            <div className='logo-item-label'>{this.props.text}</div>
        </div>;
    }
}


export default SidebarItem;
