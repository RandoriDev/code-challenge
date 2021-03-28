const reqByIp = {};

/**
 * 
 * Express middleware to handle throttling repeat requests. Currently only
 * testing request body for uniqueness but could easily be expanded to include 
 * method and headers as well. 
 * 
 * Note: Currently uses remote ip address to define a 'client'. This will catch
 * false positives if two clients send identical requests behind NAT. 
 */
export const repeatRequestMiddleware = (req, res, next) => {
    if (reqByIp[req.ip] && reqByIp[req.ip].compare(req.locals.rawBody) === 0) {
        setTimeout(() => next(), 2000);
        return;
    } 

    reqByIp[req.ip] = req.locals.rawBody;

    next();
};