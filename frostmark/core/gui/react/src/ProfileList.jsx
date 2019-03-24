import React, { Component } from 'react';
import fetch from 'node-fetch';

import './ProfileList.css';


class ProfileList extends Component {
    constructor() {
        super();
        this.state = {
            profiles: {}
        };
    }

    componentWillMount() {
        this.getProfiles();
    }

    getProfiles() {
        fetch(
            '/api/list_profiles',
            { mode: "cors" }
        ).then(response => response.json()).then(data => {
            this.setState({ profiles: data });
        });
    }

    render() {
        return <div className='profile-list'><dl>{
            Object.keys(this.state.profiles).map(browser => {
                const title = <dt>{browser}</dt>;
                const items = this.state.profiles[browser].map(profile => {
                    return <dd>{profile}</dd>;
                });
                if (!this.state.profiles[browser].length) {
                    return [];
                } else {
                    return [title, items];
                }
            })
        }</dl></div>;
    }
}


export default ProfileList;
