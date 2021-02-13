const assert = require('assert');
const redis = require("redis");

/**
 * Utility class for cache manipulation.
 *
 * @class CacheUtils
 */
class CacheUtils {

  /**
   * Registers a cache key prefix so that it isn't accidentally reused within the application.
   *
   * @static
   * @param {string} prefix - Cache key prefix
   * @returns The registered prefix;
   * @memberof CacheUtils
   */
  static registerPrefix(prefix) {
    assert(
      (!CacheUtils.REGISTERED_PREFIXES.has(prefix)),
      `${prefix} is already a registered cache key prefix`,
    );

    CacheUtils.REGISTERED_PREFIXES.add(prefix);

    return prefix;
  }

  /**
   * Retrieves a value from the cache, returns null if the key cannot be located.
   *
   * @static
   * @param {string} prefix - Cache key prefix
   * @param {string} key - Cache key
   * @memberof CacheUtils
   */
  static get(prefix, key) {
    const fqKey = CacheUtils.__getFQKey(prefix, key);

    // Check here before checking the cache, in order to avoid a cache miss while insertion is
    // in progress.
    if (fqKey in CacheUtils.PENDING_ENTRIES) {
      return CacheUtils.PENDING_ENTRIES[fqKey];
    }

    return new Promise((resolve, reject) => {
      CacheUtils.CLIENT.get(fqKey, (err, reply) => {
        if (err) {
          reject(err);
        } else {
          resolve(reply);
        }
      })
    });
  }

  /**
   * Writes a value to the cache.
   *
   * @static
   * @param {string} prefix - Cache key prefix
   * @param {string} key - Cache key
   * @param {*} value - Value to cache
   * @returns
   * @memberof CacheUtils
   */
  static set(prefix, key, value) {
    const fqKey = CacheUtils.__getFQKey(prefix, key);

    // Temporarily store the item so that we don't incur a cache miss prior to the data being
    // available in redis.
    CacheUtils.PENDING_ENTRIES[fqKey] = value;

    return new Promise((resolve, reject) => {
      CacheUtils.CLIENT.set(fqKey, value, err => {
        if (err) {
          reject(err);
        } else {
          resolve();
        }

        delete CacheUtils.PENDING_ENTRIES[fqKey];
      })
    });
  }

  /**
   * Asserts that a cache key prefix is registered.
   *
   * @static
   * @param {string} prefix - Cache key prefix.
   * @returns The fully qualified cache key which includes the prefix
   * @memberof CacheUtils
   */
  static __getFQKey(prefix, key) {
    assert(
      CacheUtils.REGISTERED_PREFIXES.has(prefix),
      `${prefix} is not a registered prefix`,
    );

    return `${prefix}_${key}`;
  }

}

// Maintain a collection of cache key prefixes.  If this were a larger application, this would
// eliminate accidental key collisions.
CacheUtils.REGISTERED_PREFIXES = new Set();

// Temporary storage for items being cached, until they are available on the cache at which point
// they are removed from here.
CacheUtils.PENDING_ENTRIES = {};

// Cache client
CacheUtils.CLIENT = redis.createClient({
  host: process.env.REDIS_HOST === undefined ? 'localhost' : process.env.REDIS_HOST,
});

module.exports = CacheUtils;
