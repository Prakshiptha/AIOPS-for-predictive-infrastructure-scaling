const express = require('express');
const client = require('prom-client');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Prometheus metrics setup
const register = new client.Registry();
client.collectDefaultMetrics({ register });

const requestCounter = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
});
const submissionCounter = new client.Counter({
  name: 'form_submissions_total',
  help: 'Total number of form submissions',
});
register.registerMetric(requestCounter);
register.registerMetric(submissionCounter);

// Middleware
app.use((req, res, next) => {
  requestCounter.inc();
  next();
});
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname)));

// Routes
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.post('/submit', (req, res) => {
  submissionCounter.inc();
  const { name, email, message } = req.body;
  console.log('Form submitted:', { name, email, message });
  res.send('Form data received!');
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
