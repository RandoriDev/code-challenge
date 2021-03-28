/**
 * 
 * Express middleware to handle and reject malicious requests
 */
export const isMaliciousMiddleware = (req, res, next) => {
    if (req.method === 'POST' && req.locals && req.locals.jsonBody && req.locals.jsonBody.is_malicious) {
        res.sendStatus(401);
        return;
    }

    next();
};