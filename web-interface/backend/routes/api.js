const express = require("express");
const router = express.Router();
const { spawn } = require('child_process');

const main_path = "/home/pi/WiFi-Chameleon/src/main.py";

const subprocess = (cmd, args, onClose = (() => 0)) => {
  const proc = spawn(cmd, args);
  let stdout = "";

  proc.stdout.on('data', data => stdout = data);
  proc.on('close', (code) => onClose(stdout, code));
}

router.get("/cmd", (req, res) => {
  if (!req.query.cmd) {
    res.status(400).send("Missing command");
    return;
  }
  let options = [main_path, req.query.cmd];
  if (req.query.param) options.push(req.query.param);
  subprocess('python3', options, (stdout, code) => {
    if (code === 0 && req.query.json) res.type('json').status(200).send(stdout);
    else if (code === 0) res.type('text/plain').status(200).send(stdout);
    else res.status(500).send(`Error code: ${code}`)
  })
})

router.get("/attack", (req, res) => {
  if (!req.query.ssid) {
    res.status(400).send("Missing ssid");
    return;
  }

  let output = "";
  const proc = spawn('python3', ["-u", main_path, "attack", req.query.ssid]);
  proc.stdout.on('data', data => {
    output += data;
    req.app.get('io').emit(`attack-${req.query.namespace}`, `${output}`);
  });
  proc.stderr.on('data', data => {
    console.log(`Error! ${data}`);
  })
  proc.on("close", (code) => {
    if (code !== 0) {
      console.log(`Exit code: ${code}, stopping attack...`);
      return;
    }
    console.log(`Attack success.`);
  })
  res.status(200).send("OK");
})

router.get("/stop-attack", (_, res) => {
  subprocess('python3', [main_path, "stop_attack"], (_, code) => {
    if (code === 0) res.status(200).send("OK");
    else res.status(500).send(`Error code: ${code}`);
  })
})

module.exports = router;