$(function () {
    const POST_URL = document.location.protocol+ "//" + document.location.hostname + ":5000"; 
    const AVATAR_USER = "img/avatar_user.png";
    const AVATAR_BOT  = "img/avatar_bot.png";
        // document.location.protocol + "//" + document.location.hostname + ":5000/chat"; 
        //"/chat"
    const MAIN = document.querySelector('main');
    const $INPUT = $('#btn-input');
    const $TIMER = $('#timer');

    let IDLE_TIME = 0;
    const MAX_IDLE_TIME = 600; //300; // === 5 minutes
    let _TIMER = null;
    const _TIMER_LAPSE = 1000;

    const _TIMER_START = function () {
            _TIMER_END();
            _TIMER = setInterval(function (){
                IDLE_TIME += 1;
                _setTimer();
                if (IDLE_TIME >= MAX_IDLE_TIME) {
                    sendMessage( true );
                    _TIMER_END();
                }
            }, _TIMER_LAPSE);
        };
    var _TIMER_END = function () {
            if (_TIMER) {
                IDLE_TIME = 0;
                clearInterval( _TIMER );
                _TIMER = null;
                _setTimer();
            }  
        };

    var _setTimer = function (){
        $TIMER.text(MAX_IDLE_TIME - IDLE_TIME);
    }

    function getTime () {
        return new Date().toLocaleTimeString("es-ES",{timeStyle: "short"})
    }
    
    function addMessageBot (o) { // { answer, icons, conversation_ended, name }
        const msg =   o.answer || [''];
        const icons = o.icons || [];
        const result = ['<li class="left clearfix">'+
                      '    <span class="chat-img pull-left">'+
                      '        <img src="'+ AVATAR_BOT +'" alt="Bot Avatar" class="img-circle" />'+
                      '    </span>'+
                      '    <div class="chat-body clearfix">'+
                      '        <div class="header">'+
                      '            <strong class="primary-font">AOD Chat</strong>'+
                      '            <small class="pull-right text-muted">'+
                      '               <span class="glyphicon glyphicon-time"></span>'+ getTime() +
                      '            </small>'+
                      '        </div>'
                    ];
    
        if (icons.length > 0){
            result.push(icons.map(function (icon, index){
                return  '<div class="weather">'+
                        '    <pre>'+ msg[index] +'</pre>'+
                        '    <img alt="weather" src="static/'+ icon +'">'+
                        '</div>';
                }).join(''));
        } else {
            result.push(msg.map(function (msg) {
                return '<pre>' + linkifyHtml(msg, {
                    attributes (href){
                        return {
                            title: href
                        };
                    },
                    format (value, type) {
                        if (type === 'url' && value.length > 45) {
                            value = 'link';
                        }
                        return value;
                    }
                }) + '</pre>'
            }).join(''));
        }
        if (o.conversation_ended){
            result.push(addScore(o.session_id))
        }
        result.push('</div></li>');
        return result.join('');
    }
    
    function addMessageUser (o) { // { name, msg }
        return  '<li class="right clearfix">'+
                '    <span class="chat-img pull-right">'+
                '        <img src="'+ AVATAR_USER +'" alt="User Avatar" class="img-circle" id="msg-user"/>'+
                '    </span>'+
                '    <div class="chat-body clearfix">'+
                '        <div class="header">'+
                '            <small class=" text-muted">'+
                '                <span class="glyphicon glyphicon-time"></span>'+ getTime() +
                '            </small>'+
                '            <strong class="pull-right primary-font">Usuario</strong>'+
                '        </div>'+
                '        <p>'+ o.msg +'</p>'+
                '    </div>'+
                '</li>';
    }
    function addScore (session_id) {
        return  '<div class="text-center" style="margin-bottom:1em">'+
                '    <div class="btn-group" role="group" aria-label="..." id="score_'+ session_id +'" data-sessionid="'+ session_id +'">'+
                '       <button type="button" class="btn btn-success" data-value="10">Buena</button>'+
                '       <button type="button" class="btn btn-info"    data-value="0">Normal</button>'+
                '       <button type="button" class="btn btn-danger"  data-value="-10">Mala</button>'+
                '    </div>'+
                '</div>';
    }

    function addEndConversation (withTxt){
        return  withTxt
                ?   '<div class="text-center">'+
                    '    <h3>Fin de conversación</h3>'+
                    '    <hr />'+
                    '    <h4>Nueva conversación</h4>'+
                    '</div>'
                : '';
    }

    const $input = $('#btn-input')
        .on('keypress', function (e){
            if (e.keyCode === 13) // INTRO key
              { sendMessage(); }
        });

    $('#btn-chat').on('click', function (){
        sendMessage();
    });

    var sendMessage = function ( endChat ) {
        let value = $input.val();
        if (endChat) {
            value = "adios"
        }
        if (value !== ""){
            // enviar al servidor
            $.ajax({
                method: "POST",
                url: POST_URL+ '/chat', 
                data: JSON.stringify({ 
                    "text": value,
                    "timeout": endChat || false
                }),
                dataType: "json",
                contentType: 'application/json;charset=UTF-8',
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true
            })
            .then(function (json){
                if (json.name && json.name !== name) {
                    name = json.name;
                }
                const isEND = json.conversation_ended;
                appendMessage(addMessageBot(json) + addEndConversation(isEND));

                // por si existe, pongo evento único de enviar score
                $('#score_'+ json.session_id ).one('click', sendScore);

                if (isEND) {
                    _TIMER_END();
                } else {
                    _TIMER_START();
                }
            });
            // el valor lo escriba directamente en el chat
            if (!endChat){
                appendMessage(addMessageUser({ name, msg: value }));
            }
        }
    };

    var sendScore = function (event) {
        const $BUTTON = $(event.target);
        const session_id = $(this).data('sessionid');
        const value = parseInt($BUTTON.data('value'));
        $(this).children().hide();
        $.ajax({
            method: "POST",
            url: POST_URL+ '/score',
            data: JSON.stringify({
                "score": value,
                session_id
            }),
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true
        })
        .then(function (json){
            console.warn(json);
            $BUTTON.show().prop('disabled', true);
        })
    }

    var appendMessage = function (msg) {
        $("#messages").append(msg);
        // scroll To bottom...
        MAIN.scrollTop = MAIN.scrollHeight;
        $INPUT.val('').focus();
    }
    
    appendMessage(addMessageBot({
        answer: ["Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los " +
        "datos abiertos que dispongo. ¿en qué puedo ayudarte?"],
        icons: []
    }));
});
