$(function () {

    var POST_URL = "";
    var AVATAR_USER = "static/img/avatar_user.png";
    var AVATAR_BOT  = "static/img/avatar_bot.png";
        // document.location.protocol + "//" + document.location.hostname + ":5000/chat";
        //"/chat"
    var MAIN = document.querySelector('main');
    var $INPUT = $('#btn-input');
    var $TIMER = $('#timer');

    var IDLE_TIME = 0;
    var MAX_IDLE_TIME = 60; //300; // === 5 minutes
    var _TIMER = null;
    var _TIMER_LAPSE = 1000;

    var _TIMER_START = function () {
            _TIMER_END();
            _TIMER = setInterval(function(){
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

    var _setTimer = function(){
        $TIMER.text(MAX_IDLE_TIME - IDLE_TIME);
    };

    function getTime() {
        return new Date().toLocaleTimeString("es-ES",{timeStyle: "short"})
    }

    function addMessageBot(o) { // { answer, icons, conversation_ended, name }
        var msg =   o.answer || [''];
        var icons = o.icons  || [];
        var buttons = o.buttons  || [];

        $('#status').text("Escriba su mensaje aquí:")
        $('#btn-input').prop('disabled', false);
        $('#btn-chat').prop('disabled', false);
        $("body").css("cursor", "default");

            var result = ['<li class="pull-right clearfix">'+
                      '    <div class="chat-img float-left">'+
                      '        <img src="'+ AVATAR_BOT +'" alt="Bot Avatar" class="img-circle"  style="margin-right: 4px" />'+
                      '        <div class="float-right"><strong class="primary-font">AOD Chat</strong><small><span class="glyphicon glyphicon-time"></span>'+ getTime() + '</small>'+
                      '        </div>'+
                      '    </div>'+
                      '    <p class="chat-body float-none"><br><br>'
                    ];


        if (icons.length > 0){
            result.push(icons.map(function(icon, index){
                return  '<div class="weather">'+
                        '    <pre>'+ msg[index] +'</pre>'+
                        '    <img alt="weather" src="'+ icon +'">'+
                        '</div>';
                }).join(''));
        } else {
            result.push(msg.map(function (msg) {
                if (msg== "Adios. Por favor valore la experiencia.") {
                    sendMessage(true);
                    return;
                }

                lines = msg.split("\n");
                if (lines.length > 3 && lines[1].split(": ").length > 1 && lines[2].split(": ").length > 1 ) { // tabla
                    resp = "<div class='container  float-left'>"
                   /* resp +='<pre>' + lines[0] + "</pre>";*/
                    resp += "<caption>Datos de la entidad</caption>";
                    resp += "<table class='table table-striped table-bordered table-sm col-12 col-lg-6' style='font-size:14px'>";

                    resp += "<thead><tr><th scope='col'>Nombre</th><th scope='col'>Dato</th></tr></thead>";
                    i=0
                    for(;i<lines.length;i++) {
                        pos = lines[i].indexOf(":");
                        if (pos!=-1) {
                            if (lines[i].split(":")[1].length == 0 ) break;
                            resp += "<tr><td>" + lines[i].substring(0,pos+1)+"</td>";
                            resp += "<td>";
                            if (lines[i].substring(pos+2).indexOf("http://opendata.aragon.es/def/ei2a#")!==-1) {
                                payload  = "/engagement.subject{\"subject_type\": \""+lines[i].substring(pos+2)+"\"}";
                                resp +=  '<div  aria-label="Acciones" class="fallback_'+ o.session_id +'" data-sessionid="'+ o.session_id +'">'
                                resp += "<button role='button' type='button' class='btn btn-sm btn-success fallback_"+ o.session_id +"' style='margin: 2px; "+ color +"' data-value='"+payload+"' data-sessionid='"+ o.session_id +"'>"+lines[i].substring(pos+2)+"</button> "
                                resp += "</div>"
                            } else {
                                resp += linkifyHtml( lines[i].substring(pos+2) )
                             }
                            "</td>";
                            resp += "</tr>";
                        }
                    }
                    resp+= "</table>"
                    resp +='<pre><div class="chat-body float-none"></div>'
                    for(j=i;j<lines.length;j++) {
                        resp += lines[j];
                    }
                    resp +='</pre></div>'
                    return resp;
                } else {
                    return '<pre>' + linkifyHtml(msg, {
                        attributes: function(href){
                            return {
                                title: href
                            };
                        },
                        format: function (value, type) {
                            if (type === 'url' && value.length > 45) {
                                value = 'ENLACE';
                            }
                            return value;
                        }
                    }) + '</pre>'
                }
            }).join(''));
        }
        if (buttons.length > 0){
             let i=0;
             let idButtons= Math.round(Math.random() * 10000);
             result.push( '<div id="'+idButtons+'" class="float-left   col-12" aria-label="acciones relacionadas" >');
             let showmore = true;
             for(i=0; i<buttons.length; i++) {
                let res=""
                color=""
                let boton = buttons[i];
//                if (i==7 && showmore || (i==6 && buttons[6].title.length == 1 && showmore))   {
                if (i>6 && showmore && buttons[7].title.length > 1)   {
                    let idMore = Math.round(Math.random() * 10000);
                    res+="<button type='button' role='button' class='btn btn-success col-12 col-lg-auto fallback_more' style='margin: 2px; padding-top: 0.175rem; padding-right: 0.75rem; padding-bottom: 0.275rem; padding-left: 0.75rem; background-color: #1a5b9c' data-value='relacionado' data-groupid='"+ idMore +"'>Mostrar más opciones</button>";
                    res+="<div id='more_"+ idMore+"' style='display: none'>";
                    showmore = false;
                 }
                color= "background-color: #0073e6";
                if (boton.payload.indexOf("engagement.subject")!==-1) color= "background-color: #0073e6"
                if (boton.payload.indexOf("greetings.hello")!==-1) color= "background-color: #003366"
                if (boton.title.length > 1) col= "col-12"; else col = "col-auto";
                res +="<button type='button' role='button' class='btn btn-success "+col+" col-lg-auto fallback_"+ o.session_id +"' style='margin: 2px; padding-top: 0.175rem; padding-right: 0.75rem; padding-bottom: 0.275rem; padding-left: 0.75rem; "+ color +"' data-value='"+boton.payload+"' data-idbuttons='"+ idButtons +"' data-sessionid='"+ o.session_id +"'>"+getTitle(boton.title)+"</button>";
                result.push(res);
             }
             if (i>7) result.push("</div>");
             result.join('')+   '    </div>';
        }
        if (o.conversation_ended){
            result.push(addScore(o.session_id))
        }
        result.push('</p></li>');
        return result.join('');
    }

    function getTitle(id) {
        if ( id.length > 50) return id.substring(0,50)+"...";
        else return id;

        let title = id.split(":")[1];
        if (typeof title != "undefined" && title.length > 50) title = title.substring(1,50)+"...";
        let parts = id.split(":")[0].split("-");
        let respuesta = "";
        for(let i=0; i < parts.length; i++ ) {
            if (parts[i] === parts[i].toUpperCase()) {
                respuesta = respuesta.trim();
                break;
                }
            if (i==0) parts[i] = parts[i][0].toUpperCase() + parts[i].slice(1);
            respuesta += parts[i] + " ";
        }
        if (typeof title == "undefined") {
            return respuesta;
        } else {
            return respuesta + ": " + title;
        }
    }
    function addMessageUser(o) { // { name, msg }

        return  '<li >'+

                '    <div class="align-top">'+
                '        <img src="'+ AVATAR_USER +'" alt="User Avatar" class="float-right rounded-circle" id="msg-user" style="margin-left: 4px"/>'+
                '        <div class="float-right" ><small><span class="glyphicon glyphicon-time"></span>'+ getTime() + '</small><strong class="primary-font" style="margin-left: 3px">Usuario</strong>'+
                '        </div>'+
                '    </div>'+
                '    <div class="chat-body float-none"><br><br>' +
                '        <p align="right">'+ o.msg +'</p>'+
                '    </div>'+
                '</li>';
    }

    function addScore(session_id) {
        return  '<div class="text-center" style="margin-bottom:1em">'+
                '    <div class="btn-group" role="group" aria-label="..." id="score_'+ session_id +'" data-sessionid="'+ session_id +'">'+
                '       <button type="button" class="btn btn-success" data-value="10">Buena</button>'+
                '       <button type="button" class="btn btn-info"    data-value="0">Normal</button>'+
                '       <button type="button" class="btn btn-danger"  data-value="-10">Mala</button>'+
                '    </div>'+
                '</div>';
    }

    function addEndConversation(withTxt){
        return  withTxt
                ?   '<div class="text-center">'+
                    '    <h3>Fin de conversación</h3> '+
                    '    <hr />' +
                    '    <h6>Este proyecto ha sido financiado por el Fondo Europeo de Desarrollo Regional</h6>'+
                    '    <h6>Construyendo Europa desde Aragón</h6> '+
                    '   <img style="float: center;"  src="static/img/flag_europe.svg" />'+
                    '    <hr />'+
                    '</div>'
                : '';
    }

    var $input = $INPUT
        .on('keypress', function(e){
            if(e.keyCode === 13) // INTRO key
              sendMessage();
        });

    $('#btn-chat').on('click', function(){
        sendMessage();
    });

    var sendMessage = function ( endChat ) {
        var value = $input.val();
        if (value.toUpperCase() == "ADIOS") {
            endChat = true;
            value = "adios";
        }

        if (endChat) {
            value = "adios"
        }
        if (value !== ""){
            $('#status').text("Esperando respuesta...")
            $('#btn-input').prop('disabled', true);
            $('#btn-chat').prop('disabled', true);
            $("body").css("cursor", "progress");
            // enviar al servidor
            $.ajax({
                method: "POST",
                url: POST_URL + 'chat',
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
            .then(function(json){
                if (json["name"] && json["name"] !== name) {
                    name = json["name"];
                }
                var isEND = json.conversation_ended;
                appendMessage(addMessageBot(json) + addEndConversation(isEND));

                // por si existe, pongo evento único de enviar score
                $('#score_'+ json.session_id ).one('click', sendScore);
                $('.fallback_'+ json.session_id ).one('click', sendFallback);
                $('.fallback_more').one('click', sendFallbackMore);

                if (isEND) {
                    _TIMER_END();
                } else {
                    _TIMER_START();
                }
            });
            // el valor lo escriba directamente en el chat
            if (!endChat){
                appendMessage(addMessageUser({ name: name, msg: value }),true);
            }
        }
    };

    var sendScore = function (event) {
        var $BUTTON = $(event.target);
        var session_id = $(this).data('sessionid');
        var value = parseInt($BUTTON.data('value'));
        $(this).children().hide();
        $.ajax({
            method: "POST",
            url: POST_URL + 'score',
            data: JSON.stringify({
                "score": value,
                "session_id": session_id
            }),
            dataType: "json",
            contentType: 'application/json;charset=UTF-8',
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true
        })
        .then(function(json){
            console.warn(json);
            $BUTTON.show().prop('disabled', true);
        })
    };
    var sendFallback = function (event) {
        var $BUTTON = $(event.target);
        var session_id = $(this).data('sessionid');
        var id_buttons = $(this).data('idbuttons');
        var value = $BUTTON.data('value');
        $("#"+id_buttons).children("button").hide();
        $("#"+id_buttons).children("div").children().hide();
        $BUTTON.show().prop('disabled', true);
        $('#status').text("Esperando respuesta...")
        $INPUT.blur();
        $('#btn-input').prop('disabled', true);
        $('#btn-chat').prop('disabled', true);
        $("body").css("cursor", "progress");

        $.ajax({
                method: "POST",
                url: POST_URL + 'chat',
                data: JSON.stringify({
                    "text": value,
                    "timeout": false
                }),
                dataType: "json",
                contentType: 'application/json;charset=UTF-8',
                xhrFields: {
                    withCredentials: true
                },
                crossDomain: true
            })
            .then(function(json){
                if (json["name"] && json["name"] !== name) {
                    name = json["name"];
                }
                appendMessage(addMessageBot(json))

                // por si existe, pongo evento único de enviar score
                $('#score_'+ json.session_id ).one('click', sendScore);
                $('.fallback_'+ json.session_id ).one('click', sendFallback);
                $('.fallback_more').one('click', sendFallbackMore);


                _TIMER_START();
                 $BUTTON.show().prop('disabled', true);
            });


    };
    var sendFallbackMore = function (event) {
        var $BUTTON = $(event.target);
        var groupid = $(this).data('groupid');
        var idDiv  = "#more_"+groupid;
        $BUTTON.hide();
        $(idDiv).show();
    };

    var appendMessage = function (msg, isScroll) {

        var topp = $("#messages").height()
        $("#messages").append(msg);

        if (isScroll){
            // scroll To bottom...
           MAIN.scrollTop = MAIN.scrollHeight;
        } else {
            MAIN.scrollTop=topp-101;
        }



        $INPUT.val('').blur();

    };
    var welcome = [
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabías que se los alcaldes y alcaldesas de todos los municipios de Aragón. <br> Por ejemplo: <br>- ¿Quién es el alcalde de Muel?<br> -¿Quienes son los concejales de Barbastro?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabes que tengo registradas cafeterías y restaurantes de Aragón. Puedes preguntarme la dirección o el teléfono de tu restaurante favorito para ver si lo tengo.<br> Por ejemplo:<br> -¿Cuál es la dirección del restaurante El Fuelle?<br> -¿Cuál es el teléfono de cafetería Aisa?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabes que tengo información de muchos alojamientos de Aragón. Puedes preguntarme dónde puedes alojarte para tú próxima escapada.<br>Por ejemplo:<br>- ¿Dónde puedo alojarme en Jaca?<br>- ¿Qué campings hay en Benasque?<br>- Dime las casas rurales de Albarracín ",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabes que tengo información de hoteles, albergues, apartamentos, campings y casas rurales de Aragón. Puedes preguntarme cómo reservar en el alojamiento que desees.<br>Por ejemplo:<br>- ¿Cómo puedo reservar en el hotel Ciudad de Teruel?<br>- ¿Cómo puedo reservar en la casa rural Marosa?<br>- ¿Cual es el teléfono del camping La Fresneda?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Tengo información de agencias de viaje y guías turísticos que hay en Aragón.<br>Por ejemplo:<br>- ¿Qué agencias de viaje hay en Zaragoza?<br>- Dime los guías turísticos de Huesca",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Tengo información sobre los procedimientos más comunes de tramitación electrónica.<br>Sabes, por ejemplo:<br>- ¿Qué es un certificado digital?<br>- ¿Para qué sirve un certificado digital?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Tengo información sobre la firma digital y las entidades certificadoras.<br>Por ejemplo:<br>- ¿Qué es la firma digital?<br>- ¿Qué pasos hay que seguir para instalar la firma digital?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabes que tengo datos sobre actividad empresarial.<br>Por ejemplo, me puedes preguntar:<br>- ¿Qué empresas del sector servicios hay en la provincia de Teruel?<br>- ¿Qué empresas del sector industria hay en la provincia de Zaragoza?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabes que tengo registrados datos de tráfico.<br>Por ejemplo, me puedes preguntar:<br>- ¿Existe alguna incidencia de tráfico en la provincia de Teruel?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabes que tengo registrados datos de carreteras.<br>Por ejemplo:<br>- ¿Por qué carretera puedo llegar a Castellote?<br>- ¿A qué velocidad se puede circular por la carretera TE-39?",
        "Hola. Soy el asistente de Aragón Open Data, estoy aquí para facilitarte los datos abiertos de los que dispongo.<br>Sabes que tengo registrados datos de transporte.<br>Por ejemplo:<br>- ¿Hay servicio de autobús a Bielsa?",
        "🗨 Soy el asistente de Aragón Open Data basado en Inteligencia Artificial. Estoy aquí para facilitarte los datos abiertos que dispongo. ¿en qué puedo ayudarte?"
    ];

    appendMessage(
        addMessageBot({
           // answer: [welcome[  Math.floor(Math.random()*welcome.length)]],
            answer: [welcome[11]],
            icons: []
        }),true

    );
});