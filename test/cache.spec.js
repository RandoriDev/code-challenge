const expect = require('expect');
const Cache = require('../src/client_cache');
const client_cache = new Cache();

describe('Test Cache', function () {
    it('inserts item into cache correctly', function () {
        let ctx = {
            request: {
                ip: "192.168.1.4",
                url: '/test'
            }
        }
        expect(client_cache.insert(ctx)).toBe(false);
        //we get true on last value equal to current value
        expect(client_cache.insert(ctx)).toBe(true);
        let entry = client_cache.cache.get(ctx.request.ip);
        expect(entry).toHaveProperty('url');
        expect(entry).toHaveProperty('body');
        expect(entry).toHaveProperty('timestamp');
        expect(entry).toHaveProperty('method');
        expect({ ...ctx.reqeust, ...entry }).toEqual(entry);
        ctx.request.ip = "192.168.1.5";
        expect(client_cache.insert(ctx)).toBe(false);
    });
});