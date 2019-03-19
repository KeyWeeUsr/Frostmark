/**
 * Global modal centered floating element with custom title and a body building
 * function to allow more flexibility while creating the body.
 */
import React, { Component } from 'react';
import Modal from 'react-modal';


// Change to dark color theme.
Modal.defaultStyles.overlay.backgroundColor = '#333333AA';
Modal.defaultStyles.content.backgroundColor = '#222222CC';
Modal.defaultStyles.content.border = '#333333CC';


class GlobalModal extends Component {
    render() {
        return <Modal
            ariaHideApp={false}
            isOpen={this.props.isOpen}
            style={{
                content: {
                    // auto-adjust height and bottom space
                    height: 'auto',
                    bottom: 'auto',

                    // dynamic 80% viewport width
                    width: '80vw',

                    // move origin to center
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)'
                }
            }}
        >
            <h2>{this.props.title}</h2>
            {this.props.getBody()}
        </Modal>;
    }
}


export default GlobalModal;
