import React, { Component } from 'react';


/**
 * Custom react-treeview/TreeView nodeLabel property element.
 */
class FolderLabel extends Component {
    render() {
        return <span className="node">{this.props.text}</span>;
    }
}


export default FolderLabel;
