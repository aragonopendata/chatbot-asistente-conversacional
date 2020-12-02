const request = require('supertest');
const app = require('../server/app');
//const host = process.env.HOST || 'localhost';
//const port = process.env.PORT;

/*
test('ServerUp', () => {
  const URL = `http://${host}:${port}`;
  console.debug(URL);
  return request(URL).get("/graphs/").then(response => {
    expect(response.statusCode).toBe(200)
  })
});
*/

// test('API GetChatList', async (done) => {
//   const response = await request(app).get("/getChatList");
//   expect(response.statusCode).toBe(200);
//   done();
// });

// test('API GetDataChart', async (done) => {
//   const response = await request(app).get("/dataChart");
//   expect(response.statusCode).toBe(200);
//   done();
// });
