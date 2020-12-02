<template lang="html">
    <v-list-item-title class="imle">
        <input
            ref="input"
            type="text"
            v-bind="$attrs"
            autofocus
            :value="value"
            @keydown.enter.exact.stop.prevent="action"
            @blur="blur"
            @keydown.esc="blur"
        />
    </v-list-item-title>
</template>

<script>
    export default {
        inheritAttrs: false,
        props: ['value'],
        mounted (){
            this.$refs.input.focus();
        },
        methods: {
            action (){
                this.$emit('action', this.$refs.input.value );
                this.blur();
            },
            blur (){
                this.$emit('cancel')
            },
        }
    }
</script>

<style>
    .imle input {
        width: 100%;
        border: 1px solid grey;
        height: 24px;
        background-color: white;
    }
</style>
