export const isMaliciousMiddleware = (req, res, next) => {
    if (req.body.is_malicious) {
        res.sendStatus(401);
        return;
    }

    next();
};