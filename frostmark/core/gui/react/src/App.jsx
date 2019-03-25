/**
 * Main application entrypoint assembling all other components.
 */
import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import './App.css';
import GlobalModal from './GlobalModal';
import BookmarkList from './BookmarkList';
import Sidebar from './Sidebar';
import ProfileList from './ProfileList';


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
        return <div className="app">
            <Router>
                <Sidebar appRef={this} />
                <GlobalModal
                    appRef={this}
                    isOpen={this.state.modalIsOpen}
                    getBody={this.state.modalBodyBuilder}
                    title={this.state.modalTitle}
                />
                <Route path='/bookmark-list' component={
                    () => <BookmarkList appRef={this} />
                } />
                <Route path='/profile-list' component={
                    () => <ProfileList appRef={this} />
                } />
            </Router>
        </div>;
    }
}


export default App;
