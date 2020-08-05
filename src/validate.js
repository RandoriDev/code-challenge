
const call_backend = require('./backend_proxy');
/*
    validate incoming requests
    - declared with cache param curried so we can set that in router with global cache
    
    looks for is_malicious=true set on request body of a POST request, return 401 if true
    checks client cache for request then calls next with result 
*/
const validate = (cache) => async (ctx, next) => {
    if (ctx.method === 'POST' && ctx.request.body && ctx.request.body.is_malicious) {
        console.log(`\nReceived malicious: returning unauthorized`, ctx.request);
        ctx.status = 401;
        return;
    } else {
        console.log(`\nReceived valid request: forwarding to server`, ctx.request);
        await call_backend(ctx, cache.insert(ctx));
    }
    await next();
}

module.exports = validate;