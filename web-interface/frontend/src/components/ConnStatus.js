import React, { useState, useEffect } from 'react';
import { Loader, Message } from 'semantic-ui-react';

export default ({state, loadingMsg="Loading", timeout=0}) => {
  const [dontShow, setDontShow] = useState(false);
  const [timeoutId, setTimeoutId] = useState(null);
  useEffect(() => {
    if((state.success || state.success) && timeout > 0 && !dontShow) {
      setTimeoutId(setTimeout(() => {
        setDontShow(true);
      }, timeout))
    }
  }, [state, timeout, dontShow])

  const clearDontShow = () => {
    if(dontShow) setDontShow(false);
    if(timeoutId !== null) {
      clearTimeout(timeoutId);
      setTimeoutId(null);
    }
  }

  let node = null;
  if(!state || state.loading) {
    clearDontShow();
    node = <Loader active>{loadingMsg}</Loader>;
  }
  else if(state.success) {
    node = <Message positive>Success!</Message>;
  }
  else if(state.error) {
    node = <Message negative>{state.errMsg || "Error!"}</Message>;
  }
  else {
    clearDontShow();
    node = null;
  }
  return (
    dontShow?null:
    <div style={{margin: "1rem"}}>
      {node}
    </div>
  )
}