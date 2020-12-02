<template lang="html">
    <v-dialog v-model="shown" max-width="500px">
        <v-tooltip bottom>
            <template #activator="{ on }">
                <v-btn 
                    icon 
                    v-on="on" 
                    @click.stop="shown = true"
                >
                    <v-icon>{{ iconActivator }}</v-icon>
                </v-btn>
            </template>
            <span>{{ tooltipActivator }}</span>
        </v-tooltip>

        <v-card>
            <v-card-text>
                <v-text-field
                    v-if="!multiple && shown"
                    :label="labelInput"
                    :hint="hintInput"
                    autofocus
                    :value="value"
                    @change="action"
                    @input="input"
                />
                <v-textarea
                    v-if="multiple && shown"
                    v-model="multiple_values"
                    :label="labelInput"
                    :hint="hintInput"
                    autofocus
                    auto-grow
                    rows="1"
                />
                <!-- <small class="grey--text">* This doesn't actually save.</small> -->
            </v-card-text>
            <v-card-actions v-if="labelBtnAction">
                <v-spacer />
                <v-btn
                    :disabled="(value.length === 0 && multiple_values.length === 0)"
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
</v-dialog>
</template>

<script>
    export default {
        props: {
            iconActivator: {
                type: String,
                default: "radio_button_unchecked"
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
                type: String,
                default: '',
            },
            multiple: {
                type: Boolean,
                default: false,
            },
        },
        data (){
            return {
                shown: false,
                multiple_values: "",
            }
        },
        watch: {
            shown (isShown){
                if (!isShown){
                    // reseteo el valor cuando se oculta...
                    // el close() no lo dispara pulsando fuera del dialog
                    this.multiple_values = "";
                }
            }
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
