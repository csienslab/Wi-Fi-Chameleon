import React from 'react';
import ReactDOM from 'react-dom';
import { createStore } from 'redux';
import { Provider } from 'react-redux';
import rootReducer from './reducers'
import { loadState, saveState } from './localState';
import throttle from 'lodash/throttle';
import App from './components/App';
import 'semantic-ui-css/semantic.min.css';

const persistedState = loadState();
const store = createStore(rootReducer, persistedState);
store.subscribe(throttle(() => {
  saveState(store.getState());
}, 1000));

ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);