<template>
    <v-row class="px-5 pb-12">
        <v-col class="pa-0">
            <v-row>
                <v-col cols="auto" class="py-0">
                    <h2 class="title">
                        Filtros aplicados:
                    </h2>
                </v-col>
                <v-col cols="auto" class="py-0">
                    <span class="subtitle-2">por rango de Fechas:</span>
                    <ita-filter-datepicker 
                        :disabled="$store.state.isBusy" 
                        @change="applyFilter($event, 'date_start', 'range')"
                    />
                </v-col>
                <v-col style="border-left:1px solid #ddd" class="py-0">
                    <span class="subtitle-2">por Marco<sup class="grey--text">interacciones</sup> :</span>
                    <ita-filter-chip-group
                        :items="$store.getters['facet/interactions.frame']"
                        multiple
                        :disabled="$store.state.isBusy"
                        @change="applyFilter($event, 'interactions.frame')"
                    />
                </v-col>
                 <v-col cols="auto" style="border-left:1px solid #ddd" class="py-0">
                    <span class="subtitle-2">por Evaluación<sup class="grey--text">sesiones</sup> :</span>
                    <ita-filter-chip-group
                        :items="$store.getters['facet/score']"
                        :disabled="$store.state.isBusy"
                        @change="applyFilter($event, 'score')"
                    />
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="7">
                    <h2 class="headline">
                        <span class="primary--text">{{ $store.getters.count_sessions }}</span> 
                        Sesiones:
                    </h2>
                    <v-row>
                        <v-col cols="4">
                            <ita-chartjs 
                                :data="$store.getters['dashboard/chartjs_dayofweek']" 
                                title="Por día semanal" 
                                :types="['Bar', 'Line']"
                            />
                        </v-col>
                        <v-col cols="4">
                            <ita-chartjs 
                                :data="$store.getters['dashboard/chartjs_hour']" 
                                title="Por hora"
                                :types="['Bar', 'Line']"
                            />
                        </v-col>
                        <v-col cols="4">
                            <ita-chartjs 
                                :data="$store.getters['dashboard/chartjs_score']" 
                                title="Evaluadas" 
                                :types="['Donut', 'Pie', 'Bar']"
                            />
                        </v-col>
                    </v-row>
                </v-col>
                <v-col cols="5" style="border-left:1px solid #ddd">
                    <h2 class="headline">
                        <span class="primary--text">{{ $store.getters.count_interactions }}</span>
                        Interacciones:
                    </h2>
                    <v-row>
                        <v-col cols="6">    
                            <ita-chartjs 
                                :data="$store.getters['dashboard/chartjs_misunderstood']" 
                                title="Respondidas" 
                                :types="['Pie', 'Donut', 'Bar']"
                            />
                        </v-col>
                        <v-col cols="6">    
                            <ita-chartjs
                                :data="$store.getters['dashboard/chartjs_frame']" 
                                title="Marcos" 
                                :types="['Pie', 'Donut', 'Bar']"
                            />
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
            <v-row>
                 <v-col>
                    <h3 class="headline">
                        Listado de <span class="primary--text">{{ $store.getters.count_sessions }}</span> Sesiones...<small>
                        (y sus <span class="primary--text">{{ $store.getters.count_interactions }}</span> interacciones)</small>
                    </h3>
                    <v-data-table
                        :headers="$store.getters['dashboard/datatable_list'].headers"
                        :items="$store.getters['dashboard/datatable_list'].items"
                        item-key="session_id"
                        class="elevation-1"
                        show-expand
                        single-expand
                        :expanded.sync="expanded"
                        dense
                        @item-expanded="openInteractions"
                    >
                        <template #item="{ item, isSelected, isExpanded, expand }">
                            <tr 
                                :class="{'blue-grey lighten-4': isExpanded}"
                                style="cursor:pointer"
                                @click="expand(!isExpanded)"
                                >
                                <td>
                                    <v-icon>mdi-chevron-{{ isExpanded ? 'down': 'right' }}</v-icon>
                                </td>
                                <!-- <td>{{ item.session_id }}</td> -->
                                <td class="text-center">{{ new Date(item.date).toLocaleDateString() }}</td>
                                <td class="text-center">{{ new Date(item.time_start).toLocaleTimeString() }}</td>
                                <td class="text-center">{{ new Date(item.time_end).toLocaleTimeString() }}</td>
                                <td class="text-right">{{ (item.duration - (item.timeout && item.duration > 600 ? 600 : 0)).toFixed(2) }}</td>
                                <td class="text-center">
                                    <v-icon 
                                        small 
                                        :class="item.timeout ? 'error--text' : 'grey--text text--lighten-1'"
                                        :title="item.timeout ? 'Conversación terminada automáticamente por inacción del usuario' : 'Conversación terminada por usuario'"
                                        >
                                        {{ item.timeout ? "mdi-timer-sand-full" : "mdi-timer-sand-empty" }}
                                        {{ item.timeout ? '': '' }}
                                    </v-icon>
                                </td>
                                <td class="text-center">
                                    <v-icon v-if="item.score === 10" title="evaluada como Buena por el usuario" class="success--text">mdi-emoticon-happy-outline</v-icon>
                                    <v-icon v-else-if="item.score === 0" title="evaluada como Normal por el usuario" class="warning--text">mdi-emoticon-neutral-outline</v-icon>
                                    <v-icon v-else-if="item.score === -10" title="evaluada como Mala por el usuario" class="error--text">mdi-emoticon-sad-outline</v-icon>
                                    <!-- <span v-else>-</span> -->
                                </td>
                                <td class="text-center">{{ item.count_interactions }}</td>
                                <td class="text-center">
                                    <span v-if="item.count_misunderstood" class="font-weight-black" :title="`${item.count_misundertood} interaccion/es no comprendidas por el Bot`">
                                        {{ item.count_misunderstood }} <v-icon small class="error--text">mdi-comment-question-outline</v-icon>
                                    </span>
                                </td>
                            </tr>
                        </template>
                        <template v-slot:expanded-item="{ headers, item }">
                            <td :colspan="headers.length" class="px-0">
                                <v-tabs>
                                    <v-tab>
                                        <v-icon left>mdi-chat</v-icon>
                                        Chat
                                    </v-tab>
                                    <v-divider vertical />
                                    <v-tab>
                                        <v-icon left>mdi-code-braces</v-icon>
                                        JSON
                                    </v-tab>
                                    <v-tab-item class="px-4 pb-12 elevation-5">
                                        <div 
                                            v-if="interactions_selected.length === 0"
                                            class="primary--text title text-center pt-12"
                                            >
                                            <v-icon large class="primary--text">mdi-spin mdi-timer-sand</v-icon> descargando interacciones...
                                        </div>
                                        <v-row 
                                            v-for="(interaction, index) in interactions_selected /*item.interactions*/"
                                            :key="item.session_id+'_'+index"
                                            style="max-width:900px;margin:0 auto"
                                            >
                                            <v-col cols="12" class="pb-0">
                                                <v-icon small>
                                                    mdi-clock-outline
                                                </v-icon>
                                                {{ new Date(interaction.date_user).toLocaleTimeString() }}
                                            </v-col>
                                            <v-col offset="3" class="pt-0">
                                                <div class="story-bubble story-bubble-right bgcolor-o05 elevation-5">
                                                    <div class="float-right">
                                                        <v-chip v-for="({entity, value}, i) in interaction.entities" :key="item.session_id+'_entity_'+ i" small class="pl-2" >
                                                            <v-avatar left color="light-blue lighten-2">Ent</v-avatar> {{ entity }} : {{ value }}
                                                        </v-chip>
                                                        <v-chip small class="pl-2" title="Intención">
                                                            <v-avatar left size="23" color="lime">Int</v-avatar> {{ interaction.intent }}
                                                        </v-chip>
                                                        <v-chip small class="pl-2" title="Marco">
                                                            <v-avatar left color="orange">Mar</v-avatar> {{ interaction.frame }}
                                                        </v-chip>
                                                    </div>
                                                    <small class="grey--text">User</small>
                                                    <br>
                                                    {{ interaction.input_user }}
                                                </div>
                                            </v-col>
                                            <v-col cols="9" class="pa-0">
                                                <div class="story-bubble story-bubble-left bgcolor-o1 elevation-5">
                                                    <small class="grey--text">Bot</small>
                                                    <br>
                                                    <div 
                                                        style="white-space:pre-wrap" 
                                                        v-html="linkify(interaction.output_bot)" 
                                                    />
                                                </div>
                                            </v-col>
                                        </v-row>
                                    </v-tab-item>
                                    <v-tab-item class="px-4 pb-4 elevation-5">
                                        <vue-json-pretty 
                                            :data="interactions_selected/*item.interactions*/"
                                            show-length
                                            highlight-mouseover-node
                                            style="word-break:break-all"
                                        />
                                    </v-tab-item>
                                </v-tabs>
                            </td>
                        </template>
                    </v-data-table>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
    import VueJsonPretty from 'vue-json-pretty';
    import linkify from '~/components/eme-linkify.js';

    import ItaChartjs          from '~/components/ItaChartjs';
    import ItaFilterChipGroup  from '~/components/ItaFilterChipGroup';
    import ItaFilterDatepicker from '~/components/ItaFilterDatepicker';

    export default {
        components: {
            ItaChartjs,
            ItaFilterChipGroup,
            ItaFilterDatepicker,
            VueJsonPretty,
        },
        async fetch ({
            store,
            params
        }) {
            await store.dispatch("GET",['dashboard']);
        },
        data () {
            return {
                // idchat: null,
                // interactions: "",
                expanded: [],
                interactions_selected: []
            };
        },
        methods: {
            async applyFilter (values = [], facetName, operator = 'or') {
                if (values.length > 0) {
                    this.$store.dispatch("SETKEY", {
                        item: "filters", 
                        key: facetName, 
                        value: {
                            values,
                            operator
                        }
                    })
                } else {
                    const newFILTER = JSON.parse(JSON.stringify(this.$store.state.filters));
                    newFILTER[facetName] = undefined; // delete newFILTER[facetNAME]
                    this.$store.dispatch("SET", ['filters', newFILTER])
                }
                // console.warn(JSON.stringify(this.$store.state.filters, null, 4));
                await this.$store.dispatch("ADD", ['dashboard', this.$store.state.filters])
            },
            async openInteractions ({item, value}) {
                if (value){ 
                    this.interactions_selected = [];
                    // grabo en store: "sessionId"
                    this.$store.dispatch("SET", ['sessionId', item.session_id]);
                    // console.warn( 'openInteractions', item, value, item.session_id, this.$store.state.sessionId);
                    await this.$store.dispatch("GET", ['session_interactions']);
                    this.interactions_selected = this.$store.state.session_interactions;
                }
            },
            linkify: text => linkify(text)
        }
    };

</script>

<style>
    .story-bubble{
            border-radius:.75em;
            padding: .25em .85em;
            position: relative;
            font-size: 1rem;
        }
            .story-bubble-right{
                border-bottom-right-radius: 0;
            }
            .story-bubble-left{
                border-bottom-left-radius: 0;
            }
    .bgcolor-o02              { background-color: rgba(0,0,0,.035); }
    .theme--dark .bgcolor-o02 { background-color: rgba(255,255,255,.035); }
    .bgcolor-o05              { background-color: rgba(0,0,0,.075); }
    .theme--dark .bgcolor-o05 { background-color: rgba(255,255,255,.075); }
    .bgcolor-o1               { background-color: rgba(0,0,0,.175); }
    .theme--dark .bgcolor-o1  { background-color: rgba(255,255,255,.175); }

    .v-data-table tbody tr.v-data-table__expanded__content {
        box-shadow: none;
    }
</style>
