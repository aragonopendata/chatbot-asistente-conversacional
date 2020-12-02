<script>
    import { Bubble, mixins } from "vue-chartjs"
    const { reactiveProp } = mixins

    export default {
        extends: Bubble,
        mixins: [ reactiveProp ],
        props: ['chartData', 'options'],
        mounted () {
            this.renderChart(this.chartData, this.options);
        }
    };
</script>
