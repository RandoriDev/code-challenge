const expect = require('expect');
const request = require('supertest');
const setup = require('./setup');

describe('Test general system function', function () {

    it('Responds with 200 on simple get with no body', function () {
        request(setup()).get('/test').expect(200);
    });

    it('Responds with 200 and body on POST with malicious=false', function () {
        const body = { is_malicious: false };
        request(setup()).post('/test').send(body)
            .set('Accept', 'application/json')
            .expect('Content-Type', 'application/json; charset=utf-8')
            .expect(200).end(function (err, res) {
                console.log(res);
                expect(res).toHaveProperty('body');
                expect(res.body).toHaveProperty('is_malicious');
                expect(res.body.is_malicious).toBe(false);
            });
    });

    it('Responds with 401 and body on POST with malicious=true', function () {
        const body = { is_malicious: true };
        request(setup()).post('/test').send(body)
            .set('Accept', 'application/json')
            .expect('Content-Type', 'application/json; charset=utf-8')
            .expect(401).end(function (err, res) {
                expect(res).toHaveProperty('text');
                expect(res.text).toBe('Unauthorized');
            });
    });

    it('Responds with 200 and waits for 2 seconds on identical subsequent calls', function () {

        let app = setup();
        request(app).get('/test').expect(200);
        let start_ts = new Date().getTime();
        request(app).get('/test')
            .expect(200).end(() => {
                let end_ts = new Date().getTime();
                expect(end_ts - start_ts).toBeGreaterThan(2000);
            });
    });

    it('Responds with 200 and does not wait for 2 seconds on non-identical subsequent calls', function () {
        let app = setup();
        request(app).get('/test').expect(200);
        let start_ts = new Date().getTime();
        request(app).get('/tested')
            .expect(200).end(() => {
                let end_ts = new Date().getTime();
                expect(end_ts - start_ts).toBeLessThan(2000);
            });
    });

});