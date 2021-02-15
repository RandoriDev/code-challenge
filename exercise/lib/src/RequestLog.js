const LogUtils = require('./LogUtils');

/**
 * Middleware encapsulation which logs HTTP requests before and after processing.  The following
 * information is logged:
 *
 * - Date/Time
 * - IP Address (and forwarded address if labelled as forwarded)
 * - Request method
 * - Request path / query args
 *
 * @class RequestLog
 */
class RequestLog {

  /**
   * Middleware execution method
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {*} next - Next middleware
   * @memberof RequestLog
   */
  static async execute(ctx, next) {
    const requestStart = new Date();

    // Grab the IP address from the x-forwarded-for header if it originates from behind a proxy
    // server, otherwise grab it from the connected address
    const ipAddress = ctx.ip;
    const fwded = (
      ctx.headers[RequestLog.PROXY_FORWARDED_HEADER] ?
      `(FWD ${ctx.headers[RequestLog.PROXY_FORWARDED_HEADER]}) ` :
      ''
    );

    const qs = ctx.querystring.length > 0 ? `?${ctx.querystring}` : '';
    const requestString = `${fwded}${ipAddress} - ${ctx.method} ${ctx.path}${qs}`;
    LogUtils.info(ctx, `${requestString} - Initiated`);
    const resultString = await next().then(r => "completed").catch(e => {
      ctx.status = 500;
      ctx.response.body = JSON.stringify({'status': 'ERROR'});
      LogUtils.error(ctx, e);
      return "failed"
    })
    const requestEnd = new Date();
    const duration = requestEnd.getTime() - requestStart.getTime();
    LogUtils.info(ctx, `Request ${resultString} (${duration.toFixed(0)}ms)`);
  }

}

RequestLog.PROXY_FORWARDED_HEADER = 'x-forwarded-for';

module.exports = RequestLog;
