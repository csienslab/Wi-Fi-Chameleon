import React from 'react';
import { Header } from 'semantic-ui-react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { logout } from '../actions';
import "../styles/navbar.css";

const mapStateToProps = (state) => ({
  hasLoggedin: state.token !== undefined,
  name: state.name,
  id: state.id
})

const mapDispatchToProps = { logout };

const NavBar = ({ hasLoggedin, name, logout }) => (
  <div className="my-div">
    <Header style={{flexGrow: 100, margin: 0}} as='h1'>
      <Link className="nav-title" to="/">
        <span className="my-icon" role="img" aria-label="Fishing">🎣</span>
        Wi-Fi Chameleon
      </Link>
    </Header>
  </div>
)

export default connect(mapStateToProps, mapDispatchToProps)(NavBar);