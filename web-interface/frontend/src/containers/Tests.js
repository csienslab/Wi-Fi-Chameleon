import React, { useState } from 'react';
import { Segment, Header, Button } from 'semantic-ui-react';
import { useAPI } from '../hooks';
import { BACKEND } from '../config';
import "../styles/settings.css";


export default () => {
  const [sendCmdState, sendCmd, initState] = useAPI();
  const [busyId, setBusyId] = useState(-1);

  const setPortal = (portal) => {
    sendCmd(BACKEND+`/cmd?cmd=set_portal&param=${portal}`);
  }

  const isBusy    = (id) => id === busyId && sendCmdState.loading;
  const isSuccess = (id) => id === busyId && sendCmdState.success;
  const isError   = (id) => id === busyId && sendCmdState.error;
  const portalButton = (id, name, portal) => {
    return (
      <Button 
        style={{marginTop: "0.5rem", marginBottom: "0.5rem"}} 
        loading={isBusy(id)} positive={isSuccess(id)} negative={isError(id)} 
        onClick={_ => {
          initState();
          setBusyId(id);
          setPortal(portal);
        }}>
        {name}
      </Button>
    )
  }

  return (
    <div>
      <div className="settings-block">

        <Segment>
          <Header as='h2'>JS API</Header>
            {portalButton(0, "Test API", "js-api")}
          <Header as='h2'>Cookie</Header>
            {portalButton(1, "Read, write, and persistence", "cookies")}
            <p>
              First round should give "Previous cookie not presented. Set Cookie successfully.", and the second round should give "Previous cookie presented.Set Cookie successfully."
            </p>
            {portalButton(2, "Value capacity", "https://wpt.live/cookies/value/value.html")}
            {portalButton(3, "SameSite", "https://samesitetest.com/setup/confirm,https://shared.samesitetest.com,https://samesitetest-external.com,http://insecure-shared.samesitetest.com,http://insecure.samesitetest-external.com,http://insecure.samesitetest.com")}
            {portalButton(4, "Secure (https)", "https://wpt.live/cookies/secure/set-from-http.https.sub.html")}
            {portalButton(5, "Secure (http)", "http://wpt.live/cookies/secure/set-from-http.https.sub.html")}
            {portalButton(27, "HttpOnly", "http://linux8.csie.ntu.edu.tw:8123/")}
            {portalButton(28, "LocalStorage", "localStorage")}
          <Header as='h2'>SOP & CORS</Header>
            {portalButton(6, "Basic", "https://wpt.live/cors/basic.htm")}
            {portalButton(7, "Origin", "https://wpt.live/cors/origin.htm")}
            <p>
              Notice that even some normal browsers can't pass all the test in basic.html.
            </p>
          <Header as='h2'>HTTP/HTTPS</Header>
            {portalButton(8, "HTTP", "default")}
            {portalButton(9, "HTTP-credit-card", "http://http-credit-card.badssl.com/")}
            {portalButton(10, "Normal HTTPS", "https://joeywang4.github.io/")}
          <Header as='h2'>Bad Certificates</Header>
            {portalButton(11, "Expired", "https://expired.badssl.com/")}
            {portalButton(12, "Wrong Host", "https://wrong.host.badssl.com/")}
            {portalButton(13, "Self-signed", "https://self-signed.badssl.com/")}
            {portalButton(14, "Untrusted root", "https://untrusted-root.badssl.com/")}
            {portalButton(15, "Revoked", "https://revoked.badssl.com/")}
            {portalButton(16, "Pinned", "https://pinning-test.badssl.com/")}
          <Header as='h2'>Bad Ciphersuite</Header>
            {portalButton(17, "Bad Cipher (DH 1024)", "https://dh1024.badssl.com/")}
          <Header as='h2'>SSL/TLS Version</Header>
            {portalButton(18, "SSL", "https://clienttest.ssllabs.com:8443/ssltest/viewMyClient.html,https://cdnjs.cloudflare.com/,https://ssllabs.com/,http://plaintext.ssllabs.com/,https://www.ssllabs.com/")}
            {portalButton(19, "TLS v1.0", "https://tls-v1-0.badssl.com:1010/")}
            {portalButton(20, "TLS v1.1", "https://tls-v1-1.badssl.com:1011/")}
          <Header as='h2'>HSTS</Header>
            {portalButton(21, "HTTPS", "https://hsts.badssl.com/")}
            {portalButton(22, "HTTP", "http://hsts.badssl.com/")}
            <p>
              Suppose that HSTS is not followed in the same session, the first portal (the https one) would no display "HSTS is working."
              <br />
              Suppose that HSTS is not followed in the different session, the second portal (the http one) would no display "HSTS is working."
            </p>
          <Header as='h2'>Misc</Header>
            {portalButton(23, "Mixed content (JS)", "https://www.mixedcontentexamples.com/Test/NonSecureJS")}
            {portalButton(24, "Mixed content (iframe)", "https://www.mixedcontentexamples.com/Test/NonSecureIFRAME")}
            {portalButton(25, "Indirect Redirection", "https://allenchou.cc/a-secret-page-for-test.html,https://self-signed.badssl.com/")}
          <Header as='h2'>Safe Browsing</Header>
            {portalButton(26, "Phishing", "https://testsafebrowsing.appspot.com/s/phishing.html")}

        </Segment>
        <div></div>
      </div>
    </div>
  )
}
