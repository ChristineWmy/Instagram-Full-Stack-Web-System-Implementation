import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Likes from './likes';
import Comment from './comment';

class Post extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      imgUrl: '',
      owner: '',
      ownerImgUrl: '',
      ownerShowUrl: '',
      postShowUrl: '',
      created: '',
      postid: 0,
      comments: [],
      lognameLikesThis: 0,
      numLikes: 0,
      url: '',
    };
    this.ismounted = false;
    this.handleDoubleClick = this.handleDoubleClick.bind(this);
    this.handleButtconChange = this.handleButtconChange.bind(this);
    //  postid: '', created: ''
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    this.ismounted = true;

    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.ismounted = true;
        // this.ismounted && this.setState({
        this.setState({
          comments: data.comments,
          imgUrl: data.imgUrl,
          owner: data.owner,
          ownerImgUrl: data.ownerImgUrl,
          ownerShowUrl: data.ownerShowUrl,
          postShowUrl: data.postShowUrl,
          postid: data.postid,
          created: data.created,
          lognameLikesThis: data.likes.lognameLikesThis,
          numLikes: data.likes.numLikes,
          url: data.likes.url,
        });
        // var comments= [{commentid: '',
        //            lognameOwnsThis: '',
        //            owner: '',
        //            ownerShowUrl: '',
        //            text: '',
        //            url: '',}];
        // comments= comments.concat(data.comments.slice(0));
        // console.log(comments);
        // console.log(this.state.comments);
        // console.log(data.comments);
      })
      .catch((error) => console.log(error));
  }

  componentWillUnmount() {
    this.ismounted = false;
  }

  handleDoubleClick() {
    const { postid, lognameLikesThis, numLikes } = this.state;
    const postUrl = `/api/v1/likes/?postid=${postid}`;
    console.log();

    if (!lognameLikesThis) {
      fetch(postUrl, { credentials: 'same-origin', method: 'POST' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState({
            lognameLikesThis: 1,
            numLikes: numLikes + 1,
            url: data.url,
          });
        })
        .catch((error) => console.log(error));
    }
  }

  handleButtconChange() {
    const {
      postid, lognameLikesThis, url, numLikes,
    } = this.state;
    const postUrl = `/api/v1/likes/?postid=${postid}`;
    console.log(postid);
    // const postUrl = `/api/v1/likes/?postid=${this.state.postid}`;
    // console.log(this.state.url);
    if (lognameLikesThis) {
      fetch(url, { credentials: 'same-origin', method: 'DELETE' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
        })
        .then(() => {
          this.setState({
            // lognameLikesThis: !this.state.lognameLikesThis,
            lognameLikesThis: 0,
            numLikes: numLikes - 1,
            url: postUrl,
          });
        })
        .catch((error) => console.log(error));
    } else {
      fetch(postUrl, { credentials: 'same-origin', method: 'POST' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState({
            // lognameLikesThis: !this.state.lognameLikesThis,
            lognameLikesThis: 1,
            numLikes: numLikes + 1,
            url: data.url,
          });
        })
        .catch((error) => console.log(error));
    }
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const {
      imgUrl, owner, ownerImgUrl, ownerShowUrl, postShowUrl,
      created, url, postid, comments, numLikes, lognameLikesThis,
    } = this.state;
    const ownerShowUrlStyle = { padding: '30px 0px' };
    const postShowUrlStyle = {
      float: 'right',
      padding: '30px 15px',
    };
    // Render number of post image and post owner
    return (
      <div className="post">
        <div>
          <a href={ownerShowUrl}>
            <img className="propic" alt="" src={ownerImgUrl} />
          </a>
          <a href={ownerShowUrl} style={ownerShowUrlStyle}>{owner}</a>
          <a href={postShowUrl} style={postShowUrlStyle}>{moment.utc(created, 'YYYY-MM-DD hh:mm:ss').fromNow()}</a>
        </div>
        <img src={imgUrl} alt="" onDoubleClick={this.handleDoubleClick} />
        <Likes
          lognameLikesThis={lognameLikesThis}
          numLikes={numLikes}
          url={url}
          onLognameLikesThisChange={this.handleButtconChange}
          post_info={postid}
        />
        <Comment comments={comments} postInfo={postid} />
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
