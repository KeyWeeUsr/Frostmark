import React, { Component } from 'react';

import './About.css';
import Foldable from './Foldable';


class About extends Component {
    constructor() {
        super();
        this.state = {
            licenses: {}
        };
    }

    componentWillMount() {
        this.getLicenses();
    }

    getLicenses() {
        fetch(
            '/api/all_licenses',
            { mode: "cors" }
        ).then(response => response.json()).then(data => {
            this.setState({ licenses: data });
        });
    }

    render() {
        return <div className='about'>
            <p>Frostmark is a simple bookmarks manager. It can import all
            bookmarks from multiple browsers, list the imported bookmarks and
            export them via HTML format.</p>

            <p>The goal for the future is to be able to extensively manage the
            bookmarks both via console and GUI interface, automatically search
            the system for the available browsers, import the profiles without
            explicitly specifying paths to the browser profiles and export all
            or only specific folders even directly into the browser&#39;s
            bookmarks.</p>

            <p>Feel free to open a pull request with your improvements for the
            project, open an issue in case of bug or a feature request and come
            and talk about the project in the &nbsp;
            <a href="https://riot.im/app/#/group/+frostmark:matrix.org">
            Matrix community</a></p>

            {
                Object.keys(this.state.licenses).map(
                    key => <Foldable
                        title={
                            this.state.licenses[key].commit
                            ? `${key} (${this.state.licenses[key].commit})`
                            : key
                        }
                        text={ this.state.licenses[key].license }
                    />
                )
            }
        </div>;
    }
}


export default About;
