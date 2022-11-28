import React, { useState, useEffect } from 'react';
import { Loader, Segment, Header } from 'semantic-ui-react';
import WiFiList from '../components/WiFiList';
import ErrMsg from '../components/ErrMsg';
import ConnStatus from '../components/ConnStatus';
import { useAPI, useWs } from '../hooks';
import { BACKEND } from '../config';
import '../styles/wifi.css';

const connected = (state) => state && state.wpa_state && state.wpa_state === "COMPLETED";

export default () => {
  const [currentWifiState, getCurrentWifi] = useAPI("json");
  const [scanWifiState, scanWifi] = useAPI("json");
  const [stopAttackState, doStopAttack] = useAPI();
  const [attackState, doAttack] = useAPI();
  const [reload, setReload] = useState(false);
  const id = `${Math.floor(Math.random() * 100000)}`;
  const recv = useWs(`attack-${id}`)

  useEffect(() => {
    if((stopAttackState.success) && !reload) {
      setTimeout(() => {
        setReload(true);
      }, 1000)
    }
  }, [stopAttackState, attackState, reload])

  if(reload) {
    window.location.reload();
  }

  if (currentWifiState.isInit()) {
    getCurrentWifi(BACKEND + `/cmd?cmd=connection_status&json=1`);
    scanWifi(BACKEND + `/cmd?cmd=scan&json=1`);
  }

  const attack = (ssid) => {
    console.log(`Starting attack for ssid: ${ssid}`);
    doAttack(BACKEND + `/attack?ssid=${ssid}&namespace=${id}`)
  }

  const stopAttack = () => {
    console.log("Stopping attack");
    doStopAttack(BACKEND + "/stop-attack");
  }

  let node = null;
  if (currentWifiState.isInit() || currentWifiState.loading) {
    node = <Loader active={true}>Loading current connection...</Loader>;
  }
  else if (currentWifiState.success && scanWifiState.loading) {
    if (connected(currentWifiState.response)) {
      node = (
        <div>
          <WiFiList list={[currentWifiState.response]} current={true} onClick={stopAttack} />
          <Loader active={true}>Loading available APs...</Loader>
        </div>
      )
    }
    else {
      node = <Loader active={true}>Loading available APs...</Loader>;
    }
  }
  else if (currentWifiState.error || scanWifiState.error) {
    node = <ErrMsg />;
  }
  else {
    let attack_msg = <Loader active>Waiting for attack result...</Loader>;
    if (recv !== "") {
      attack_msg = (
        <div className="wifi-list-container">
          <Header className="wifi-list-title" as="h5" textAlign="center">
            Attack result
          </Header>
          <Segment className="wifi-attack-msg" inverted>
            {recv}
          </Segment>
        </div>
      );
    }
    node = (
      <div>
        {
          connected(currentWifiState.response) ?
            <WiFiList list={[currentWifiState.response]} current={true} onClick={stopAttack} /> :
            null
        }
        <ConnStatus state={stopAttackState} loadingMsg="Stopping attack..." />
        <WiFiList
          list={scanWifiState.response}
          onClick={connected(currentWifiState.response) ? null : attack}
        />
        {
          attackState.success ? attack_msg : null
        }
      </div>
    );
  }

  return node;
}