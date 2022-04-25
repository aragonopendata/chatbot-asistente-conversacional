<template>
    <v-btn 
        class="text-none"
        v-bind="props"
        @click="copy"
        >
        <v-icon :left="!('fab' in props)">{{ iconCurrent }}</v-icon>
        {{ 'fab' in props ? '' : labelCurrent }}
    </v-btn>
</template>

<script>
    export default {
        props: {
            text: {
                type: String,
                default: ''
            },
            title: {
                type: String,
                default: 'Copiar al portapapeles'
            },
            label: {
                type: String,
                default: 'Copiar'
            },
            labelCopied: {
                type: String,
                default: 'Copiado !!!'
            },
            icon: {
                type: String,
                default: 'mdi-content-copy'
            },
            iconCopied: {
                type: String,
                default: 'mdi-clipboard-check-outline'
            },
            color: {
                type: String,
                default: 'default'
            },
            colorCopied: {
                type: String,
                default: 'success'
            },
            timelapse: {
                type: Number,
                default: 1000, // miliseconds
            },
            btnProps: {
                type: Object,
                default: () => {}
            },
        },
        data () {
            return {
                disabled: false,
                isCopied: false
            }
        },
        computed: {
            iconCurrent () {
                return this.isCopied ? this.iconCopied : this.icon
            },
            labelCurrent () {
                return this.isCopied ? this.labelCopied : this.label
            },
            colorCurrent (){
                return this.isCopied ? this.colorCopied : this.color
            },
            props () {
                console.log(this.$attrs)
                return { 
                    title: this.title,
                    color: this.colorCurrent,
                    ...this.$attrs
                }
            }
        },
        watch: {
            isCopied (v) {
                if (v === true) {
                    setTimeout(() => {
                        this.isCopied = false;
                    }, this.timelapse)
                }
            }
        },
        methods: {
            /*async*/ copy () {
                this.disabled = true

                // await navigator.clipboard.writeText(this.text)
                const e = document.createElement('textarea');
                e.value = this.text;
                document.body.appendChild(e);
                e.focus();
                e.select();
                document.execCommand('copy');
                document.body.removeChild(e);

                this.disabled = false
                this.isCopied = true
            }
        }
    }
</script>
