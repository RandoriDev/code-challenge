/* 
    cache to store last request key'd by client_id
    to run validation against incoming requests

    we check last request for client and
    return true from insert if the received request
    has the same endpoint and method as the previous request

*/
function Cache() {
    this.cache = new Map();
}
//create entry for cache
Cache.prototype.create_entry = function (ctx) {
    const { url, method, body } = ctx.request;
    return {
        url,
        method,
        body,
        timestamp: new Date().getTime()
    }
}
//insert cache entry by client ip
Cache.prototype.insert = function (ctx) {
    //validate current request against existing entry per client_ip
    let validate = (entry) => {
        /*
            I wasn't sure if it was desired to compare the body content in order to classify as "exact same request"
            but that would be easy to add here... JSON.stringify(request.body) === JSON.stringify(entry.body)

            If this is modeling a simple DOS attack, my intuition is that it is better to simply look at the method/url 
        */
        return entry.url === ctx.request.url && entry.method === ctx.request.method;
    }
    const client_ip = ctx.request.ip;
    const entry = this.create_entry(ctx);
    let do_wait = false;
    if (this.cache.has(client_ip)) {
        do_wait = validate(this.cache.get(client_ip));
    }
    console.log(`\nInserting to cache for ${client_ip}\n --- wait triggered: ${do_wait}\n --- cache entry:`, entry);
    this.cache.set(client_ip, entry);
    return do_wait;
}

module.exports = Cache;
