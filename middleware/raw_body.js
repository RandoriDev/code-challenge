import express from 'express';

export const rawBodyMiddleware = express.raw({
    type: 'application/json',
    verify: (req, _, buf) => {
        req.locals = req.locals || {};
        req.locals.rawBody = buf
    }
});