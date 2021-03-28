import express from 'express';

/**
 * Express middleware to parse body and store both parsed and raw body.
 */
export const rawBodyMiddleware = express.raw({
    type: '*/*',
    verify: (req, _, buf) => {
        req.locals = req.locals || {};
        if (req.headers['content-type'] === 'application/json') {
            req.locals.jsonBody = JSON.parse(buf.toString());
            req.locals.rawBody = buf;
        }
    }
});