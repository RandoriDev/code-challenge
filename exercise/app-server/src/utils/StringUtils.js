/**
 * String manipulation utility class
 *
 * @class StringUtils
 */
class StringUtils {

  /**
   * Returns a Buffer containing n cryptographically unsecure pseudo random bytes of data.
   *
   * @static
   * @param {number} nBytes - Number of random bytes to generate
   * @returns A buffer of n pseudo random bytes of data.
   * @memberof StringUtils
   */
  static getRandomBytes(nBytes) {
    const buffer = Buffer.alloc(nBytes);

    let randomNum;
    for (let index = 0; index < nBytes; index++) {
      // 6 * 8 = 48 (utilize the full 48 bits that are evenly divisible by 8,
      // just under our 53 bit limit)
      const shiftOffset = index % 6;
      if (shiftOffset === 0) {
        // Bring the floating point value into the integer domain by multiplying by 2 ^ 52
        randomNum = Math.random() * (2 ** 52);
      }

      // Shift right and mask in order to capture the next byte of data
      buffer[index] = (randomNum >> (shiftOffset * 8)) & (255);
    }

    return buffer;
  }

}

module.exports = StringUtils;
