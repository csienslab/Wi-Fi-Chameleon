import React from 'react';
import { Loader } from 'semantic-ui-react';
import DaemonList from '../components/DaemonList';
import ErrMsg from '../components/ErrMsg';
import { useAPI } from '../hooks';
import { BACKEND } from '../config';

export default () => {
  const [getStatusState, getStatus] = useAPI('json', );
  if(getStatusState.isInit()) {
    getStatus(BACKEND+`/cmd?cmd=status&json=1`);
  }

  let node = null;
  if(getStatusState.loading) {
    node = <Loader active />;
  }
  else if(getStatusState.error) {
    node = <ErrMsg />;
  }
  else {
    node = <DaemonList list={getStatusState.response} />;
  }

  return (
    <div>
      {node}
    </div>
  )
}