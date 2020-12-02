import Vue from 'vue';

// -----------------------------------------------------------------
// GENERICOS
// -----------------------------------------------------------------
const _URL_PROXY_ = `/api` // from "nuxt.config.js"

const _GET_REGEX = new RegExp("\\[([^\\[\\]]*)\\]", "g"); //-- /\[([^\[\]]*)\]/g
// https://www.30secondsofcode.org/snippet/get
// const _GET = (from, ...selectors) =>
//     [...selectors].map(s =>
//       s
//         .replace(_GET_REGEX, '.$1.')
//         .split('.')
//         .filter(t => t !== '')
//         .reduce((prev, cur) => prev && prev[cur], from)
//     );
const _GET = (from, selector, valueDefault) =>
    selector
        .replace(_GET_REGEX, '.$1.')
        .split('.')
        .filter(t => t !== '')
        .reduce((prev, cur) => prev && prev[cur], from) || valueDefault;
// -----------------------------------------------------------------------------
// STATE
//
export const state = () => ({
    projects: [],
    projectId: '', // id of project selected

    models: [],
    modelId: '', // id of model selected

    stories: [],
    storyId: '', // id of story selected

    interactions: [],
    interactionId: '', // id of interaction selected

    intents: [],
    intentId: '', // id of intent selected

    entities: [],
    entityId: '', // id of entity selected

    values: [],
    valueId: '', // id of value selected

    templates: [],
    templateId: '', // id of template selected

    examples: [],
    recommendations: [],

    actions: [],

    chatUser: '', // texto que envía el usuario...
    chatBot: { answer: [] }, // texto que calcula el bot...

    train: {},
    training: {
        is_training: false,
    },

    notification: {
        type: 'success', // error | warning | success | info
        message: ''
    },

    isBusy: false,
    //---------------------------------------------------------------------------
    dashboard: {
        count_sessions: [{}],
        count_interactions: [{}],
        facet_interactions_per_misunderstood: [],
        facet_sessions_per_score: [],
        facet_interactions_per_frame: []
    },
    sessionId: '',
    session_interactions: [],
    // filtros para MongoDB como "$match"
    filters: {
        
    }
});
// -----------------------------------------------------------------------------
// GETTER > COMPUTED
//
// const SORTBY = (o, key) => [...o].sort((a, b) => a[key] > b[key] ? 1 : a[key] < b[key] ? -1 : 0);

const SORTBY_UNCASE = (o, key) => [...o].sort((a, b) => {
            const _a = a[key].toLowerCase();
            const _b = b[key].toLowerCase();
            return _a > _b ? 1 : _a < _b ? -1 : 0 
        });

const getById = function ( itemId, items){
        return  state => state[itemId] && state[items]
            ? state[items].find(i => i.id === state[itemId])
            : {}
    };
const _LABELS = {
        "score": { 
            "10": "Bueno", 
            "0": "Normal", 
            "-10": "Malo", 
            "null": "no evaluados" 
        },
        "frame": {
            "farming": "Agricultura",
            "citizensinfo": "Ciudadanía",
            "Unknown": "¿?",
            "aragon": "Aragón",
            "tourism": "Turismo",
            "transport": "Transporte"
        },
        "dayofweek":  [
            "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"
        ],
        "hours": [
            "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", 
            "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00" 
        ],
        "misunderstood": {
            "true": "No entendidas",
            "false": "Entendidas"
        }
    };
const _GETLABEL = (hashMap, value) => String(value) in hashMap ? hashMap[value] : value;

