/**
 * Main application entrypoint assembling all other components.
 */
import React, { Component } from 'react';
import './App.css';
import BookmarkList from './BookmarkList';


/**
 * Application class included in the index.js/index.html.
 */
class App extends Component {

    /**
     * Render all the components.
     */
    render() {
        return (
            <div className="App">
                <BookmarkList />
            </div>
        );
    }
}


export default App;
