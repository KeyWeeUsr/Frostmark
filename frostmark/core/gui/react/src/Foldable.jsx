import React, { Component } from 'react';


class Foldable extends Component {
    constructor() {
        super();
        this.foldableElement = null;
        this.state = {
            defaultFoldableStyle: {
                backgroundColor: '#404040',
                color: '#66CCFF',
                cursor: 'pointer',
                padding: '1em 1em 1em 2em',
                width: '100%',
                border: '1px outset #333333',
                textAlign: 'left',
                outline: 'none'
            },
            defaultContentStyle: {
                padding: '1em 1em',
                display: 'none',
                overflow: 'hidden',
                whiteSpace: 'pre',
                backgroundColor: '#333333'
            },
            defaultHoverOverStyle: {
                backgroundColor: '#66CCFF',
                color: '#333334'
            },
            defaultHoverOutStyle: {
                backgroundColor: '#404040',
                color: '#66CCFF'
            }
        };
        this.openFoldable = this.openFoldable.bind(this);
        this.setHoverOver = this.setHoverOver.bind(this);
        this.setHoverOut = this.setHoverOut.bind(this);
        this.setDeltaStyle = this.setDeltaStyle.bind(this);
    }

    openFoldable() {
        let content = this.foldableElement;
        content = content.getElementsByClassName('content')[0];

        if (content.style.display === 'block') {
            content.style.display = 'none';
        } else {
            content.style.display = 'block';
        }
    }

    setDeltaStyle(deltaStyle) {
        const button = this.foldableElement.getElementsByTagName('button')[0];
        Object.keys(deltaStyle).forEach(
            item => button.style[item] = deltaStyle[item]
        );
    }

    setHoverOver() {
        this.setDeltaStyle(
            this.props.hoverOverStyle || this.state.defaultHoverOverStyle
        );
    }

    setHoverOut() {
        this.setDeltaStyle(
            this.props.hoverOutStyle || this.state.defaultHoverOutStyle
        );
    }

    render() {
        return <div
            ref={el => this.foldableElement = el}
            onMouseDown={ this.openFoldable }
            onMouseOver={ this.setHoverOver }
            onMouseOut={ this.setHoverOut }
        >
            <button
                style={
                    this.props.foldableStyle || this.state.defaultFoldableStyle
                }
            >
                { this.props.title }
            </button>
            <div
                className='content'
                style={
                    this.props.contentStyle || this.state.defaultContentStyle
                }
            >{ this.props.text }</div>
        </div>;
    }
}


export default Foldable;
