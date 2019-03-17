/**
 * Main application entrypoint assembling all other components.
 */
import React, { Component } from 'react';
import './App.css';
import GlobalModal from './GlobalModal';
import BookmarkList from './BookmarkList';


/**
 * Application class included in the index.js/index.html.
 */
class App extends Component {
    constructor() {
        super();
        this.state = {
            modalIsOpen: false,
            modalTitle: '',
            modalBodyBuilder: () => {}
        };

        // Bind the functions to the instance
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }

    /**
     * Create a modal with a custom title and a function that renders its body.
     */
    openModal(title, bodyBuilder) {
        this.setState({
            modalTitle: title,
            modalIsOpen: true,
            modalBodyBuilder: bodyBuilder
        });
    }

    /**
     * Close the modal and clear the defaults.
     */
    closeModal() {
        this.setState({
            modalTitle: '',
            modalIsOpen: false,
            modalBodyBuilder: () => {}
        });
    }

    /**
     * Render all the components.
     */
    render() {
        return <div className="App">
            <GlobalModal
                appRef={this}
                isOpen={this.state.modalIsOpen}
                getBody={this.state.modalBodyBuilder}
                title={this.state.modalTitle}
            />
            <BookmarkList appRef={this} />
        </div>;
    }
}


export default App;
