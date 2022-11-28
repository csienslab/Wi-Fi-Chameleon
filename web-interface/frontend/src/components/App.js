import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import { Message } from 'semantic-ui-react';
import NavBar from './NavBar';
import Menu from './Menu';
import WiFi from '../containers/WiFi';
import Phish from '../containers/Phish';
import Settings from '../containers/Settings';
import Tests from '../containers/Tests';
import Home from '../containers/Home';
import "../styles/app.css";

function App() {

  return (
    <BrowserRouter>
      <NavBar />
      <div className="main-container">
        <Menu />
        <div className="content-container">
          <Switch>
            <Route exact path="/">
              <Home />
            </Route>
            <Route exact path="/wifi">
              <WiFi />
            </Route>
            <Route exact path="/phishing">
              <Phish />
            </Route>
            <Route exact path="/settings">
              <Settings />
            </Route>
            <Route exact path="/tests">
              <Tests />
            </Route>
            <Route path="/:unknown">
              {({ match }) => (
                <div className="err-msg">
                  <Message negative>
                    <Message.Header>404</Message.Header>
                    {`${match.params.unknown} Not Found!`}
                  </Message>
                </div>
              )}
            </Route>
          </Switch>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;