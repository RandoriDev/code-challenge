const reqByIp = {};
export const repeatRequestMiddleware = (req, res, next) => {
    if (reqByIp[req.ip] && reqByIp[req.ip].compare(req.locals.rawBody) === 0) {
        setTimeout(() => next(), 2000);
        return;
    } 

    reqByIp[req.ip] = req.locals.rawBody;

    next();
};