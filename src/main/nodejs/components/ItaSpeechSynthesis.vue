<template>
    <v-tooltip 
        v-if="synth"
        bottom
        >
        <template #activator="{ on }">
            <v-btn 
                small
                icon
                class="float-right"
                :disabled="disabled"
                v-on="on"
                @click="speechStart"
                >
                <v-icon :class="color">{{ icon }}</v-icon>
            </v-btn>
        </template>
        <span>{{ tooltip }}</span>
    </v-tooltip>
</template>

<script>
    export default {
        props: {
            text: {
                type: String,
                default: ""
            },
            html: {
                type: String,
                default: ""
            },
            target: {
                type: String,
                default: "",
            },
            autostart: {
                type: Boolean,
                default: false
            },
            iconPlay: {
                type: String,
                default: 'mdi-text-to-speech'
            },
            iconStop: {
                type: String,
                default: 'mdi-text-to-speech-off'
            },
            tooltipPlay: {
                type: String,
                default: 'Leer texto en voz alta'
            },
            tooltipStop: {
                type: String,
                default: 'Pausar la voz alta'
            }
        },
        data () {
            return {
                synth: window.speechSynthesis,
                speech: new window.SpeechSynthesisUtterance(),
                speaking: false,
            }
        },
        computed: {
            icon () {    return this.speaking ? this.iconStop    : this.iconPlay },
            tooltip () { return this.speaking ? this.tooltipStop : this.tooltipPlay },
            color () {   return this.speaking ? 'error--text'    : 'primary--text' },
            txt () {     
                return this.container 
                    ? this.container.textContent
                    : this.html
                        ? this.textFromHtml(this.html)
                        : this.text 
            },
            disabled () { return !this.txt },
            container () { return this.target ? window.document.getElementById(this.target) : false },
        },
        mounted () {
            this.speech.onstart = () => { this.speaking = true };
            this.speech.onend   = () => { this.speaking = false };

            if (this.autostart) {
                this.speechStart();
            }
        },
        beforeDestroy () {
            this.synth.cancel();
        },
        methods: {
            textFromHtml: html => (new DOMParser().parseFromString(html, 'text/html')).body.textContent || '',
            speechStart () {
                this.synth.cancel();
                if (!this.speaking) {
                    this.speech.text = this.txt;
                    this.synth.speak(this.speech);
                }
            }
        }
    }
</script>
