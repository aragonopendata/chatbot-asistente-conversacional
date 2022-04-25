<template>
    <v-card tile class="mcb-card">
        <v-toolbar 
            :color="toolbarColor"
            :dark="!$vuetify.theme.dark"
            :light="$vuetify.theme.dark"
            dense
            class="mcb-card-toolbar"
            >
            <v-toolbar-title>
                <v-icon>{{ toolbarIcon }}</v-icon>  <span v-html="title" />
            </v-toolbar-title>

            <v-spacer />

            <v-tooltip 
                v-if="speech_has"
                bottom
                >
                <template #activator="{ on }">
                    <v-btn 
                        icon
                        v-on="on"
                        @click="speech_disabled = !speech_disabled"
                        >
                        <v-icon>{{ speech_icon }}</v-icon>
                    </v-btn>
                </template>
                <span>{{ speech_disabled ? 'Activa' : 'Desactiva' }} Leer textos en voz alta</span>
            </v-tooltip>

            <v-divider 
                light
                class="mr-2" 
                vertical 
            />
            <ita-idle-timer 
                ref="itaIdleTimer" 
                title="component" 
                :max-idle-time="maxIdleTime"
                @onEnd="endChat"
            />
        </v-toolbar>
        <v-card-text 
            ref="chat" 
            class="mcb-chatbot mcb-card-body"
            >
            <v-row
                v-for="({ text, answer = [], time, conversation_ended, score, session_id } = item, index) in chat"
                :id="`chat_item_${index}`"
                :key="`chat_item_${index}`"
                no-gutters
                class="py-5"
                >
                <v-col cols="12">
                    <v-icon small>
                        mdi-clock-outline
                    </v-icon>
                    {{ time }}
                </v-col>
                <v-col v-if="text" offset="3">
                    <div class="story-bubble story-bubble-right bgcolor-o05 elevation-5">
                        <small class="grey--text">User</small>
                        <br>
                        {{ text }}
                    </div>
                </v-col>
                <v-col cols="9" class="mt-4">
                    <div class="story-bubble story-bubble-left bgcolor-o1 elevation-5">
                        <ita-speech-synthesis
                            v-if="!speech_disabled"
                            autostart
                            :html="linkify(answer.join())"
                        />
                        <small class="grey--text">Bot</small>
                        <br>
                        <div 
                            style="white-space:pre-wrap" 
                            v-html="linkify(answer.join('\n\n'))" 
                        />
                        <template v-if="conversation_ended">
                            <v-divider class="mt-4 mb-1" />
                            <div class="caption">Tu opinión de este servicio es:</div>
                            <ItaChatScore :value="score" @change="submitScore($event, session_id)" />
                        </template>
                    </div>
                </v-col>
                <v-col v-if="conversation_ended" cols="12" class="text-center py-10">
                    <h2 class="title">
                        Fin de conversación
                    </h2>
                    <v-divider class="my-5" />
                    <h2 class="subtitle-1">
                        Nueva conversación
                    </h2>
                </v-col>
            </v-row>
        </v-card-text>
        <v-toolbar
            :color="toolbarColor"
            dense
            flat
            class="mcb-card-toolbar"
            >
            <!-- 
                error en v-text-field: clearable => value === null (no "") 
                cambiar:
                    v-model="chat_user"
                por:
                    :value="chat_user"
                    @input="chat_user = $event || ''"
                
            -->
            <v-text-field
                ref="input"
                dense
                solo
                flat
                autofocus
                hide-details
                clearable
                append-icon="mdi-send"
                :label="label"
                :disabled="isBusy"
                :value="chat_user"
                @input="chat_user = $event || ''"
                @click:append="sendChat()"
                @keydown.enter.exact.prevent="sendChat()"
            />
            <eme-speech-recognition 
                fab
                small
                class-all="ml-2"
                :text.sync="chat_user"
                :voice-actions="[
                    {
                        voices: ['borrar', 'eliminar', 'vaciar'],
                        action: resetChat
                    },
                    {
                        voices: ['enviar'],
                        action: sendChat
                    }
                ]"
            />
        </v-toolbar>
    </v-card>
