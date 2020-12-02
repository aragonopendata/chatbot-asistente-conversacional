<template lang="html">
    <v-snackbar
        v-model="show"
        :color="color"
        bottom
        :multi-line="multiLine"
        :vertical="vertical"
        :timeout="timeout"
        class="ita-notification"
        dark
    >
        <div v-if="title" class="text--center">
            <v-icon>{{ icon }}</v-icon>
            {{ title }}
        </div>
        <v-divider v-if="title" vertical inset class="mx-4" />
        <div>
            {{ message }}
        </div>
        <v-btn
            text
            @click="show = false"
        >
            <v-icon>mdi-close</v-icon>
        </v-btn>
    </v-snackbar>
</template>

<script>
    const isCONFIG = o => ['color','timeout', 'multiLine', 'title', 'icon'].every(k => k in o);
            
    export default {
        props: {
            type: {
                type: String,
                default: 'success',
                validator: value => ['success', 'warning', 'error', 'info'].includes(value)
            },
            message: {
                type: String,
                default: ''
            },
            successConfig: {
                type: Object,
                default: () => ({
                    color: 'success',
                    timeout: 1000,
                    multiLine: false,
                    title: '',
                    icon: ''
                }),
                validator: isCONFIG
            },
            errorConfig: {
                type: Object,
                default: () => ({
                    color: 'error',
                    timeout: 0,
                    multiLine: true,
                    title: 'ERROR',
                    icon: 'mdi-bug'
                }),
                validator: isCONFIG
            },
            warningConfig: {
                type: Object,
                default: () => ({
                    color: 'warning',
                    timeout: 5000,
                    multiLine: true,
                    title: 'WARNING',
                    icon: 'mdi-alert'
                }),
                validator: isCONFIG
            },
            infoConfig: {
                type: Object,
                default: () => ({
                    color: 'info',
                    timeout: 5000,
                    multiLine: true,
                    title: 'INFO',
                    icon: 'mdi-information'
                }),
                validator: isCONFIG
            }
        },
        data (){
            return {
                show: false,
                vertical: false,
            }
        },
        computed: {
            color (){     return this[`${this.type}Config`].color },
            timeout (){   return this[`${this.type}Config`].timeout },
            multiLine (){ return this[`${this.type}Config`].multiLine },
            title (){     return this[`${this.type}Config`].title },
            icon (){      return this[`${this.type}Config`].icon },
        },
        watch: {
            type ()    { this.showNotification(); },
            message () { this.showNotification(); },
            show ( shown ){
                if (shown === false){
                    setTimeout(() => {
                        this.$emit('close')
                    }, 400); // .4s según desaparece v-snackbar
                }
            }
        },
        methods: {
            showNotification () {
                this.show = false;
                if (this.message) {
                    this.show = true;
                }
            }
        }
    }
</script>

<style>
    .ita-notification {
        word-break: break-word;
    }
</style>
