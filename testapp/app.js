var express = require('express');
var app = express();

app.use(function(req, res, next) {
  res.contentType("application/json");
  next();
});

app.get('/', function (req, res) {
  res.send('{"msg": "Hello World!"}"');
});

app.get('/user', function (req, res) {
  res.send('{"msg": "Samar"}"');
});

app.post('/', function (req, res) {
  res.send('"msg": "Got a POST request"}');
});

app.put('/', function (req, res) {
  res.send('"msg": "Got a PUT request"}');
});

app.post('/user', function (req, res) {
  res.send('"msg": "Got a POST request for creating user"}');
});

app.put('/user', function (req, res) {
  res.send('"msg": "Got a PUT request at /user"}');
});

app.delete('/user', function (req, res) {
  res.send('"msg": "Got a DELETE request at /user"}');
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
