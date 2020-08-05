const BACKEND_BASE_URL = `https://backend/`;
const CALL_DELAY = 2000;
/*
    call_backend: calls backend with full request and returns response 
    from server.

    - optional delay_by param to delay call to backend by x ms
*/
async function call_backend(ctx, delay = false) {
    //if delay set, delay call to backend by time
    if (delay === true) {
        console.log(`\nDelaying call to backend by ${CALL_DELAY}`);
        await sleep(CALL_DELAY);
    }
    //simulate async call
    try {
        const response = await send(ctx);
        console.log(`\nRequest to server returned with status: ${response.status}`);
        //return response/status from server to user
        ctx.status = response.status;
        ctx.body = response.body;
    } catch (e) {
        console.log(`\nError forwarding request to server`, e);
    }
}
/*
    send: send request to backend service and return the response
    -  takes koa ctx as param
*/
async function send(ctx) {
    //model an identical request from context
    const url = BACKEND_BASE_URL + ctx.url;
    const request = {
        method: ctx.method,
        headers: {
            "Content-Type": "application/json",
            authorization: ctx.headers.authorization
        }
    };
    //add body on non GET calls where body is present
    if (ctx.request.body && ctx.method !== "GET") {
        request.body = ctx.request.body;
    }
    console.log(`\nForwarding request ${url}:`, request);
    //here we would await fetch(request) in real scenario
    return new Promise(resolve => setTimeout(resolve({ body: request.body ? request.body : "OK", status: 200 }), 200));
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = call_backend;