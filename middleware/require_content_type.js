/**
 * 
 * Express middleware to enforce the existance of a content-type header
 */
export const requireContentTypeMiddleware = (req, res, next) => {
    if (!req.headers['content-type']) {
        res.sendStatus(415);
        return;
    }
    next();
}
