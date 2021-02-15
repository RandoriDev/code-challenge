const StringUtils = require('./StringUtils');

/**
 * Utility class for event logging
 *
 * @class LogUtils
 */
class LogUtils {

  /**
   * Log a debugging message to the console.
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {string} message - Log message
   * @memberof LogUtils
   */
  static debug(ctx, message) {
    console.debug(LogUtils.__format(ctx, message));
  }

  /**
   * Log an info message to the console.
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {string} message - Log message
   * @memberof LogUtils
   */
  static info(ctx, message) {
    console.info(LogUtils.__format(ctx, message));
  }

  /**
   * Log a warning message to the console.
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {string} message - Log message
   * @memberof LogUtils
   */
  static warn(ctx, message) {
    console.warn(LogUtils.__format(ctx, message));
  }

  /**
   * Log an error message to the console.
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {string} message - Log message
   * @memberof LogUtils
   */
  static error(ctx, message) {
    console.error(LogUtils.__format(ctx, message));
  }

  /**
   * Generates a formatted log message from the Koa context and the log message.  Log entry
   * contains:
   *
   * - UTC+0 timestamp
   * - Request identifier
   * - Log message
   *
   * @static
   * @param {object} ctx - Koa context
   * @param {string} message - Log message
   * @returns
   * @memberof LogUtils
   */
  static __format(ctx, message) {
    if (ctx.__requestId === undefined) {
      // Add a "unique" ID to the context.  This ID is unique enough for the purpose of looking at
      // somewhat adjacent log entries, and correlating connection.  It's not 100% foolproof, but
      // it should be good enough.
      ctx.__requestId = StringUtils.getRandomBytes(8).toString('hex')
    }
    return `${new Date().toISOString()} (${ctx.__requestId}) - ${message}`
  }
}

module.exports = LogUtils;
