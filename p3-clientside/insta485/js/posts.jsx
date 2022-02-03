import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Posts extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      postsInfo: [],
      next: '',
    };
    //  postid: '', created: ''
    this.handleScroll = this.handleScroll.bind(this);
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          postsInfo: data.results,
          next: data.next,
        });
      })
      .catch((error) => console.log(error));
  }

  handleScroll() {
    const { postsInfo, next } = this.state;
    // console.log(next)

    fetch(next, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          postsInfo: postsInfo.concat(data.results),
          next: data.next,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    // Render number of post image and post owner
    if (String(window.performance.getEntriesByType('navigation')[0].type) === 'back_forward') {
      this.state = window.history.state;
    }
    window.history.replaceState(this.state, '', '/');
    const { postsInfo, next } = this.state;
    return (
      <div className="posts">
        <InfiniteScroll
          dataLength={postsInfo.length}
          next={this.handleScroll}
          hasMore={next !== ''}
          loader={<h4>Loading...</h4>}
        >
          {postsInfo.map((postInfo) => (
            <div key={postInfo.postid}>
              <Post url={postInfo.url} />
            </div>
          ))}
          {/* {posts_url} */}
        </InfiniteScroll>
      </div>
    );
  }
}

Posts.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Posts;
