import express from 'express';

/**
 * Express middleware to parse body and store both parsed and raw body.
 */
export const rawBodyMiddleware = express.raw({
    type: 'application/json',
    verify: (req, _, buf) => {
        req.locals = req.locals || {};
        req.locals.rawBody = buf;
        req.locals.body = JSON.parse(buf.toString());
    }
});