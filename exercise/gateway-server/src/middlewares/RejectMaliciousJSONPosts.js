const { LogUtils } = require('lib');

/**
 * Middlewhere encapsulation which rejects POST requests containing JSON payloads which contain a
 * key named "is_malicious".
 *
 * @class RejectMaliciousJSONPosts
 */
class RejectMaliciousJSONPosts {

  /**
   * Middleware execution method
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {*} next - Next middleware
   * @returns
   * @memberof RejectMaliciousJSONPosts
   */
  static async execute(ctx, next) {
    const contentTypeHeader = ctx.headers[RejectMaliciousJSONPosts.CONTENT_TYPE_HEADER];
    if (
      ctx.method === RejectMaliciousJSONPosts.POST_METHOD &&
      contentTypeHeader !== undefined &&
      contentTypeHeader.toLowerCase() === RejectMaliciousJSONPosts.JSON_CONTENT_TYPE &&
      typeof(ctx.request.rawBody) === 'string',
      RejectMaliciousJSONPosts.MALICIOUS_KEY_RE.exec(ctx.request.rawBody) !== null
    ) {
      // We have a malicious piece of JSON, return a 400 immediately
      LogUtils.warn(ctx, `Malcious payload detected from ${ctx.ip}`);
      ctx.status = 401;
      return;
    }

    await next();
  }

}

RejectMaliciousJSONPosts.POST_METHOD = 'POST';
RejectMaliciousJSONPosts.CONTENT_TYPE_HEADER = 'content-type';
RejectMaliciousJSONPosts.JSON_CONTENT_TYPE = 'application/json';
RejectMaliciousJSONPosts.MALICIOUS_KEY_RE = /"is_malicious"[\r\n\s]*:[\r\n\s]*"is_malicious"/;

module.exports = RejectMaliciousJSONPosts;
