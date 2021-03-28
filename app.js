import express from 'express';
import logger from 'morgan';
import expressProxy from 'express-http-proxy';
import {rawBodyMiddleware} from './middleware/raw_body.js';
import {repeatRequestMiddleware} from './middleware/repeat_request.js';
import {BACKEND_SERVICE_URL} from './constants.js';
import {isMaliciousMiddleware} from './middleware/is_malicious.js';
import { requireContentTypeMiddleware } from './middleware/require_content_type.js';

const app = express();

app.set('trust proxy', true); 

app.use(requireContentTypeMiddleware);
app.use(rawBodyMiddleware);
app.use(isMaliciousMiddleware);
app.use(repeatRequestMiddleware);

app.use(logger('combined'));
app.use(expressProxy(BACKEND_SERVICE_URL));

export default app;