/*
 * Really simple test client which prods the server.  No concurrency, just a simple neverending
 * loop.  Not a full coverage test of the server, and intentionally not methodical.  Just a
 * demonstration.
 */

const fetch = require('node-fetch');
const querystring = require('querystring');

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
  '{"is_malicious": true}',
  '  {  "is_malicious"  :   "person"       }',
  '["hello there", { "is_malicious" : "yup" }  ] ',
  '["hello there", { \n\n"is_malicious" \n: "yup" }  ] ',
];

// Make sure these are all valid
maliciousBodies.forEach(body => JSON.parse(body))

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
const doPost = (requestURL) => {
  const isMalicious = Math.random() < 1/4;

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
    options.body = JSON.stringify({
      'some key': 'some value'
    });
  }

  return fetch(requestURL, options);
}

/**
 * Initiates a GET request to our application server.
 * Returns a promise.
 */
const doGet = (requestURL) => {
  return fetch(requestURL, {method: "GET"});
}

// This is the main loop, keeps firing requests to the application server in order to demonstrate
// the server's response.
(async () => {
  let url = randoUrl();
  let isGet = true;
  while(true) {
    let prevMatches;

    // 70% chance of getting a random path/url
    if (Math.random() < 0.80) {
      const newUrl = randoUrl();
      const newIsGet = Math.random() < 0.5;
      prevMatches = (newUrl === url && newIsGet === isGet);
      url = newUrl;
      isGet = newIsGet;

    } else {
      prevMatches = true;
    }

    if (prevMatches) {
      console.log("About to issue a request that matches the previous one");
    } else {
      console.log("About to issue a request");
    }

    const method = isGet === true ? doGet : doPost;
    const [
      response,
      error
    ] = await method(url).then(r => [r, null]).catch(e => [null, e]);
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

    // Wait a second in between requests, just to avoid bombarding the logs in an unreadible way
    await sleep(1000);
  }
 })();
