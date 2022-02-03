import React from 'react';
import PropTypes from 'prop-types';

class Comment extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { comments: [], value: '' };
    this.handleChange = this.handleChange.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
  }

  static getDerivedStateFromProps(props, state) {
    const prevProps = state.prevProps || {};
    const controlledValue = prevProps.comments !== props.comments ? props.comments : state.comments;
    return {
      prevProps: props,
      comments: controlledValue,
    };
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleKeyDown(event) {
    const { postInfo } = this.props;
    const url = `/api/v1/comments/?postid=${postInfo}`;
    // const url = `/api/v1/comments/?postid=${this.props.post_info}`;
    event.preventDefault();
    const { value } = this.state;
    console.log(value);
    const requestOptions = {
      credentials: 'same-origin',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: value }),
      // body: JSON.stringify({ text: this.state.value }),
    };
    fetch(url, requestOptions)
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((prevState) => ({
          comments: prevState.comments.concat(data),
        }));
      })
      .catch((error) => console.log(error));
    this.setState({ value: '' });
  }

  handleClick(commentid, url) {
    fetch(url, { credentials: 'same-origin', method: 'DELETE' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));
    // this.setState({
    //   comments: this.state.comments.filter((comment) => comment.commentid !== commentid),
    // });

    this.setState((prev) => ({
      comments: prev.comments.filter((comment) => comment.commentid !== commentid),
    }));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const ownerStyle = {
      float: 'left', lineHeight: '5px', marginTop: '-10px', fontWeight: 'bold',
    };
    const buttonStyle = { float: 'right', marginRight: '5px' };
    // Render number of post image and post owner

    const { value, comments } = this.state;

    return (
      <div>
        {comments.map((item) => (
          <p key={item.commentid}>
            <a href={item.ownerShowUrl} key={item.owner} style={ownerStyle}>{item.owner}</a>
            {` ${item.text}`}
            {item.lognameOwnsThis ? (
              <button type="button" className="delete-comment-button" style={buttonStyle} onClick={this.handleClick.bind(this, item.commentid, item.url)}>
                Delete Comment
              </button>
            ) : null }
            <br />
          </p>
        ))}
        <form className="comment-form" onSubmit={this.handleKeyDown}>
          <input type="text" value={value} onChange={this.handleChange} />
        </form>
      </div>
    );
  }
}

Comment.propTypes = {
  postInfo: PropTypes.number.isRequired,
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      commentid: PropTypes.number.isRequired,
      lognameOwnsThis: PropTypes.bool.isRequired,
      owner: PropTypes.string.isRequired,
      ownerShowUrl: PropTypes.string.isRequired,
      text: PropTypes.string.isRequired,
      url: PropTypes.string.isRequired,
    }),
  ).isRequired,
};

export default Comment;
