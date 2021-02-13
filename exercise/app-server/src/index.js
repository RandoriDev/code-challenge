const Koa = require('koa');
const bodyParser = require('koa-bodyparser');
const DelayDupli = require('./middlewares/DelayDupli');
const RejectMaliciousJSONPosts = require('./middlewares/RejectMaliciousJSONPosts');
const RequestLog = require('./middlewares/RequestLog');
const GenericService = require('./services/GenericService');

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

    // No routing, just pass everythign to this very generic backend which handles all our requests
    // indescriminantly
    app.use(GenericService.execute);

    app.listen(listenPort, () => {
      console.log(`Listening on port ${listenPort}`);
    });
  }

}

Main.run();
