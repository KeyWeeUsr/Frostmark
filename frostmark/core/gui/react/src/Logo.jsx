import React, { Component } from 'react';
import './Logo.css';


class Logo extends Component {
    textLogo() {
        return [
            '╔═╗┬─┐┌─┐┌─┐┌┬┐┌┬┐┌─┐┬─┐┬┌─',
            '╠╣ ├┬┘│ │└─┐ │ │││├─┤├┬┘├┴┐',
            '╚  ┴└─└─┘└─┘ ┴ ┴ ┴┴ ┴┴└─┴ ┴'
        ];
    }

    render() {
        return <div className='logo'>
            <code className='logo-line'>
                {this.textLogo().map((item) => {
                    return item + '\n'
                })}
            </code>
        </div>;
    }
}


export default Logo;
