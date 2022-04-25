<template lang="html">
    <v-hover #default="{ hover }">
        <v-row no-gutters class="imate" :class="{invisible:!hover}">
            <v-col>
                <v-autocomplete
                    ref="autocomplete"
                    v-model="valueInput"
                    class="ma-0 pa-0 justify-end"
                    hide-details
                    :disabled="!isEditing"
                    :items="intents"
                    label="@ Intent:"
                    item-text="name"
                    item-value="name"
                    @blur="blurEdit"
                >
                    <template #item="{ item }">
                        {{ item.name }}
                        <ita-num-sup :num="item.templates_length" />
                    </template>
                </v-autocomplete>
            </v-col>
            <v-col cols="auto">
                <v-btn
                    v-show="!!value"
                    icon
                    text
                    title="SEE templates of this INTENT"
                    color="warning darken-2"
                    class="btn-target ma-0"
                    @click.stop="$emit('targetIntent')"
                >
                    <v-icon>mdi-crosshairs-gps</v-icon>
                </v-btn>
            </v-col>
            <v-col cols="auto">
                <v-slide-x-reverse-transition mode="out-in">
                    <v-btn
                        ref="btn"
                        :key="`btn-${mode}`"
                        icon
                        text
                        :class="[`ma-0`, `btn-${mode}`]"
                        :title="`${mode.toUpperCase()} text`"
                        :disabled="!valueInput"
                        @click.stop="toggleEdit"
                    >
                        <v-icon>{{ icon }}</v-icon>
                    </v-btn>
                </v-slide-x-reverse-transition>
            </v-col>
        </v-row>
    </v-hover>
</template>

<script>
    export default {
        props: {
            value: {
                type: String,
                required: true,
            },
            intents: {
                type: Array,
                required: true,
            },
        },
        data (){
            return {
                isEditing: false,
                valueInput: ''
            }
        },
        computed: {
            // intents_array(){
            //     return this.intents.map(intent => intent.name); //Object.keys(this.intents);
            // },
            mode () {
                return this.isEditing ? 'save' : 'edit';
            },
            icon () {
                return this.isEditing ? 'mdi-content-save' : 'mdi-pencil'
            }
        },
        watch: {
            value: {
                handler ( value ){
                    this.valueInput = value;
                    this.isEditing = (value === '');
                },
                immediate: true,
            }
        },
        methods: {
            async blurEdit ({ relatedTarget }){
                await this.$nextTick();
                // ERROR !!!! => SE dispara "BLUR" 2 veces ¿?¿?¿?¿?¿?¿?
                // console.warn('autocomplete - blurEdit', this.$refs);
                // compruebo que no venga del botón de al lado...
                if (this.$refs.btn && relatedTarget !== this.$refs.btn.$el){
                    this.isEditing = (this.value === ''); //false;
                    // resetea al último valor...
                    this.valueInput = this.value;
                }
            },
            toggleEdit (){
                if (this.valueInput === '') { return; }
                //console.warn('toggleEdit');
                this.isEditing = !this.isEditing;
                // caso Editable, grabo...
                if (!this.isEditing){
                    //console.warn('save')
                    this.$emit('save', this.valueInput);
                } else {
                    this.$nextTick(function (){
                        this.$refs.autocomplete.$refs.input.focus();
                    })
                }
            },
        }
    }
</script>

<style>
    .imate .v-text-field__details{
        display: none;
    }
    .imate .v-input{
        font-size: inherit; /* 16px */
    }
    .imate .btn-save{
        color: var(--v-error-base);
    }
    .imate .btn-edit{
        color: var(--v-primary-base);
    }
    .imate .v-input__slot{
        margin-bottom: 0;
    }
        .imate .v-input--is-disabled .v-input__slot::before{
            border-image-width: 0 !important;
        }
    .imate .theme--light.v-input--is-disabled textarea {
        color: rgba(0,0,0,0.5);
    }
    .imate .v-label{
        top: .5rem !important;
    }
    .imate .btn-target,
    .imate .btn-edit,
    .imate .v-btn__content,
    .imate .v-icon,
    .imate .v-label {
        transition-duration: unset;
    }
    .imate.invisible .btn-target,
    .imate.invisible .btn-edit,
    .imate.invisible .v-label{
        visibility: hidden;
    }
</style>
