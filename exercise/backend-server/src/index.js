const Koa = require('koa');
const { RequestLog } = require('lib');
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
    const listenPort = process.env.PORT === undefined ? 8089 : parseInt(process.env.PORT);

    // Middleware chain
    app.use(RequestLog.execute);

    // No routing, just pass everythign to this very generic backend which handles all our requests
    // indescriminantly
    app.use(GenericService.execute);

    app.listen(listenPort, () => {
      console.log(`Listening on port ${listenPort}`);
    });
  }

}

Main.run();
