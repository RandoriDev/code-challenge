/*
 * Really simple test client which prods the server.  No concurrency, just a simple neverending
 * loop.  Not a full coverage test of the server, and intentionally not methodical.  Just a
 * demonstration.
 */

const fetch = require('node-fetch');
const querystring = require('querystring');
const assert = require('assert');

const HOSTNAME = process.env['TARGET_HOSTNAME'] === undefined ? 'localhost' : process.env['TARGET_HOSTNAME'];
const PORT = process.env['TARGET_PORT'] === undefined ? 8088 : parseInt(process.env['TARGET_PORT']);
const URL = `http://${HOSTNAME}:${PORT}`;

const names = [
  'bird',
  'dog',
  'cat',
  'car',
];

const queryArgs = [
  'sort',
  'pageNum',
  'pageSize',
];

const maliciousBodies = [
  '{"is_malicious": "is_malicious"}',
  '  {  "is_malicious"  :   "is_malicious"       }',
  '["hello there", { "is_malicious" : "is_malicious" }  ] ',
  '["hello there", { \n\n"is_malicious" \n: "is_malicious" }  ] ',
];

const nonMalciousBodies = [
  '{"is_malicious": "Nope"}',
  '  {  "is_malicious"  :   false       }',
  '["hello there", { "is_malicious" : [ "no" ] }  ] ',
  '["hello there", { \n\n"is_malicious" \n: "probably not" }  ] ',
  '{"Nope": "is_malicious"}',
  '  {  "hello"  :   "is_malicious"       }',
];

// Make sure these are all valid
maliciousBodies.forEach(body => JSON.parse(body))

let prevRequestHash = null
let curRequestHash = null;

/**
 * Generates a URL to our application server with a random path length
 *
 * @returns string - Random URL to our application server
 */
const randoUrl = () => {
  const url = [
    URL,
    ...names.slice(0, Math.floor(Math.random() * names.length))
  ].join('/');

  const query = {};
  queryArgs.slice(0, Math.floor(Math.random() * queryArgs.length)).forEach(queryArg => {
    query[queryArg] = Math.ceil(Math.random() * 100)
  });

  // Return the url with query args
  if (Object.keys(query).length > 0) {
    return `${url}?${querystring.encode(query)}`;
  }

  return url;
}

const sleep = (nMsec) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => resolve(), nMsec);
  })
}

/**
 * Initiates a POST request to our application server.  Some posts contain malcious data,
 * some don't.  Depends on random variable.
 * Returns a promise.
 */
const doPost = (requestURL, isMalicious) => {
  const options = {
    method: 'POST',
  }
  options.headers = {
    'Content-Type': 'application/json',
  }

  if (isMalicious === true) {
    console.warn("Sending a malicious request :)");

    options.body = maliciousBodies[Math.floor(Math.random() * maliciousBodies.length)];
  } else {
    options.body = nonMalciousBodies[Math.floor(Math.random() * nonMalciousBodies.length)];
  }

  curRequestHash = [
    'POST',
    requestURL,
    options.body
  ].join('|');

  return fetch(requestURL, options);
}

/**
 * Initiates a GET request to our application server.
 * Returns a promise.
 */
const doGet = (requestURL) => {
  curRequestHash = [
    'GET',
    requestURL,
  ].join('|');

  return fetch(requestURL, {method: "GET"});
}

// This is the main loop, keeps firing requests to the application server in order to demonstrate
// the server's response.
(async () => {
  let url = randoUrl();
  let isGet = true;
  while(true) {
    // 70% chance of getting a random path/url
    if (Math.random() < 0.80) {
      url = randoUrl();
      isGet = Math.random() < 0.5;
    }

    let isMalicious;
    if (isGet === true) {
      isMalicious = false;
    } else {
      isMalicious = Math.random() < 1/4;
    }

    console.log("Sending request")
    const startTime = new Date().getTime();
    const method = isGet === true ? doGet : doPost;
    const [
      response,
      error
    ] = await method(url, isMalicious).then(r => [r, null]).catch(e => [null, e]);
    if (error) {
      console.error(error);
    } else {
      const [ data, jsonError ] = await response.json().then(r => [r, null]).catch(e => [null, e]);
      if (jsonError) {
        console.error(jsonError)
      } else {
        console.log(data);
      }
    }
    const endTime = new Date().getTime();

    if (isMalicious === true) {
      assert(response.status === 401)
    } else {
      assert(200 <= response.status < 300);
    }

    const duration = endTime - startTime;
    if (curRequestHash === prevRequestHash && isMalicious === false) {
      assert(duration > 2000, `Time was too quick for a duplicate request ${duration}ms`);
    } else {
      assert(duration < 300, `Time was too slow for a non-duplicate request ${duration}ms`);
    }

    prevRequestHash = curRequestHash;
    // Wait a second in between requests, just to avoid bombarding the logs in an unreadible way
    await sleep(1000);
  }
 })().catch(e => {
   console.error(e);
 })
