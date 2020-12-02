import io from 'socket.io-client'

// const { endpoint } = require('@/package')
// const socket = io(pkg.endpoint.websocket/*process.env.WS_URL*//*, {
//         transports: ['polling']
//     }*/);
// const dev = (process.env.NODE_ENV !== 'production');
// const HOSTNAME = dev
//         ? window.location.hostname // endpoint.HOST_dev <= "193.144.225.63" (Alvaro)
//         : window.location.hostname
//         ;
//
// dev  => http://193.144.225.63:5008
// prod => http://hostname:5008
//
const socket = io( process.env.urlSocket );
export default socket
