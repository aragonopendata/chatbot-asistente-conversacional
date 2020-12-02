<template>
    <v-tooltip
        v-if="recognition"
        bottom
        >
        <template #activator="{ on }">
            <v-btn 
                v-bind="$attrs"
                :class="classes + ' ' + classAll"
                v-on="on"
                @click="speechStart"
                >
                <v-icon :large="voice">{{ icon }}</v-icon>
            </v-btn>
        </template>
        {{ tooltip }}
    </v-tooltip>
</template>

<script>
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = SpeechRecognition ? new SpeechRecognition() : false;

    export default {
        inheritAttrs: false,
        props: {
            text: {
                type: [String, null],
                default: ''
            },
            lang: {
                type: String,
                default: 'es-ES'
            },
            iconOff: {
                type: String,
                default: 'mdi-microphone'
            },
            iconOn: {
                type: String,
                default: 'mdi-microphone-off'
            },
            tooltipOff: {
                type: String,
                default: 'Comenzar dictado de texto'
            },
            tooltipOn: {
                type: String,
                default: 'Detener dictado de texto'
            },
            voiceInternalActions: {
                type: Array,
                default: () => [
                    {
                        voices: ['parar', 'pausar', 'desactivar', 'terminar', 'apagar', 'stop'],
                        action: 'onPauseStart'
                    },
                    {
                        voices: ['comenzar', 'continuar', 'activar', 'encender'],
                        action: 'onPauseEnd'
                    }
                ]
            },
            voiceActions: {
                type: Array,
                default: () => []
            },
            classAll: {
                type: String,
                default: ''
            },
            classOff: { 
                type: String, 
                default: 'primary--text'
            },
            classOn: { 
                type: String, 
                default: 'error--text lighten-2'
            },
            classVoice: { 
                type: String, 
                default: 'error--text darken-2'
            },
            classPaused: { 
                type: String, 
                default: 'grey--text'
            }
        },
        data () {
            return {
                active: false,
                voice: false,
                paused: false,
                recognition,
                runtimeTranscription: '',
                sentences: [],
            }
        },
        computed: {
            icon () {    return this.active ? this.iconOn    : this.iconOff },
            tooltip () { return this.active ? this.tooltipOn : this.tooltipOff },
            classes () { 
                return this.paused 
                    ? this.classPaused 
                    : this.active 
                        ? this.voice 
                            ? this.classVoice 
                            : this.classOn 
                        : this.classOff 
            },
            // color () {   return this.paused ? 'grey--text' : this.active ? this.voice ? 'error--text lighten-2' : 'error--text darken-3' : 'primary--text' },
            actions () {
                return [ ...this.voiceInternalActions, ...this.voiceActions ].reduce((o, {voices, action}) => { 
                        // check if "action" is internal or extenal to this component
                        const act = typeof action === "string" ? this[action] : action;
                        voices.forEach(voice => {
                            o[voice] = act
                        });
                        return o;
                    }, {});
            }
        },
        mounted () {
            recognition && this.speechInit();
        },
        beforeDestroy () {
            recognition && this.speechDestroy();
        },
        methods: {
            speechInit () {
                recognition.lang = this.lang;
                recognition.interimResults = true;
                recognition.addEventListener('speechstart', this.onSpeechStart);
                recognition.addEventListener('speechend', this.onSpeechEnd);
                recognition.addEventListener('result', this.onResult);
                recognition.addEventListener('end', this.onEnd);
            },
            speechDestroy () {
                recognition.removeEventListener('speechstart', this.onSpeechStart);
                recognition.removeEventListener('speechend', this.onSpeechEnd);
                recognition.removeEventListener('result', this.onResult);
                recognition.removeEventListener('end', this.onEnd);
            },
            onPauseStart ()  { this.paused = true },
            onPauseEnd ()    { this.paused = false },
            onSpeechStart () { this.voice = true },
            onSpeechEnd ()   { this.voice = false },
            onResult (event) {
                    const text = Array.from(event.results)
                        .map(result => result[0])
                        .map(result => result.transcript)
                        .join('')
                    this.runtimeTranscription = text
            },
            onEnd () { 
                if (this.runtimeTranscription) {
                    // console.warn('onEnd', this.runtimeTranscription, this.runtimeTranscription in this.actions);
                    if (this.runtimeTranscription in this.actions){
                        this.actions[this.runtimeTranscription]()
                        this.runtimeTranscription = '';
                    } else if (!this.paused) {
                        this.sentences.push(this.capitalizeFirstLetter(this.runtimeTranscription));
                        this.$emit('update:text', `${this.text}${this.sentences.slice(-1)[0]} `);
                        this.runtimeTranscription = '';
                    }
                }
                recognition.stop()
                if (this.active) {
                    recognition.start()
                }
            },
            capitalizeFirstLetter (str) {
                return str.charAt(0).toUpperCase() + str.slice(1)
            },
            speechStart () {
                if (this.active) {
                    // end
                    this.active = false;
                    recognition.stop();
                    this.$emit('speechend', {
                        sentences: this.sentences,
                        text:      this.sentences.join(' ')
                    })
                } else {
                    // start
                    this.active = true;
                    recognition.start();
                }
                this.paused = false;
            }
        }
    }
</script>
