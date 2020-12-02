<template lang="html">
    <v-hover>
        <v-layout slot-scope="{ hover }" class="imtte" :class="{invisible:!hover}">
            <v-textarea
                ref="textarea"
                v-model="valueInput"
                auto-grow
                rows="1"
                :disabled="!isEditing"
                class="pt-0 mt-0"
                @blur="blurEdit"
                @keydown.enter.exact.prevent="toggleEdit"
            />
            <!-- <v-slide-x-reverse-transition mode="out-in"> -->
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
            <!-- </v-slide-x-reverse-transition> -->
        </v-layout>
    </v-hover>
</template>

<script>
export default {
    props: {
        value: {
            type: String,
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
        mode (){
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
        async toggleEdit (){
            if (this.valueInput === '') { return; }
            //console.warn('toggleEdit');
            this.isEditing = !this.isEditing;
            // caso Editable, grabo...
            if (!this.isEditing){
                //console.warn('save')
                this.$emit('save', this.valueInput);
            } else {
                await this.$nextTick();
                this.$refs.textarea.$refs.input.focus();
            }
        },
    }
}
</script>

<style>
    .imtte .v-messages{
        min-height: 0; /* 12px */
    }
    .imtte .v-input{
        font-size: inherit; /* 16px */
    }
    .imtte .btn-save{
        color: var(--v-error-base);
    }
    .imtte .btn-edit{
        color: var(--v-primary-base);
    }
    .imtte .v-input__slot{
        margin-bottom: 0;
    }
        .imtte .v-input--is-disabled .v-input__slot::before{
            border-image-width: 0 !important;
        }
    .imtte .theme--light.v-input--is-disabled textarea {
        color: rgba(0,0,0,0.5);
    }
    .imtte .btn-edit,
    .imtte .v-btn__content,
    .imtte .v-icon {
        transition-duration: unset;
    }
    .imtte.invisible .btn-edit{
        visibility: hidden;
    }
</style>
