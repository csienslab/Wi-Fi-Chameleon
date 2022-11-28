import React, { useState } from 'react';
import { Loader } from 'semantic-ui-react';
import PasswordList from '../components/PasswordList';
import ErrMsg from '../components/ErrMsg';
import { useAPI, useWs } from '../hooks';
import { BACKEND } from '../config';

export default () => {
  const [passwordState, getPassword] = useAPI("json");
  const hidePassword = useAPI()[1];
  const deletePassword = useAPI()[1];
  const [filter, setFilter] = useState([]);
  useWs("password_log", () => {getPassword(BACKEND + "/cmd?cmd=load_password")});
  let node = <Loader active />;
  let list = passwordState.response || [];

  if (passwordState.isInit()) {
    getPassword(BACKEND + "/cmd?cmd=load_password");
  }

  const doHide = (id) => {
    console.log(`Hide ${id}`);
    hidePassword(BACKEND + `/cmd?cmd=hide_password&param=${id}`);
    setFilter([...filter, id]);
  }
  const doDelete = (id) => {
    console.log(`Delete ${id}`);
    deletePassword(BACKEND + `/cmd?cmd=delete_password&param=${id}`);
    setFilter([...filter, id]);
  }

  if (passwordState.success || passwordState.loading) {
    node = (
      <PasswordList
        list={list.filter(password => !filter.includes(password.id) && password.hide === 0)}
        doHide={doHide}
        doDelete={doDelete}
      />
    );
  }
  else if (passwordState.error) {
    node = <ErrMsg />;
  }

  return node;
}