import express from 'express';
import logger from 'morgan';
import {RootRouter} from './routes/index.js';
import {rawBodyMiddleware} from './middleware/raw_body.js';
import {repeatRequestMiddleware} from './middleware/repeat_request.js';

const app = express();

app.set('trust proxy', true); 

app.use(logger('dev'));
app.use(rawBodyMiddleware);
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(repeatRequestMiddleware);

app.use('/', RootRouter);

export default app;