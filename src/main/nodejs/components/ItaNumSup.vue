<template>
    <sup :class="num ? 'grey--text' : 'error--text'" :hidden="hidenum">
        {{ num_of_total }}
    </sup>
</template>

<script>
    export default {
        props: {
            num: {
                type:[Number, String, Object, Array],
                default: ''
            },
            total: {
                type:[Number, String, Object, Array],
                default: ''
            },
            hide: {
                type:[Number, String],
                default: ''
            }
        },
        computed: {
            num_of_total (){
                if (this.total === '') { return this.num; }
                const NUM = this.count(this.num);
                const TOTAL = this.count(this.total);
                return NUM === TOTAL ? NUM : `${NUM}/${TOTAL}`
            },
            hidenum (){
                return this.num_of_total === this.hide;
            }
        },
        methods: {
            count (ao){
                return !ao ? 0 : Array.isArray(ao) ? ao.length : Object.keys(ao).length;
            },
        }
    }
</script>
