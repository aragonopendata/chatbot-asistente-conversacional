/*
 * encontrar un modo de crear una sola instancia de tooltip para toda la aplicación
 */
<template>
    <!-- <v-tooltip bottom content-class="itaBtnIcon">
        <template #activator="{ on: tooltip }"> -->
            <v-fab-transition>
                <v-btn
                    v-show="showBtn"
                    fab
                    :disabled="disabled"
                    :height="size"
                    :width="size"
                    :title="tooltip || $attrs.title"
                    v-bind="$attrs"
                    v-on="{ /*...tooltip,*/ ...activator }"
                    @click.stop="$emit('action')"
                >
                    <v-icon>
                        {{ icon }}
                    </v-icon>
                </v-btn>
            </v-fab-transition>
        <!-- </template>
        {{ tooltip }}
    </v-tooltip> -->
</template>

<script>
    export default {
        inheritAttrs: false,
        props: {
            icon: {
                type: String,
                default: 'mdi-exclamation'
            },
            tooltip: {
                type: String,
                default: ''
            },
            // color: {
            //     type: String,
            //     default: ''
            // },
            // case parent 'v-menu' or 'v-dialog' and v-btn is his activator
            activator: {
                type: Object,
                default: () => {}
            },
            showBtn: {
                type: Boolean,
                default: true
            },
            size: {
                type: [Number, String],
                default: 32
            },
            disabled: {
                type: Boolean,
                default: false
            }
        }
    }
</script>

<style>
    .itaBtnIcon.v-tooltip__content {
        font-size: 12px;
        padding: 3px 8px;
    }
</style>
