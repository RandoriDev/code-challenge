const Koa = require("koa");
const router = require("./router");
const bodyParser = require("koa-bodyparser");
const app = new Koa();
//set up app with body parser middleware and inject routes
app.use(bodyParser());
app.use(router.routes());
//set port and export main app listener
const PORT = 8080;
console.log(`Starting Randori Test Server on port: ${8080}`);
module.exports = app.listen(PORT);
