/**
 * 
 * Express middleware to handle and reject malicious requests
 */
export const isMaliciousMiddleware = (req, res, next) => {
    if (req.method === 'POST' && req.locals.body.is_malicious) {
        res.sendStatus(401);
        return;
    }

    next();
};