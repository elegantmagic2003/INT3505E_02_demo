// product-service.js
const express = require('express');
const app = express();

app.get('/api/product', (req, res) => {
  res.json({ service: 'product', message: 'Hello from product service!' });
});

app.listen(3003, () => console.log('Product service running on port 3003'));
