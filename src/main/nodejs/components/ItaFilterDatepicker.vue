<template>
    <v-menu
        v-model="isMenuShown"
        :close-on-content-click="false"
        :return-value.sync="isMenuShown"
        transition="scale-transition"
        offset-y
        min-width="290px"
        :disabled="disabled"
        >
        <template #activator="{ on }">
            <v-text-field
                v-model="filterTextFieldFormatted" 
                hide-details
                icon="mdi-calendar"
                :disabled="disabled"
                clearable
                clear-icon="mdi-filter-remove"
                readonly
                :title="JSON.stringify(filterDatePicker)"
                dense
                style="font-size:85%"
                v-on="on"
                @click:clear="clearDate"
            />
        </template>
        <v-date-picker 
            v-model="filterDatePicker" 
            range 
            no-title
            scrollable
            locale="es"
            >
            <v-spacer />
            <v-btn text color="primary" @click="cancelDate">Cancelar</v-btn>
            <v-btn color="primary" @click="saveDate">OK</v-btn>
        </v-date-picker>
    </v-menu>
</template>

<script>
    export default {
        props: {
            disabled: {
                type: Boolean,
                default: true
            }
        },
        data () {
            return {
                isMenuShown: false,
                filterDatePicker: [], //['2019-11-09', '2019-11-28']
                filterTextField: [],
                filterTextFieldFormatted: '',
            }
        },
        methods: {
            saveDate () {
                // ['2019-11-09', '2019-11-28'] => '09/11/2019 ~ 28/11/2019'
                this.filterTextField = this.filterDatePicker.sort();
                this.filterTextFieldFormatted = this.filterTextField.map(d => new Date(d).toLocaleDateString()).join(' ~ ')
                this.closeMenu();
                this.$emit('change', this.filterTextField);
            },
            cancelDate () {
                this.filterDatePicker = this.filterTextField;
                this.closeMenu();
            },
            closeMenu () {
                this.isMenuShown = false;
            },
            clearDate () {
                this.filterDatePicker = [];
                this.saveDate();
            }
        }
    }
</script>