export const getters = {
    models:    state => SORTBY_UNCASE(state.models,    'name'),
    stories:   state => SORTBY_UNCASE(state.stories,   'name'),
    intents:   state => SORTBY_UNCASE(state.intents,   'name'),
    entities:  state => SORTBY_UNCASE(state.entities,  'name'),
    templates: state => SORTBY_UNCASE(state.templates, 'name'),
    values:    state => SORTBY_UNCASE(state.values,    'name'),
    examples:  state => SORTBY_UNCASE(state.examples,  'text'),
    actions:   state => [...state.actions].sort(), // sort es mutable...
    
    // selected project by id
    // project: state => state.projectId
    //     ? state.projects.find(e => e.id === state.projectId)
    //     : {},
    project:     getById('projectId',     'projects'),
    model:       getById('modelId',       'models'),
    story:       getById('storyId',       'stories'),
    entity:      getById('entityId',      'entities'),
    intent:      getById('intentId',      'intents'),
    value:       getById('valueId',       'values'),
    template:    getById('templateId',    'templates'),
    interaction: getById('interactionId', 'interactions'),

    api (state, getters){
        return {
            projects:    `/projects`,
            models:      `/projects/${state.projectId}/models`,
            chatBot:     `/projects/${state.projectId}/models/${state.modelId}/chats`,
            score:       `/projects/${state.projectId}/models/${state.modelId}/score`,
            stories:     `/projects/${state.projectId}/models/${state.modelId}/stories`,
            interactions:`/projects/${state.projectId}/models/${state.modelId}/stories/${state.storyId}/interactions`,
            train:       `/../exec/projects/${state.projectId}/models/${state.modelId}/train`,
            training:    `/projects/${state.projectId}/models/${state.modelId}/training`,
            intents:     `/projects/${state.projectId}/models/${state.modelId}/intents`,
            entities:    `/projects/${state.projectId}/models/${state.modelId}/entities`,
            values:      `/projects/${state.projectId}/models/${state.modelId}/entities/${state.entityId}/values`,
            templates:   `/projects/${state.projectId}/models/${state.modelId}/intents/${state.intentId}/templates`,
            examples:    `/projects/${state.projectId}/models/${state.modelId}/intents/${state.intentId}/templates/${state.templateId}/examples`,
            recommendations: `/recommender/intents/${(getters.interaction || {}).text}`,
            actions:     `/actions`,
            //----------------------------------------------------------------------
            dashboard:   `/aggregation/count_sessions,count_interactions,facet_sessions_per|isoDayOfWeek,facet_sessions_per|hour,facet_interactions_per_misunderstood,facet_sessions_per_score,facet_interactions_per_frame,sessions`,
            session_interactions: `/aggregation/interactions|${state.sessionId}`,
        }
    },
    //------------------------------------------------------------------------------------------------------
    // "facet_sessions_per|isoDayOfWeek"
    "dashboard/chartjs_dayofweek": state => {
        const data = _LABELS.dayofweek.map((d, i) => {
            const dayOfWeek = _GET(state, 'dashboard.facet_sessions_per|isoDayOfWeek', []).filter(o => o._id === i+1)[0];
            return dayOfWeek ? dayOfWeek.count : 0
        })
        return {
            "labels": _LABELS.dayofweek,
            "datasets": [{
                "label": "Nº de sesiones",
                data ,
                "backgroundColor": "#BBDEFB",// ["#BBDEFB", "#C5CAE9", "#D1C4E9", "#FFE0B2", "#B2EBF2", "#C8E6C9", "#D7CCC8", "#CFD8DC", "#DCEDC8", "#F0F4C3", "#B3E5FC", "#B2DFDB", "#FFCCBC", "#FFF9C4", "#E1BEE7", "#F8BBD0", "#FFCDD2", "#FFECB3"],
                "borderColor": "#2196F3", //["#2196F3", "#3F51B5", "#673AB7", "#FF9800", "#00BCD4", "#4CAF50", "#795548", "#607D8B", "#8BC34A", "#CDDC39", "#03A9F4", "#009688", "#FF5722", "#FFEB3B", "#9C27B0", "#E91E63", "#F44336", "#FFC107"],
                "borderWidth": 1,
                //----------------------------------------------------
                "fill": false
            }]
        }
    },
    // "facet_sessions_per|hour"
    "dashboard/chartjs_hour": state => {
        const data = _LABELS.hours.map((d, i) => {
            const hour = _GET(state, 'dashboard.facet_sessions_per|hour', []).filter(o => o._id === i)[0];
            return hour ? hour.count : 0
        })
        return {
            "labels": _LABELS.hours,
            "datasets": [{
                "label": "Nº de sesiones",
                data,
                "backgroundColor": "#BBDEFB",// ["#BBDEFB", "#C5CAE9", "#D1C4E9", "#FFE0B2", "#B2EBF2", "#C8E6C9", "#D7CCC8", "#CFD8DC", "#DCEDC8", "#F0F4C3", "#B3E5FC", "#B2DFDB", "#FFCCBC", "#FFF9C4", "#E1BEE7", "#F8BBD0", "#FFCDD2", "#FFECB3"],
                "borderColor": "#2196F3", //["#2196F3", "#3F51B5", "#673AB7", "#FF9800", "#00BCD4", "#4CAF50", "#795548", "#607D8B", "#8BC34A", "#CDDC39", "#03A9F4", "#009688", "#FF5722", "#FFEB3B", "#9C27B0", "#E91E63", "#F44336", "#FFC107"],
                "borderWidth": 1,
                //----------------------------------------------------
                "fill": false
            }]
        }
    },

    "count_interactions": state => _GET(state, 'dashboard.count_interactions[0].count', 0),
    "count_sessions":     state => _GET(state, 'dashboard.count_sessions[0].count', 0),

    // "facet_interactions_per_misunderstood" & "count_interactions"
    "dashboard/chartjs_misunderstood": state => {
        const ITEMS = _GET(state, 'dashboard.facet_interactions_per_misunderstood', []);
        const labels = ITEMS.map(o => _GETLABEL( _LABELS.misunderstood, o._id));
        const data   = ITEMS.map(o => o.count)
        return {
            labels,
            "datasets": [{
                //"label": "",
                data,
                "backgroundColor": ["#C5CAE9", "#D1C4E9"], // "#FFE0B2", "#B2EBF2", "#C8E6C9", "#D7CCC8", "#CFD8DC", "#DCEDC8", "#F0F4C3", "#B3E5FC", "#B2DFDB", "#FFCCBC", "#FFF9C4", "#E1BEE7", "#F8BBD0", "#FFCDD2", "#FFECB3"],
                "borderColor": ["#3F51B5", "#673AB7"], // "#FF9800", "#00BCD4", "#4CAF50", "#795548", "#607D8B", "#8BC34A", "#CDDC39", "#03A9F4", "#009688", "#FF5722", "#FFEB3B", "#9C27B0", "#E91E63", "#F44336", "#FFC107"],
                "borderWidth": 1
            }]
        }
    },
    "dashboard/chartjs_score": state => {
        const ITEMS = _GET(state, 'dashboard.facet_sessions_per_score', []);
        const labels = ITEMS.map(o => _GETLABEL( _LABELS.score, o._id));
        const data   = ITEMS.map(o => o.count)
        return {
            labels,
            "datasets": [{
                //"label": "",
                data, //[ ...data, total_sessions_unscored ],
                "backgroundColor": ["#ffcdd2", "#fff9c4", "#c8e6c9", "#cfd8dc"], // "#FFE0B2", "#B2EBF2", "#C8E6C9", "#D7CCC8", "#CFD8DC", "#DCEDC8", "#F0F4C3", "#B3E5FC", "#B2DFDB", "#FFCCBC", "#FFF9C4", "#E1BEE7", "#F8BBD0", "#FFCDD2", "#FFECB3"],
                "borderColor": ["#f44336", "#ffeb3b", "#4caf50", "#607d8b"], // "#FF9800", "#00BCD4", "#4CAF50", "#795548", "#607D8B", "#8BC34A", "#CDDC39", "#03A9F4", "#009688", "#FF5722", "#FFEB3B", "#9C27B0", "#E91E63", "#F44336", "#FFC107"],
                "borderWidth": 1
            }]
        }
    },
    "dashboard/chartjs_frame": state => {
        // const total_interactions = getters.count_interactions;
        const ITEMS = _GET(state, 'dashboard.facet_interactions_per_frame', []);
        const labels = ITEMS.map(o => _GETLABEL( _LABELS.frame, o._id));
        const data   = ITEMS.map(o => o.count)
        return {
            labels,
            "datasets": [{
                //"label": "",
                data,
                "backgroundColor": ["#FFE0B2", "#B2EBF2", "#C8E6C9", "#D7CCC8", "#CFD8DC", "#DCEDC8", "#F0F4C3", "#B3E5FC", "#B2DFDB", "#FFCCBC", "#FFF9C4", "#E1BEE7", "#F8BBD0", "#FFCDD2", "#FFECB3"],
                "borderColor": ["#FF9800", "#00BCD4", "#4CAF50", "#795548", "#607D8B", "#8BC34A", "#CDDC39", "#03A9F4", "#009688", "#FF5722", "#FFEB3B", "#9C27B0", "#E91E63", "#F44336", "#FFC107"],
                "borderWidth": 1
            }]
        }
    },
    "dashboard/datatable_list": state => {
        const ITEMS = _GET(state, 'dashboard.sessions', []);
        return {
            headers: [
                { text: ' ',                 value: 'data-table-expand' },
                // { text: 'Id Sesión',        align: 'left',   value: 'session_id', sortable: false },
                { text: 'Fecha',            align: 'center',  value: 'date' },
                { text: 'Hora Inicio',      align: 'center',  value: 'time_start', sortable: false },
                { text: 'Hora Fin',         align: 'center',  value: 'time_end', sortable: false },
                { text: 'Duración útil (sg)',    align: 'right',  value: 'duration' },
                { text: 'Timeout',          align: 'center', value: 'timeout' },
                { text: 'Evaluación',       align: 'center', value: 'score' },
                { text: 'Interacciones',    align: 'center', value: 'count_interactions' },
                { text: 'No entendidos',    align: 'center', value: 'count_misunderstood' },
                // { text: 'Adaptado Visual',   align: 'center', value: 'adaptado_visual' },
                // { text: 'Adaptado Auditivo', align: 'center', value: 'adaptado_auditivo' }
            ],
            items: ITEMS.map(({session_id, date_start, date_end, /*interactions,*/ is_timeout, count_interactions, count_misunderstood, score = null}) => ({
                session_id,
                "timeout":    is_timeout,
                "date":       date_start,
                "time_start": date_start,
                "time_end":   date_end, // interactions[interactions.length -1].date_bot,
                "duration":   (new Date(date_end) - new Date(date_start)) / 1000,
                //"count_interactions": interactions.length,
                count_interactions,
                count_misunderstood,
                // "count_misunderstood2": interactions.filter(item => item.is_misunderstood).length,
                // interactions,
                "score":  score == null ? -11 : score,
            }))
        }
    },
    "facet/interactions.frame": state => {
        const ITEMS = _GET(state, 'dashboard.facet_interactions_per_frame', []);
        return ITEMS.map(({ count, _id: value}) => ({
            count,
            label:  _GETLABEL( _LABELS.frame, value), 
            value
        }))
    },
    "facet/score": state => {
        const ITEMS = _GET(state, 'dashboard.facet_sessions_per_score', []);
        return ITEMS.map(({ count, _id: value}) => ({
            count,
            label: _GETLABEL( _LABELS.score, value), 
            value
        }))
    },
}

