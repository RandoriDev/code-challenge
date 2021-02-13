const assert = require('assert');

/**
 * Utility class for timers.
 *
 * @class TimerUtils
 */
class TimerUtils {

  /**
   * Sleeps for n milliseconds.
   *
   * @static
   * @param {Number} nMilli - Number of milliseconds to sleep.
   * @memberof TimerUtils
   */
  static async sleep(nMilli) {
    assert(typeof(nMilli) === 'number');
    assert(nMilli >= 0);

    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve();
      }, nMilli)
    })
  }

}

module.exports = TimerUtils;
