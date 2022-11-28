# How to perform tests

## JS API
```bash
sudo python3 src/main.py set_portal js-api
```

## Cookie

Read, write, and persistence
```bash
sudo python3 src/main.py set_portal cookies
```
First round should give "Previous cookie not presented. Set Cookie successfully.", and the second round should give "Previous cookie presented.Set Cookie successfully."

Value capacity:
```bash
sudo python3 src/main.py set_portal https://wpt.live/cookies/value/value.html
```

SameSite:
```bash
sudo python3 src/main.py set_portal https://samesitetest.com/setup/confirm,https://shared.samesitetest.com,https://samesitetest-external.com,http://insecure-shared.samesitetest.com,http://insecure.samesitetest-external.com,http://insecure.samesitetest.com
```

Secure:
```bash
sudo python3 src/main.py set_portal https://wpt.live/cookies/secure/set-from-http.https.sub.html # should work
sudo python3 src/main.py set_portal http://wpt.live/cookies/secure/set-from-http.https.sub.html # should not work
```
~~Note that, if the captive portal session is not sandboxed, then in the HTTP test, the two tests should be failed and pass respectively, otherwise both tests will be failed.~~

HttpOnly:
```bash
sudo python3 src/main.py set_portal http://linux8.csie.ntu.edu.tw:8123/
```

## SOP & CORS

```bash
sudo python3 src/main.py set_portal https://wpt.live/cors/basic.htm
sudo python3 src/main.py set_portal https://wpt.live/cors/origin.htm
```

Notice that even some normal browsers can't pass all the test in `basic.html`.

## SSL

HTTP:
```bash
sudo python3 src/main.py set_portal default
```

HTTP-credit-card:
```bash
sudo python3 src/main.py set_portal http://http-credit-card.badssl.com/
```

Normal:
```bash
sudo python3 src/main.py set_portal https://joeywang4.github.io/
```

Expired:
```bash
sudo python3 src/main.py set_portal https://expired.badssl.com/
```

Wrong Host:
```bash
sudo python3 src/main.py set_portal https://wrong.host.badssl.com/
```

Self-signed:
```bash
sudo python3 src/main.py set_portal https://self-signed.badssl.com/
```

Untrusted root:
```bash
sudo python3 src/main.py set_portal https://untrusted-root.badssl.com/
```

Revoked:
```bash
sudo python3 src/main.py set_portal https://revoked.badssl.com/
```

Pinned:
```bash
sudo python3 src/main.py set_portal https://pinning-test.badssl.com/
```

Bad cipher (DH 1024):
```bash
sudo python3 src/main.py set_portal https://dh1024.badssl.com/
```

Outdated TLS:
```bash
sudo python3 src/main.py set_portal https://clienttest.ssllabs.com:8443/ssltest/viewMyClient.html,https://cdnjs.cloudflare.com/,https://ssllabs.com/,http://plaintext.ssllabs.com/,https://www.ssllabs.com/ # SSL
sudo python3 src/main.py set_portal https://tls-v1-0.badssl.com:1010/ # TLS v1.0
sudo python3 src/main.py set_portal https://tls-v1-1.badssl.com:1011/ # TLS v1.1
```

HSTS:
```bash
sudo python3 src/main.py set_portal https://hsts.badssl.com/
sudo python3 src/main.py set_portal http://hsts.badssl.com/
```
Suppose that HSTS is not followed in the same session, the first portal (the https one) would no display "HSTS is working."
Suppose that HSTS is not followed in the different session, the second portal (the http one) would no display "HSTS is working."

Mixed content
```bash
sudo python3 src/main.py set_portal https://www.mixedcontentexamples.com/Test/NonSecureJS # JS
sudo python3 src/main.py set_portal https://www.mixedcontentexamples.com/Test/NonSecureIFRAME # iframe
```

Indirect Redirection:
```bash
sudo python3 src/main.py set_portal https://allenchou.cc/a-secret-page-for-test.html,https://self-signed.badssl.com/
```

## LocalStorage
```bash
sudo python3 src/main.py set_portal localStorage
```

## Safe Browsing
Phishing
```bash
sudo python3 src/main.py set_portal https://testsafebrowsing.appspot.com/s/phishing.html
```

Malware (download link)
```bash
sudo python3 src/main.py set_portal https://testsafebrowsing.appspot.com/s/malware.html
```

Malware (direct access)
```bash
sudo python3 src/main.py set_portal https://testsafebrowsing.appspot.com/s/content.exe
```