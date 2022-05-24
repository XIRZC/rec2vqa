const WebSocket = require('ws');

;((Ws) => {

    const server  = new Ws.Server({ port: 8000 });

    const init = () => {
        bindEvent()
    }

    function bindEvent() {
        server.on('open', handleOpen);
        server.on('close', handleClose);
        server.on('error', handleError);
        server.on('connection', handleConnection);
    }

    function handleOpen (e) {
        console.log('WebSocket Open')
    }

    function handleClose (e) {
        console.log('WebSocket close')
    }

    function handleError (e) {
        console.log('WebSocket error')
    }

    function handleConnection (ws) {
        console.log('WebSocket Connection');
        ws.on('message', handleMessage)
    }

    function handleMessage (msg) {
        console.log(JSON.parse(msg))
    }

    init()
})(WebSocket)