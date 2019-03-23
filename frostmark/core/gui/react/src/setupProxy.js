const proxy = require('http-proxy-middleware');


function proxyRequest(app) {
    app.use(
        proxy('/api', {
            target: process.env.REACT_PROXY,

            // don't proxy websockets
            ws: false
        })
    );
};


module.exports = proxyRequest;
