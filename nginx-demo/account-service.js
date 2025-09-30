// account-service.js
const express = require('express');
const app = express();

app.get('/api/account', (req, res) => {
  res.json({ service: 'account', message: 'Hello from account service!' });
});

app.listen(3001, () => console.log('Account service running on port 3001'));
