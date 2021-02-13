const Koa = require('koa');
const proxy = require('koa-proxy');
const bodyParser = require('koa-bodyparser');
const DelayDupli = require('./middlewares/DelayDupli');
const RejectMaliciousJSONPosts = require('./middlewares/RejectMaliciousJSONPosts');
const { RequestLog } = require('lib');

class Main {

  /**
   * Main execution method
   *
   * @static
   * @memberof Main
   */
  static run() {
    const app = new Koa();
    const listenPort = process.env.PORT === undefined ? 8088 : parseInt(process.env.PORT);
    const backendHostname = process.env.BACKEND_SERVER_HOSTNAME === undefined ? 'localhost' : process.env.BACKEND_SERVER_HOSTNAME;
    const backendPort = process.env.BACKEND_SERVER_PORT === undefined ? 8089 : parseInt(process.env.BACKEND_SERVER_PORT)

    // Middleware chain
    app.use(RequestLog.execute);

    // Parses JSON / forms when available (on all endpoints), limit to 50kb payloads
    app.use(bodyParser({
      enableTypes: ['json', 'form'],
      jsonLimit: '50kb',
      formLimit: '50kb',
    }));

    app.use(RejectMaliciousJSONPosts.execute);
    app.use(DelayDupli.execute);
    app.use(proxy({
      host: `http://${backendHostname}:${backendPort}`,
      jar: true,    // Enable cookie forwarding
    }));

    app.listen(listenPort, () => {
      console.log(`Listening on port ${listenPort}`);
    });
  }

}

Main.run();
