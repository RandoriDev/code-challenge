import express from 'express';
import logger from 'morgan';
import {RootRouter} from './routes/index.js';
import {rawBodyMiddleware} from './middleware/raw_body.js';

const app = express();

app.use(logger('dev'));
app.use(rawBodyMiddleware);
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/', RootRouter);

export default app;