import { WS_ADDRESS } from '../configs';

function useWebSocket (handleOpen, handleMessage) {
    console.log(WS_ADDRESS)
    const ws = new WebSocket(WS_ADDRESS);

    const init = () => {        
        bindEvent()
    }
    
    function bindEvent () {
        ws.addEventListener('open', handleOpen, false);
        ws.addEventListener('close', handleClose, false);
        ws.addEventListener('error', handleError, false);
        ws.addEventListener('message', handleMessage, false);
    }

    function handleClose(e) {
        console.log('WebSocket close', e);
    }

    function handleError(e) {
        console.log('WebSocket error', e);
    }

    init();

    return ws;
}

export default useWebSocket;