import http from 'http';

const trips = [];

function handleRequest(req, res) {
  if (req.method === 'GET' && req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok' }));
  } else if (req.method === 'GET' && req.url === '/trips') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(trips));
  } else if (req.method === 'POST' && req.url === '/auth/register') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const data = JSON.parse(body || '{}');
        // placeholder registration logic
        const user = { id: Date.now(), ...data };
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(user));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'invalid json' }));
      }
    });
  } else {
    res.writeHead(404);
    res.end();
  }
}

const server = http.createServer(handleRequest);

if (process.env.NODE_ENV !== 'test') {
  const port = process.env.PORT || 3000;
  server.listen(port, () => {
    console.log(`Server listening on port ${port}`);
  });
}

export default server;
