import { useState, useEffect } from 'react';
import webSocket from 'socket.io-client';
import { BACKEND } from '../config';

const ws = webSocket(BACKEND);
if(ws) console.log("Websocket connected!");

export default (nameSpace, callback=null) => {
  const [recv, setRecv] = useState("");

  useEffect(() => {
    if (ws) {
      ws.on(nameSpace, message => {
        setRecv(message);
        if(callback !== null) {
          callback(message);
        }
      })
    }
  }, [nameSpace, callback])

  return recv;
}