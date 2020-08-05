const Router = require("@koa/router");
const validate = require('./validate');
const Cache = require("./client_cache");

const router = new Router();
const client_cache = new Cache();
/*
    validate calls call_backend so call_backend must always exist
    subsequent to validate in middleware chain
*/
router.all("/:target", validate(client_cache));


module.exports = router;