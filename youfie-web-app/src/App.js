import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Richard and Friends</h2>
        </div>
        <p className="App-intro">
          We are a group of scientists and technologists that specialize in avant-garde algorithms and quantitative methods pertaining to the derivation of alpha from complex signal haversted from the web.
        </p>
      </div>
    );
  }
}

export default App;
