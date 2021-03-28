export const isMaliciousMiddleware = (req, res, next) => {
    if (req.method === 'POST' && req.body.is_malicious) {
        res.sendStatus(401);
        return;
    }

    next();
};