</template>

<script>
    import { mapState, mapActions } from 'vuex';

    import linkify from '~/plugins/eme-linkify.js';

    export default {
        props: {
            active: {
                type: Boolean,
                default: false
            },
            toolbarColor: {
                type: String,
                default: "",
            },
            toolbarIcon: {
                type: String,
                default: "",
            },
            title: {
                type: String,
                default: "Chat",
            },
            maxIdleTime: {
                type: Number,
                default: 600, // 10seg | 60 = 1min | 300 = 5 min
            },
            disabled: {
                type: Boolean,
                default: true
            },
            label: {
                type: String,
                default: `Write a message here...`
            },
        },
        data (){
            return {
                chat_user: '',
                chat: [],
                isWaitingAnswer: false,
                speech_disabled: true,
                speech_has: !!window.speechSynthesis,
            }
        },
        computed:{
            ...mapState(['chatBot']),
            isBusy () {
                return this.disabled || this.isWaitingAnswer
            },
            speech_icon () {
                return this.speech_disabled ? 'mdi-volume-off' : 'mdi-volume-high'
            }
        },
        watch: {
            active (isActive) {
                if (!isActive && this.$refs.itaIdleTimer.$options._TIMER) {
                    // close dialog
                    this.endChat();
                }
            }
        },
        methods: {
            ...mapActions(['GET','SET','ADD']),
            resetChat () {
                this.chat_user = ''
            },
            async sendChat ( endChat = false ){
                if (endChat) {
                    this.chat_user = 'adios'
                }
                if (this.chat_user !== ''){
                    this.isWaitingAnswer = true;
                    try {
                        this.SET(['chatUser', this.chat_user]);
                        await this.ADD([
                            `chatBot`,
                            {
                                "text": this.chat_user,
                                "timeout": endChat || false
                            }
                        ]);
                        this.chat.push({
                            time: new Date().toLocaleTimeString("es-ES",{timeStyle: "short"}),
                            // caso endChat no muestro el cliente "adios"...
                            text: endChat ? '' : this.chat_user,
                            score: null,
                            ...this.chatBot, // {answer: [], conversation_ended, icons: [], session_id}
                        });
                        this.chat_user = '';
                        this.scrollToBottom();
                    } catch (error) {
                        this.$emit('onError', {config: this.chat_user, method: 'POST', error});
                    }
                    this.isWaitingAnswer = false;
                    await this.$nextTick();
                    this.$refs.input.focus();
                    this[ this.chatBot.conversation_ended ? 'endTimer' : 'startTimer' ]()
                }
            },
            async scrollToBottom (){
                await this.$nextTick();
                const ELE = this.$refs.chat;
                // try {
                    ELE.scrollTo(0, ELE.scrollHeight);
                    // no compatible IE
                    // ELE.scrollTo({
                    //     left: 0,
                    //     top: ELE.scrollHeight,
                    //     behavior: 'smooth',
                    // });
                // } catch (error) {
                // }
            },
            async submitScore (score, session_id) {
                // console.warn('submitScore', score, JSON.stringify(item,null,4));
                try {
                    await this.ADD([
                        'score',
                        {
                            score,
                            session_id
                        }
                    ])
                } catch (error) {
                    this.$emit('onError', {config: 'score', method: 'POST', error});
                }
            },
            endChat () {
                this.endTimer(); // ends old timer...
                this.sendChat(true); // inits new timer...
            },
            //-------------------------------------------------------------------- 
            startTimer () {
                this.$refs.itaIdleTimer.startTimer()
            },
            endTimer () {
                this.$refs.itaIdleTimer.endTimer()
            },
            hasTimer () {
                return this.$refs.itaIdleTimer.hasTimer()
            },
            linkify: text => linkify(text)
        }
    }
</script>

<style>
    /********************************************************* */
    .mcb-card {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
        .mcb-card-toolbar {
            flex-grow: 0 !important;
        }
        .mcb-card-body {
            flex-grow: 1 !important;
            overflow-y: auto;
        }
</style>