let RESET = {
        templates:    ['templates', 'templateId', 'examples'],
        values:       ['values', 'valueId'],
        interactions: ['interactions', 'interactionId'],
    }
    RESET = {
        ...RESET,
        intents:  ['intents',  'intentId', ...RESET.templates],
        entities: ['entities', 'entityId', ...RESET.values],
        stories:  ['stories',  'storyId',  ...RESET.interactions],
    }
    RESET = {
        ...RESET,
        models: ['models', 'modelId', ...RESET.stories, ...RESET.entities, ...RESET.intents],
    }
    RESET = {
        ...RESET,
        projects: ['projects', 'projectId', ...RESET.models]
    }
// -----------------------------------------------------------------------------
// ACTIONS > ASYNCHRONOUS TRANSACTIONS
//
/*
** definido en 'nuxt.config.js'
** sustituido por 'axios.baseURL/axios.browserBaseURL'
*/
export const actions = {
    async GET ({ commit, dispatch, getters }, [items, toReset = false] ){
        commit('set', ['isBusy', true]);
        try {
            // intento conseguir datos...
            const {data} = await this.$axios.get( _URL_PROXY_ + getters.api[items] );
            // reseteo primero, si lo pido y existe...
            if (toReset && items in RESET){
                await dispatch('RESET', RESET[items]);
            }
            // asigno datos traidos...
            commit('set', [items, data]);
        } catch (error) {
            dispatch('NOTIFICATION_ERROR', error);
        }
        commit('set', ['isBusy', false]);
    },
    async ADD ({ commit, dispatch, getters }, [items, item] ){
        commit('set', ['isBusy', true]);
        try {
            const {data} = await this.$axios.post(  _URL_PROXY_ + getters.api[items], item );
            await commit('set', [items, data]);
        } catch (error) {
            dispatch('NOTIFICATION_ERROR', error);
        }
        commit('set', ['isBusy', false]);
    },
    async DELETE ({ commit, dispatch, getters }, [items, itemId, toReset = false]){
        commit('set', ['isBusy', true]);
        try {
            const {data} = await this.$axios.delete(`${_URL_PROXY_ + getters.api[items]}/${itemId}`);
            // reseteo primero, si lo pido y existe...
            if (toReset && items in RESET){
                await dispatch('RESET', RESET[items]);
            }
            // asigno datos traidos...
            commit('set', [items, data]);
        } catch (error) {
            dispatch('NOTIFICATION_ERROR', error);
        }
        commit('set', ['isBusy', false]);
    },
    async PATCH ({ commit, dispatch, getters }, [items, item]){
        commit('set', ['isBusy', true]);
        try {
            const {data} = await this.$axios.patch(`${_URL_PROXY_ + getters.api[items]}/${item.id}`, item);
            await commit('set', [items, data]);
            await commit('set', ['notification', {
                type: 'success', 
                message: `OK - ${items} changed and saved!`
            }])
        } catch (error) {
            dispatch('NOTIFICATION_ERROR', error);
        }
        commit('set', ['isBusy', false]);
    },
    SET ({ commit }, o){
        commit('set', o);
    },
    SETKEY ({ commit }, o){
        commit('setkey', o );
    },
    RESET ({ dispatch, state }, arrItems){
        arrItems.forEach(i => {
            if (i in state) {
                dispatch('SET',[i, Array.isArray(state[i]) ? [] : '']);
            }
        });
    },
    NOTIFICATION_ERROR ({ commit }, error){
        if (error && 'response' in error){
            const { status, statusText, config } = error.response;
            commit('set', ['notification', {
                type: 'error', 
                message: `${status} - ${statusText}: ${config.url}`
            }])
        }
    },
    NOTIFICATION_RESET ({ commit }){
        commit('set', ['notification', '', 'message'])
    }
}
// -----------------------------------------------------------------------------
// MUTATIONS > SYNCHRONOUS TRANSACTIONS
//
export const mutations = {
    set ( state,[dataName, data, key]){
        state[dataName] = key ? data[key] : data;
    },
    setkey ( state, {item, key, value} ){
        //item[key] = value; // no reactive !!!!
        //item = { ...item, [key]: value} // no reactive !!!!
        // item puede ser un <object>Reactivo, no un <string>Nombre
        Vue.set(state[item] || item, key, value);
    },
}
