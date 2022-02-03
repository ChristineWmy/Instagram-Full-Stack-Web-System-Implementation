import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    // this.state = { lognameLikesThis: props.lognameLikesThis,
    //                numLikes: '',
    //                url: '' };

    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    const { onLognameLikesThisChange } = this.props;
    onLognameLikesThisChange();
    // this.props.onLognameLikesThisChange();
    // this.setState(prevState => ({
    //   lognameLikesThis: !prevState.lognameLikesThis
    // }));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    // const {  } = this.state;
    // const a_style1 = {display: 'inline',};
    // const a_style2 = {float: 'right',
    //                     padding: '30px 15px',};
    // Render number of post image and post owner
    const { lognameLikesThis, numLikes } = this.props;
    return (
      <div>
        <button type="button" onClick={this.handleClick} className="like-unlike-button">
          {lognameLikesThis ? 'unlike' : 'like'}
        </button>
        <p>
          <span>{numLikes}</span>
          <span>{numLikes === 1 ? ' like' : ' likes'}</span>
        </p>
      </div>
    );
  }
}

Likes.propTypes = {
  onLognameLikesThisChange: PropTypes.func.isRequired,
  lognameLikesThis: PropTypes.number.isRequired,
  numLikes: PropTypes.number.isRequired,
};

export default Likes;
