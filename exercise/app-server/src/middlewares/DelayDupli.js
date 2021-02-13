const crypto = require('crypto');
const CacheUtils = require('../utils/CacheUtils');
const TimerUtils = require('../utils/TimerUtils');
const LogUtils = require('../utils/LogUtils');

/**
 * Middleware encapsulation which incurs a 2 second delay penalty before continuing down the
 * middleware stack, for requests from the same user which are identical to the previous received
 * request.  A duplicate request consists (for this example) of a matching combination of:
 *
 *  - Remote IP address (proxied addresses are not taken into consideration)
 *  - Path
 *  - Query string
 *  - Request body
 *
 * @class DelayDupli
 */
class DelayDupli {

  /**
   * Middleware execution method
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {*} next - Next middleware
   * @memberof DelayDupli
   */
  static async execute(ctx, next) {
    // IP address of the connected client is used as client's identity
    const ipAddress = ctx.ip;

    const prevReqHashDigest = await CacheUtils.get(
      DelayDupli.DELAY_PREFIX,
      ipAddress,
    );

    // Serialize the query string in key order so that subsequent query strings match even
    // if in different order.
    const queryString = JSON.stringify(ctx.query, Object.keys(ctx.query).sort());

    // Create an MD5 hash of the request parameters and use that as part of the cache key
    // MD5 is not secure due to collision probability, but this is not a security sensitive
    // application of the hash function, so it shouldn't pose a problem.
    let currentReqHash = crypto.createHash('md5');
    currentReqHash.update(
      [
        ctx.method,
        ctx.path,
        queryString,
      ].join('|')
    )

    if (ctx.request.rawBody !== undefined) {
      // For the sake of simplicity, we will consider bodies to be unique based purely on their
      // checksum.  We aren't worried about rearranged JSON that amounts to the same request.
      currentReqHash.update(ctx.request.rawBody)
    }
    const reqHashDigest = currentReqHash.digest("hex");

    if (prevReqHashDigest === reqHashDigest) {
      // This will throttle consecutive duplicate requests.  No provisioning is made for concurrent
      // request throttling, beyond what is implicitly available in this solution.
      LogUtils.warn(
        ctx,
        `Duplicate request detected, imposing ${DelayDupli.DUPLICATE_REQUEST_DELAY_MS}ms delay`
      );
      await TimerUtils.sleep(DelayDupli.DUPLICATE_REQUEST_DELAY_MS);
    } else {
      // Only update if the request is different from the previous
      CacheUtils.set(DelayDupli.DELAY_PREFIX, ipAddress, reqHashDigest);
    }

    await next();
  }

}

// Cache key prefix for this middleware
DelayDupli.DELAY_PREFIX = CacheUtils.registerPrefix('DELAY');

// Number of milliseconds to wait when a duplicate request from the same client arrives
DelayDupli.DUPLICATE_REQUEST_DELAY_MS = 2 * 1000;

module.exports = DelayDupli;
