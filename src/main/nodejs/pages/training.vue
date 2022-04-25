<template>
    <v-row class="fill-height" no-gutters>
        <v-col cols="12" sm="2" class="fill-height" :class="{'hideProjects': projects.length <= 1}">
            <!-- <v-toolbar-title>
                <span v-show="'name' in project">
                    <span class="caption lime--text text--darken-4">
                        1. Project
                    </span>
                    <v-chip
                        label
                        small
                        color="lime darken-4"
                        dark
                    >
                        {{ project.name }}
                    </v-chip>
                    <v-icon>mdi-arrow-right</v-icon>
                </span>
                <span v-show="'name' in model">
                    <span class="caption lime--text text--darken-3">
                        2. Model
                    </span>
                    <v-chip
                        label
                        small
                        color="lime darken-3"
                        dark
                    >
                        {{ model.name }}
                    </v-chip>
                    <v-icon>mdi-arrow-right</v-icon>
                </span>
                <span v-show="'name' in story">
                    <span class="caption lime--text text--darken-2">
                        3. Story
                    </span>
                    <v-chip
                        label
                        color="lime darken-2"
                        dark
                        small
                    >
                        {{ story.name }}
                    </v-chip>

                    <v-icon>mdi-arrow-right</v-icon>
                </span>
                <span class="primary--text">
                    {{ $route.path.slice(1) }}
                    <v-icon class="primary--text">mdi-arrow-down</v-icon>
                </span>
            </v-toolbar-title> -->
            <ita-card-list
                class="mcb-projects"
                toolbar-color="blue lighten-2"
                toolbar-icon="mdi-numeric-0-box"
                title="Projects"
                :names="['project','projects']"
                store-items="projects"
                store-item-id="projectId"
                item-children="models_length"
                @onItemSelected="onProjectSelected"
                @onError="NOTIFICATION_ERROR"
            />

            <ita-card-list
                class="mcb-models"
                toolbar-color="blue lighten-2"
                toolbar-icon="mdi-numeric-1-box"
                title="Models"
                :names="['model','models']"
                store-items="models"
                store-item-id="modelId"
                item-children="stories_length"
                :show-add="projectId!==''"
                @onItemSelected="onModelSelected"
                @onError="NOTIFICATION_ERROR"
                >
                <template #prependContent="{ item }">
                    <v-btn 
                        x-small 
                        :title="`test chat: '${item.name}'`"
                        class="mr-2"
                        @click="chat_dialog = true"
                        >
                        <v-icon small>
                            mdi-chat
                        </v-icon>
                    </v-btn>
                </template>
                <template #appendContent="{ item }">
                    <v-chip 
                        v-if="item.last_trained_timestamp" 
                        class="caption float-right" 
                        small 
                        pill
                        outlined
                        title="last trained"
                        >
                        <v-avatar left class="mr-0">
                            <v-icon left class="mr-0">
                                mdi-clock-outline
                            </v-icon>
                        </v-avatar>
                        {{ new Date(item.last_trained_timestamp).toLocaleString() }}
                    </v-chip>
                </template>
            </ita-card-list>

            <ita-card-list
                class="mcb-stories"
                toolbar-color="blue lighten-2"
                toolbar-icon="mdi-numeric-2-box"
                title="Rules"
                :names="['story','stories']"
                store-items="stories"
                store-item-id="storyId"
                item-children="interactions_length"
                :show-add="modelId!==''"
                @onItemSelected="onStorySelected"
                @onError="NOTIFICATION_ERROR"
                >
                <template #appendMenu="{ hover }">
                    <!-- <ita-btn-icon
                        v-show="hover"
                        title="Create and Download files"
                        :icon="isDownloading ? `mdi-spin mdi-cog` : `mdi-download`"
                        color="error"
                        class="ml-2"
                        :disabled="isDownloading"
                        @action="downloadModel()"
                    /> -->
                    <ita-btn-icon
                        v-show="hover && enabledTraining"
                        title="Create and Download files"
                        :icon="isDownloading ? `mdi-spin mdi-cog` : `mdi-download`"
                        color="error"
                        class="ml-2"
                        :href="`${$config.base}/api/projects/download`"
                        :disabled="isDownloading"
                        @action="downloadingModel()"
                    />
                    <!-- <ita-btn-icon
                        :show-btn="hover && enabledTraining"
                        :tooltip="`Train model: '${model.name}'`"
                        icon="mdi-wrench"
                        color="error"
                        :disabled="isTraining"
                        @action="trainModel()"
                    />
                    <v-progress-circular
                        v-if="isTraining"
                        indeterminate
                        color="error"
                        title="is Training!!"
                    >
                        <v-icon small>
                            mdi-wrench
                        </v-icon>
                    </v-progress-circular> -->
                </template>
            </ita-card-list>
        </v-col>
        <v-col cols="12" sm="3" class="fill-height">
            <ita-training
                class="mcb-story"
                toolbar-color="blue lighten-1"
                toolbar-icon="mdi-numeric-3-box"
                :intents="intents"
                :disabled="!storyId"
                title="Training model"
                :names="['interaction','interactions']"
                store-items="interactions"
                @onError="NOTIFICATION_ERROR"
            />
        </v-col>
        <v-col cols="12" sm="3" class="fill-height">
            <ita-card-list
                class="mcb-intents"
                toolbar-color="blue"
                toolbar-icon="mdi-numeric-4-box"
                title="Intents"
                :names="['intent','intents']"
                store-items="intents"
                store-item-id="intentId"
                item-children="templates_length"
                :show-add="modelId!==''"
                @onItemSelected="onIntentSelected"
                @onError="NOTIFICATION_ERROR"
            />

            <ita-card-list
                class="mcb-entities"
                toolbar-color="blue"
                toolbar-icon="mdi-numeric-4-circle"
                title="Entities"
                :names="['entity','entities']"
                store-items="entities"
                store-item-id="entityId"
                item-children="values_length"
                :show-add="modelId!==''"
                @onItemAdded="onTemplateChanged"
                @onItemDeleted="onTemplateChanged"
                @onItemSelected="onEntitySelected"
                @onError="NOTIFICATION_ERROR"
            >
                <template #default="{item}">
                    <span 
                        :style="{color: item.text_color, backgroundColor: item.color}" 
                        class="px-2"
                        >
                        {{ item.name }}
                    </span>
                </template>
                <template #prependContent="{item}">
                    <v-menu 
                        v-if="item.intents" 
                        open-on-hover
                        transition="scale-transition"
                        tile
                        >
                        <template #activator="{ on }">
                            <ita-btn-icon
                                icon="mdi-filter"
                                class="mr-3"
                                :size="28"
                                :tooltip="`Intents with entity: ${item.name}`"
                                :activator="on"
                            />
                        </template>
                        <v-list>
                            <v-subheader>
                                Intents with 
                                <span 
                                    :style="{color: item.text_color, backgroundColor: item.color}" 
                                    class="px-2"
                                    >
                                    {{ item.name }}
                                </span>
                            </v-subheader>
                            <v-list-item-group>
                                <v-list-item
                                    v-for="({templates_length, id, name}) in item.intents"
                                    :key="`${item.id}_${id}`"
                                    class="minheight30"
                                    @click="$root.$emit('select_intentId', id);$root.$emit('select_entityId', item.id)"
                                    >
                                    <v-list-item-content class="py-0">
                                        <v-list-item-title>
                                            {{ name }} <sup class="grey--text">{{ templates_length }}</sup>
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list-item-group>
                        </v-list>
                    </v-menu>
                </template>
            </ita-card-list>
        </v-col>

        <v-col cols="12" sm="4" class="fill-height">
            <ita-card-list
                class="mcb-templates"
                toolbar-color="blue darken-2"
                toolbar-icon="mdi-numeric-5-box"
                title="Templates"
                :names="['template','templates']"
                store-items="templates"
                store-item-id="templateId"
                item-children="templates_length"
                :show-add="intentId!==''"
                @onItemAdded="onTemplateChanged"
                @onItemDeleted="onTemplateChanged"
                @onItemChanged="onTemplateChanged"
                @onItemSelected="onTemplateSelected"
                @onError="NOTIFICATION_ERROR"
            >
                <template #after-title>
                    <span v-if="'name' in intent" class="ml-4">of {{ intent.name }}</span>
                </template>

                <template #default="{item}">
                    <span v-html="tmplHilightEntities(item.name)" />
                </template>
            </ita-card-list>

            <ita-card-list
                class="mcb-values"
                toolbar-color="blue darken-2"
                toolbar-icon="mdi-numeric-5-circle"
                title="Values"
                :names="['value','values']"
                store-item="value"
                store-items="values"
                store-item-id="valueId"
                :show-add="entityId!==''"
                @onItemAdded="onValueChanged"
                @onItemDeleted="onValueChanged"
                @onItemChanged="onValueChanged"
                @onError="NOTIFICATION_ERROR"
            >
                <template #after-title>
                    <span v-if="'name' in entity" class="ml-4">of
                        <span
                            :style="{
                                color: entity.text_color,
                                backgroundColor: entity.color
                            }"
                            class="px-1 mx-1"
                        >
                            {{ entity.name }}
                        </span>
                        in {{ entityTotalTemplates() }} templates
                    </span>
                </template>
            </ita-card-list>
        </v-col>

        <v-dialog
            v-model="examples_dialog"
            scrollable
            max-width="600"
            transition="dialog-transition"
            content-class="tile"
            >
            <v-card class="mcb-card" tile>
                <v-card-title class="primary white--text pa-4">
                    Examples
                    <ita-num-sup :num="examples.length" :hide="0" class="text--lighten-1" />
                </v-card-title>
                <v-card-subtitle v-if="template.name" class="primary white--text">
                    {{ intent.name }} &raquo;
                    <div v-html="tmplHilightEntities( template.name )" />
                </v-card-subtitle>
                <v-list>
                    <v-list-item-group>
                        <v-list-item 
                            v-for="(item, index) in examples" 
                            :key="`examples_${index}`"
                            >
                            <v-list-item-content class="py-0">
                                <v-list-item-title
                                    class="noclickable"
                                    v-html="exampleHilightEntities(item)"
                                />
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-card>
        </v-dialog>

        <v-dialog   
            v-model="chat_dialog"
            max-width="500"
            transition="dialog-transition"
            content-class="tile"
            >
            <ita-chatbot
                :active="chat_dialog"
                :max-idle-time="600"
                toolbar-color="pink"
                toolbar-icon="mdi-chat"
                style="height:90vh"
                :title="`test Chat of model: &laquo;${model.name}&raquo;`"
                :disabled="!enabledChat"
                :label="modelId ? `Escriba su mensaje aquí...` : 'Primero seleccione un modelo'"
                @onError="NOTIFICATION_ERROR"
            />
        </v-dialog>
    </v-row>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';

    const _REGEX_ = /\${([^}]+)}/g;
    //const _REGEX_ = /\${([\w ]+)}/mg;

    // polyfill for "String.prototype.matchAll"
    // if (!("matchAll" in String.prototype)) {
    //     /** package.json > dependencies > "string.prototype.matchall": "^4.0.2", */
    //     const matchAll = require('string.prototype.matchall');
    //     matchAll.shim()
    // }

    export default {
        filters: {
            recommended ( arr = [] ){
                return arr.length ? `Intents recommended:<br/> ${arr.map(r => `<a href="#">${r}</a>`).join(', ')}` : ``;
            }
        },
        data () {
            return {
                examples_dialog: false,
                chat_dialog: false,
                isTraining: false,
                isDownloading: false,
            }
        },
        computed: {
            ...mapState([
                'projects',
                'projectId',
                'storyId',
                'modelId',

                'intentId',
                'entityId',
            ]),
            ...mapGetters([
                'project',
                'models',
                'model',
                'stories',
                'story',

                'intents',
                'intent',
                'entities',
                'entity',
                
                'templates', // sortBy 'name'
                'examples',  // sortBy 'text'
                'template',
            ]),
            idIfOneProject () {
                return this.projects.length === 1
                    ? this.projects[0].id
                    : false
                    ;
            },
            entityByName (){ // se cachea...
                return name => this.entities.find(e => e.name === name) || {};
            },
            entitiesNames (){
                return this.entities.map(e => e.name);
            },
            enabledChat (){
                return true;
                // return this.modelId && this.model.enabled_chat
            },
            enabledTraining (){
                return this.isTraining === false && this.stories.length > 0;
                // return this.modelId && this.model.enabled_training
            }
        },
        created (){
            this.GET(['projects', true])
                .then(() => {
                    // caso de haber sólo 1:
                    // 1. hacer invisible "Projects"
                    // 2. seleccionarlo para conseguir "Models" 
                    if (this.idIfOneProject){
                        this.SET(['projectId', this.idIfOneProject]);
                        // await this.$nextTick();
                        this.onProjectSelected(this.idIfOneProject);
                    }
                });
        },
        methods: {
            ...mapActions([
                'GET',
                'SET',
                'RESET',
                'NOTIFICATION_ERROR',
            ]),
            onTemplateChanged (){
                this.GET(['intents']);
                this.GET(['entities']);
            },
            onValueChanged (){
                this.intentId && this.GET(['templates']);
                this.GET(['entities']);
            },
            colorizeEntities ( entityValue, entityName){
                //console.warn('colorizeEntities', entityValue, entityName);
                const {text_color, color, id} = this.entityByName(entityName);
                if (!!color && !!text_color){
                    return `<span data-entity="${id}" style="color: ${text_color}; background-color: ${color}" class="px-1">${entityValue}</span>`;
                }
                return entityValue
            },
            // from tmpl: ...${param}... => ...<span class="entity">param</span>...
            tmplHilightEntities ( txt = "" ){
                const PARAMS = Array.from(txt.matchAll(_REGEX_));
                // comprobar que existen los PARAMS como ENTITIES correctamente, si no ERROR..
                const ENTITIES = PARAMS.filter( ([, entityName]) => this.entitiesNames.includes(entityName) );

                if (ENTITIES.length){
                    // número de EJEMPLOS que saldrán sustituyendo el TEMPLATE por todas las combinaciones de VALUES de ENTITIES existentes
                    const num = ENTITIES.reduce((acc, [, entityName]) => acc * this.entityByName(entityName).values_length , 1);
                    return txt.replace(_REGEX_, this.colorizeEntities)  + ` <sup class="grey--text">${num}</sup>`;
                }
                return txt;
            },
            sortByDesc (o, key){
                return [...o].sort((a, b) => a[key] > b[key] ? -1 : a[key] < b[key] ? 1 : 0)
            },
            exampleHilightEntities ( item ){
                const {entities, text} = item;
                return entities.length === 0
                    ? text
                    : this
                        .sortByDesc(entities, 'start')
                        .reduce((txt, {start, end, value, entity}) =>
                            txt.substring(0,start) + this.colorizeEntities(value, entity) + txt.substring(end)
                        , text);
            },
            entityTotalTemplates (){
                return Object.values(this.entity.intents || {}).reduce((acc, o) => acc + o.templates_length, 0);
            },
            async onTemplateSelected (id, target){
                if (!target) { return; }
                if (target.dataset && target.dataset.entity){
                    this.$root.$emit('select_entityId', target.dataset.entity)
                } else {
                    // abro dialog con EXAMPLES generados a partir de este TEMPLATE
                    await this.GET(['examples']);
                    this.examples_dialog = true;
                }
            },
            onIntentSelected (id){
                this.intentId && this.GET(['templates']);
                this.RESET(['templateId']);
            },
            onEntitySelected (id){
                this.entityId && this.GET(['values']);
            },
            onProjectSelected (id){
                if (id){
                    this.GET(['models', true]);
                }
            },
            onModelSelected (id){
                if (id){
                    Promise.all([
                        this.GET(['stories', true]),
                        this.GET(['entities', true]),
                        this.GET(['intents', true]),
                    ])
                }
            },
            onStorySelected (id){
                if (id){
                    this.GET(['interactions'], true)
                }
            },
            async trainModel (){
                // actualizo los modelos
                await this.GET(['models']);
                // si es entrenable
                if (this.enabledTraining){
                    this.isTraining = true;
                    this.SET(['notification', { 
                        type: 'info', 
                        message: `Start training model: ${this.model.name} !!!`
                    }]);
                    this.GET(['train'])
                        .then(async response => {
                            await this.GET(['models']);
                            this.SET(['notification', { 
                                type: 'success', 
                                message: `model ${this.model.name} trained successfully !!!`
                            }]);
                            console.warn('trained', response);
                            this.isTraining = false;
                        });
                } else {
                    this.SET(['error', `Training Model: ${this.model.name}\n${this.model.reason}`]);
                }
            },
            downloadingModel () {
                this.SET(['notification', { 
                    type: 'info', 
                    message: `Generating model files now!<br/>In 30 seconds starts downloading !!!`
                }]);
            },
           /*async*/ downloadModel () {
                this.isDownloading = true
                try {
                    // const { data } = await this.$axios.get('/api/projects/download')
                    // console.log(data)
                    this.exportTo(/*data*/)
                } catch (error) {
                    console.log(error)
                }
                this.isDownloading = false
            },
            exportTo (/*data*/) {
                // const blob = new Blob(
                //         [data], 
                //         {type: 'application/gzip'}
                //     )
                const url = '/api/projects/download' //window.URL.createObjectURL(blob)
                const a  = document.createElement('a');
                a.href = url
                a.download = 'files.gzip';
                document.body.appendChild(a);
                a.click();
                setTimeout(() => {
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                }, 0);
                // } else {
                //     window.open(url) //  window.location.asign
                // }
                // if (window.navigator.msSaveOrOpenBlob) window.navigator.msSaveOrOpenBlob(file, filename + extension);
            },
        },
    }
