<template>
    <v-chip-group
        v-model="selected"
        column
        :multiple="multiple"
        active-class="primary--text primary font-weight-bold"
        >
        <v-chip
            v-for="({count, label, value}) in itemsWithoutNull"
            :key="label"
            :value="value"
            :disabled="disabled"
            filter
            outlined
            small
            >
            {{ label }} <sup class="grey--text">{{ count }}</sup>
        </v-chip>
    </v-chip-group>
</template>

<script>
    export default {
        props: {
            items: {
                type: Array, //  [ { count, name, label }, .... ]
                default: () => []
            },
            multiple: {
                type: Boolean,
                default: false
            },
            disabled: {
                type: Boolean,
                default: true
            }
        },
        data () {
            return {
                selected: []
            }
        },
        computed: {
            // FIXED :: ¡¡¡OJO!!!
            // existe un problema con todos los valores === NULL
            // por ahora, desaparecen de filtros...
            itemsWithoutNull () {
                return this.items.filter(i => i.value !== null)
            }
        },
        watch: {
            selected (values = []) {
                //console.warn( 'watch', values, oldvalues, [].concat(values) );
                // siempre (múltiple o no) devolverá un ARRAY de valores o vacío si están todos deseleccionados
                this.$emit('change', [].concat(values))
            }
        }
    }
</script>
