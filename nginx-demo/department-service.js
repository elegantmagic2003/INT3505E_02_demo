// department-service.js
const express = require('express');
const app = express();

app.get('/api/department', (req, res) => {
  res.json({ service: 'department', message: 'Hello from department service!' });
});

app.listen(3002, () => console.log('Department service running on port 3002'));
