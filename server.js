

const http = require('http')
const crypto = require('crypto')

const targetHostname = 'localhost'
const targetPort = 80
const listenPort = 8080

function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    let rawData = ''
    req.on('data', (chunk) => {
      rawData += chunk
    })
    req.on('end', () => {
      resolve(rawData)
    })
    req.on('error', (err) => {
      reject({
        statusCode: 400,
      })
    })
  })
}

async function maliciousCheck(rawData) {
  let data
  try {
    data = JSON.parse(rawData)
  } catch {
    throw {
      statusCode: 400,
    }
  }
  if (data.is_malicious) {
    throw {
      statusCode: 401,
    }
  }
}

const recentRequests = {}

async function delayDuplicates(remoteAddress, hash) {
  const lastRequestHash = recentRequests[remoteAddress]
  recentRequests[remoteAddress] = hash
  if (lastRequestHash === hash) {
    return new Promise((resolve) => {
      setTimeout(() => resolve(), 2000)
    })
  }
}

async function proxyRequest(hostname, port, headers, rawData, res) {
  const proxyReq = http.request({
    hostname: hostname,
    port: port,
    method: 'POST',
    headers: headers,
  }, (proxyRes) => {
    Object.keys(proxyRes.headers).forEach((name) => {
      res.setHeader(name, proxyRes.headers[name])
    })
    res.statusCode = proxyRes.statusCode
    proxyRes.pipe(res)
  })
  proxyReq.write(rawData)
  proxyReq.end()
}

async function requestListener (req, res) {
  const remoteAddress = res.socket.remoteAddress
  let rawData
  try {
    rawData = await readRequestBody(req)
    await maliciousCheck(rawData)
    const hash = crypto.createHash('md5').update(rawData).digest('hex').toString()
    await delayDuplicates(remoteAddress, hash)
  } catch (err) {
    if (err.statusCode) {
      res.statusCode = err.statusCode
      res.end()
      console.error(`${new Date().toISOString()} Failed request from ${remoteAddress}. Error code ${err.statusCode}`)
    } else{
      console.error(err)
    }
    return
  }
  try {
    await proxyRequest(targetHostname, targetPort, req.headers, rawData, res)
  } catch (err) {
    console.error(err)
  }
  console.log(`${new Date().toISOString()} Proxied request from ${remoteAddress}`)
}

const server = http.createServer(requestListener);
server.listen(listenPort)
