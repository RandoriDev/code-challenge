import express from 'express';
import {isMaliciousMiddleware} from '../middleware/is_malicious.js';

const router = express.Router();

router.get('*', function(req, res, next) {
  res.json({status: 'success'});
});

router.post('*', [isMaliciousMiddleware, function(req, res, next) {
  res.json({status: 'success'});
}]);

export const RootRouter = router;