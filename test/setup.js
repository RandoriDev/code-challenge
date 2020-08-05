let server = require('../src/server');
function setup() {
    let app = server;
    if (!app) {
        console.log('Failed to get server');
    } else {
        return app;
    }
}

module.exports = setup;