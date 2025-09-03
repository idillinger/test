import test from 'node:test';
import assert from 'node:assert';
import server from '../src/index.js';

let port;
await new Promise(resolve => server.listen(0, () => {
  port = server.address().port;
  resolve();
}));

const base = `http://localhost:${port}`;

test.after(() => {
  server.close();
});

test('GET / returns ok', async () => {
  const res = await fetch(base);
  const body = await res.json();
  assert.equal(res.status, 200);
  assert.equal(body.status, 'ok');
});

test('POST /auth/register returns created user', async () => {
  const res = await fetch(base + '/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Alice' })
  });
  const body = await res.json();
  assert.equal(res.status, 201);
  assert.equal(body.name, 'Alice');
  assert.ok(body.id);
});
