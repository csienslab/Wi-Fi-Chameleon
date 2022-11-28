const express = require("express");
const fs = require("fs");
const router = express.Router();

router.post("/", (req, res) => {
  let dir = req.query.dir;
  let filename = req.query.filename;
  if (!dir || !filename) {
    res.status(400).send("Missing path");
    return;
  }

  path = "/home/pi/screenshots/"+dir;
  let rawData = [];

  req.on('data', data => {
    rawData.push(data);
  })
  req.on('end', async _ => {
    const totSize = rawData.reduce((sum, currBuffer) => sum + currBuffer.length, 0);
    const output = Buffer.concat(rawData, totSize);
    await fs.promises.mkdir(path, { recursive: true }).catch(console.error);
    fs.writeFile(`${path}/${filename}`, output, (err) => {
      if (err) {
        console.log(err);
        res.status(500).send("Fail");
      }
      else res.status(200).send("OK");
    })
  });
})

module.exports = router;