</script>

<style>
    .tile {
        border-radius: 0;
    }
    .minheight30{
        min-height: 30px;
    }
    /*
    ** común
    */
    .theme--light.v-list .v-list-item--highlighted{
        border: var(--v-accent-lighten2) 1px solid;
    }
    .mcb-projects  { height: 100px !important; }
    .mcb-models    { height: 125px !important; }
    .mcb-stories   { height: calc(100% - 225px) !important; }

    .hideProjects .mcb-projects  { display: none; }
    .hideProjects .mcb-models    { height: 125px !important; }
    .hideProjects .mcb-stories   { height: calc(100% - 125px) !important; }

    .mcb-intents   { height: 60% !important; }
    .mcb-entities  { height: 40% !important; }

    .mcb-templates { height: 60% !important; }
    .mcb-values    { height: 40% !important; }

    /*
    ** ENTITIES
    */
    .intentsInEntity {
        color: white;
        background-color: var(--v-primary-lighten1);
        padding: .5rem;
        border-radius: 1rem;
        display: none;
        font-size: .8rem;
        /* width: 2rem; */
        line-height: .2rem;
    }
        .mcb-card .v-list-item:hover .intentsInEntity{
            display: inline-block;
        }

    /*
    ** TEMPLATES
    */
    .mcb-projects .mcb-card-body,
    .mcb-models   .mcb-card-body,
    .mcb-stories  .mcb-card-body,
    .mcb-intents  .mcb-card-body,
    .mcb-entities .mcb-card-body {
        background-color: rgba(0,0,0,.05);
    }
        .theme--dark .mcb-projects .mcb-card-body,
        .theme--dark .mcb-models   .mcb-card-body,
        .theme--dark .mcb-stories  .mcb-card-body,
        .theme--dark .mcb-intents  .mcb-card-body,
        .theme--dark .mcb-entities .mcb-card-body {
            background-color: rgba(255,255,255,.05);
        }
</style>
