<template lang="html">
    <v-menu
        v-model="shown"
        :close-on-content-click="false"
        min-width="350px"
    >
        <template #activator="{ on: menu }">
            <ita-btn-icon
                :show-btn="showActivator || shown"
                :tooltip="tooltipActivator"
                :activator="menu"
                :icon="iconActivator"
                :color="color"
            />
        </template>
        <v-card>
            <v-card-text>
                <v-text-field
                    v-if="!multiple"
                    ref="textfield"
                    :prepend-inner-icon="iconActivator"
                    :label="labelInput"
                    :hint="hintInput"
                    autofocus
                    :value="value"
                    @change="action"
                    @input="input"
                />
                <v-textarea
                    v-else
                    ref="textfield"
                    v-model="multiple_values"
                    :prepend-inner-icon="iconActivator"
                    :label="labelInput"
                    :hint="hintInput"
                    autofocus
                    auto-grow
                    rows="1"
                />
            </v-card-text>
            <v-card-actions v-if="labelBtnAction">
                <v-spacer />
                <v-btn
                    :disabled="!hasValues"
                    text
                    color="primary"
                    @click="action"
                >
                    {{ labelBtnAction }}
                </v-btn>
                <v-btn
                    color="error"
                    @click="close"
                >
                    {{ labelBtnCancel }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-menu>
</template>

<script>
    import ItaBtnIcon from '~/components/ItaBtnIcon'

    export default {
        components: {
            ItaBtnIcon
        },
        props: {
            iconActivator: {
                type: String,
                default: "mdi-circle-outline"
            },
            tooltipActivator: {
                type: String,
                default: "Action"
            },
            labelInput: {
                type: String,
                default: "labelInput"
            },
            labelBtnAction: {
                type: String,
                default: ""
            },
            labelBtnCancel: {
                type: String,
                default: "cancel"
            },
            hintInput:{
                type: String,
                default: "", //Do not repeat an existing name for a new Intent"
            },
            // v-model = XXXX
            value: {
                type: [String, Array],
                default: '',
            },
            multiple: {
                type: Boolean,
                default: false,
            },
            color: {
                type: String,
                default: ""
            },
            showActivator: {
                type: Boolean,
                default: true
            }
        },
        data (){
            return {
                shown: false,
                multiple_values: "",
            }
        },
        computed: {
            hasValues () {
                return this.multiple_values.length || this.value.length
            }
        },
        watch: {
            shown (isShown){
                if (!isShown){
                    // reseteo el valor cuando se oculta...
                    // el close() no lo dispara pulsando fuera del menu
                    this.multiple_values = "";
                } else {
                    // this.$nextTick(() => {
                    //     //console.warn(this.$refs.textfield.$refs.input);
                    //     this.$refs.textfield.$refs.input.focus();
                    // })
                    setTimeout(() => this.$nextTick(this.$refs.textfield.focus), 50)
                }
            },
        },
        methods: {
            close (){
                this.shown = false;
            },
            action (){
                // once more if multiple
                if (this.multiple){
                    this.input(this.multiple_values);
                }
                this.$emit('action');
                this.close();
            },
            input ( value ){
                const V = this.multiple
                    // lines in array, trim, no empties
                    ? value.split(/\n/).map(v => v.trim()).filter(v => v)
                    : value
                    ;
                this.$emit('input', V)
            }
        }
    }
</script>
<style scoped>
    .v-card__text {
        padding: 0 16px; /*16px 16px*/
    }

</style>
