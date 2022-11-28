const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');

const apiRoute = require("./routes/api");
const fileRoute = require("./routes/file");

// Create server to serve index.html
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = process.env.PORT || 3001;

// Routing
app.use(cors());
app.use(express.json());
app.use('/upload', fileRoute);
app.use('/', apiRoute);
app.set('io', io);

fs.watch("/home/pi/WiFi-Chameleon/data/password.log", () => {
  io.emit("password_log", "Changed");
});

// Start server listening process.
http.listen(port, () => {
  console.log(`Server listening on port ${port}.`);
});