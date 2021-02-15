const { LogUtils } = require('lib');

/**
 * Service which responds generically to any HTTP request.  It performs no validation but
 * merely handles traffic according to HTTP request method.  All responses are serialized JSON,
 * and all responses carry a 'status' key in the payload.  Valid statuses are 'OK', and 'ERROR'.
 *
 * @class GenericService
 */
class GenericService {

  /**
   * Processes an HTTP request and returns a response according to the request method.  See
   * HTTP method type specific handlers below.
   *
   * @static
   * @param {*} ctx
   * @memberof GenericService
   */
  static async execute(ctx) {
    const method = ctx.method;
    let handlerParts;
    if (method in GenericService.METHOD_TO_HANDLER_AND_DEFAULT_RESPONSE) {
      handlerParts = GenericService.METHOD_TO_HANDLER_AND_DEFAULT_RESPONSE[method];
    } else {
      handlerParts = [GenericService.doOther, 200];
    }

    const [ handler, defaultResponseStatus ] = handlerParts;

    ctx.response.type = 'application/json';
    const [ result, error ] = await handler(ctx).then(r => [r, null]).catch(e => [null, e]);
    if (error !== null) {
      // For the sake of this example, we're assuming that all errors are a result of a bad request
      LogUtils.error(ctx, error);

      ctx.status = 400;
      ctx.response.body = JSON.stringify({
        'status': 'ERROR',
      });
    } else {
      ctx.status = defaultResponseStatus;
      ctx.response.body = JSON.stringify(result);
    }
  }

  /**
   * Handles a GET request, returns a response containing:
   *
   * {
   *    message: <pleasent response message>,
   *    status: <response status indicator>,
   * }
   *
   * @static
   * @param {object} ctx - Koa context
   * @returns
   * @memberof GenericService
   */
  static async doGet(ctx) {
    return {
      message: `Have a number happy customer: ${Math.floor(Math.random() * 100000)}`,
      status: 'OK',
    }
  }

  /**
   * Handles a POST request, returns a response containing:
   *
   * {
   *    id: <id of the mock created object>,
   *    status: <response status indicator>,
   * }
   *
   * @static
   * @param {object} ctx - Koa context
   * @returns
   * @memberof GenericService
   */
  static async doPost(ctx) {
    // Assume an object was created, set the response type accordingly
    return {
      id: GenericService.SERIAL ++,
      status: 'OK',
    }
  }

  /**
   * Handles a PUT request, returns a response containing:
   *
   * {
   *    status: <response status indicator>,
   * }
   *
   * @static
   * @param {object} ctx - Koa context
   * @returns
   * @memberof GenericService
   */
  static async doPut(ctx) {
    return {
      status: 'OK',
    }
  }

  /**
   * Handles a DELETE request, returns a response containing:
   *
   * {
   *    status: <response status indicator>,
   * }
   *
   * @static
   * @param {object} ctx - Koa context
   * @returns
   * @memberof GenericService
   */
  static async doDelete(ctx) {
    return {
      status: 'OK',
    }
  }

  /**
   * Handles response for any HTTP method not found in
   * GenericService.METHOD_TO_HANDLER_AND_DEFAULT_RESPONSE request, returns a response containing:
   *
   * {
   *    status: <response status indicator>,
   * }
   *
   * @static
   * @param {object} ctx - Koa context
   * @returns
   * @memberof GenericService
   */
  static async doOther(ctx) {
    return {
      status: 'OK',
    }
  }
}

// Mapping from HTTP method to service handler and default response code
GenericService.METHOD_TO_HANDLER_AND_DEFAULT_RESPONSE = Object.fromEntries([
  ['GET', [GenericService.doGet, 200]],
  ['POST', [GenericService.doPost, 201]],
  ['PUT', [GenericService.doPut, 200]],
  ['DELETE', [GenericService.doDelete, 200]],
]);

// Counter which increments after each create operation
GenericService.SERIAL = 1;

// Ok status (associated with a successful request)
GenericService.STATUS_OK = 'OK';

// Error status (associated with a failed request)
GenericService.STATUS_ERROR = 'ERROR';

module.exports = GenericService;
