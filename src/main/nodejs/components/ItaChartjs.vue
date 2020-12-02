<template>
    <v-card flat color="transparent">
        <v-card-title class="pa-0">
            {{ title }}
            <v-spacer />
            <v-menu v-model="menu">
                <template v-if="types.length > 1" #activator="{ on }">
                    <v-btn icon v-on="on">
                        <v-icon>{{ iconSettings }}</v-icon>
                    </v-btn>
                </template>
                <v-list dense>
                    <v-subheader>Change chart:</v-subheader>
                    <v-list-item
                        v-for="{chart, icon, options} in chartsEnabled" 
                        :key="chart" 
                        @click="selectChart(chart, options)"
                        >
                        <v-list-item-title>
                            <v-icon>{{ icon }}</v-icon>
                            <span>{{ chart }}</span>
                            <v-chip 
                                v-if="chart === chartType"
                                x-small 
                                color="info" 
                                label
                               >
                                default
                            </v-chip>
                        </v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-card-title>
        <keep-alive>
            <component :is="component" :chart-data="data" :options="chartOptions" />
        </keep-alive>
    </v-card>
</template>

<script>
    import ChartDataLabels from 'chartjs-plugin-datalabels';

    const _CHART_TYPES_ = ['Bar', 'Line', /*'Spline',*/ 'Pie', 'Donut', 'Bubble', 'PolarArea', 'Radar'];

    const _OPTIONS_DISPLAY_ = {
            // auto and no '0'
            display: ({ dataIndex, dataset }) => {
                const value = dataset.data[dataIndex];
                return value > 0 ? 'auto' : false
            }
        };
    const _OPTIONS_FONT_ = {
            font: {
                size: 10,
                weight: 'bold'
            }
        };
    const _OPTIONS_COLOR_ = {
            color: ({dataset}) =>  dataset.borderColor,
        };
    // const _OPTION_BUBBLED_ = {
    //         backgroundColor: ({dataset}) =>  dataset.backgroundColor,
    //         borderRadius: 10,
    //         borderWidth: 1,
    //         borderColor: ({dataset}) =>  dataset.borderColor,
    //     };
    const _OPTIONS_PIE_ = {
            plugins: {
                datalabels: {
                    ..._OPTIONS_DISPLAY_,
                    ..._OPTIONS_COLOR_,
                    ..._OPTIONS_FONT_
                }
            }
        };
    const _OPTIONS_LINE_ = {
            elements: { line: { tension: 0 } }, // Sólo para "Line"
            legend: {
                display: false //sin labels en Chartjs
            },   
            plugins: {
                datalabels: {
                    anchor: 'end',
                    align: 'top',
                    offset: 0,
                    // ..._OPTION_BUBBLED_,
                    ..._OPTIONS_COLOR_,
                    ..._OPTIONS_DISPLAY_,
                    ..._OPTIONS_FONT_
                },
            }
        };

    export default {
        components: {
            ChartDataLabels
        },
        props: {
            data: {
                type: [Object, Array],
                required: true
            },
            title: {
                type: String,
                required: true
            },
            types: {
                type: Array,
                default: () => _CHART_TYPES_,
                validator: value => value.every(val => _CHART_TYPES_.includes(val))
            },
            charts: {
                type: Array,
                default: () => [
                    { 
                       chart: 'Bar',
                       icon: 'mdi-chart-bar',
                       options: _OPTIONS_LINE_,
                    }, 
                    { 
                       chart: 'Line',
                       icon: 'mdi-chart-line',
                       options: _OPTIONS_LINE_,
                    }, 
                    { 
                       chart: 'Pie',
                       icon: 'mdi-chart-pie',
                       options: _OPTIONS_PIE_,
                    }, 
                    { 
                       chart: 'Donut',
                       icon: 'mdi-chart-donut',
                       options: _OPTIONS_PIE_,
                    }, 
                    { 
                       chart: 'Bubble',
                       icon: 'mdi-chart-bubble',
                       options: null,
                    }, 
                    { 
                       chart: 'PolarArea',
                       icon: 'mdi-chart-donut-variant',
                       options: null,
                    }, 
                    { 
                       chart: 'Radar',
                       icon: 'mdi-radar',
                       options: null,
                    } 
                ]
            },
            iconSettings: {
                type: String,
                default: 'mdi-settings-outline'
            }
        },
        data () {
            return {
                menu: false,
                chartType: this.types[0],
                chartOptions: this.chartByType(this.types[0]).options,
            }
        },
        computed : {
            component () {
                const type = this.chartType;
                return () => import(`~/components/ItaChartjs${type}`)
            },
            chartsEnabled () {
                return this.types.map(this.chartByType)
            }
        },
        methods: {
            selectChart (chart, options) {
                this.chartType = chart;
                this.chartOptions = options;
            },
            chartByType (type) {
                return this.charts.filter(c => c.chart === type)[0]
            }
        }
    }
</script>
