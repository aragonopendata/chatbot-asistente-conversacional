<template>
    <v-hover #default="{ hover }">
        <v-card 
            tile
            class="mcb-story mcb-card" 
            >
            <v-toolbar
                :color="toolbarColor"
                :dark="!$vuetify.theme.dark"
                :light="$vuetify.theme.dark"
                dense
                class="mcb-card-toolbar"
                >
                <v-toolbar-title>
                    <v-icon>{{ toolbarIcon }}</v-icon> {{ title }}
                </v-toolbar-title>

                <slot name="after-title"></slot>

                <v-spacer />

                <ita-btn-icon
                    :show-btn="hover && !disabled"
                    :color="toolbarColor"
                    :tooltip="`Add new ${names[1]}`"
                    icon="mdi-plus-circle-outline"
                    @action="addItem"
                />
            </v-toolbar>
            <v-list 
                ref="story"
                class="mcb-card-body"
                >
                <v-hover
                    v-for="({ id, text = '', utter = '', actions = [], intent = '', recommendations }) in items"
                    :key="`interaction_${id}`"
                    #default="{ hover: hoverItem }"
                    >   
                    <v-list-item :class="{'bgcolor-o02': hoverItem}" class="py-5">
                        <v-fab-transition>
                            <v-list-item-action style="position:absolute;left:1rem">
                                <ita-btn-icon
                                    :tooltip="`Delete ${names[0]}`"
                                    :show-btn="hoverItem"
                                    color="error"
                                    icon="mdi-delete-forever"
                                    @action="deleteItem(id)"
                                />
                            </v-list-item-action>
                        </v-fab-transition>
                        <v-row no-gutters>
                            <v-col offset="2">
                                <div class="story-bubble story-bubble-right bgcolor-o05 elevation-5">
                                    <small class="grey--text">User</small>
                                    <br>
                                    <ita-textarea
                                        :value="text"
                                        @save="changeItem(id, 'text', ...arguments)"
                                    />
                                    <div
                                        v-if="recommendations"
                                        class="v-messages theme--light"
                                    >
                                        <div class="v-messages__wrapper">
                                            <div class="v-messages__message">
                                                Intents recommended:
                                                <a
                                                    v-for="recommended in recommendations"
                                                    :key="`interaction_${id}_${recommended}`"
                                                    class="recommended"
                                                    @click="clickOnRecommendedIntent(recommended, id)"
                                                    >
                                                    {{ recommended }}
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                    <ita-autocomplete
                                        :value="intent"
                                        :intents="intents"
                                        @save="changeItem(id, 'intent', ...arguments)"
                                        @targetIntent="selectIntentByName(intent)"
                                    />
                                </div>
                            </v-col>
                            <v-col cols="10" class="mt-4">
                                <div class="story-bubble story-bubble-left bgcolor-o1 elevation-5">
                                    <small class="grey--text">Bot</small>
                                    <br>
                                    <template v-for="({type, value}, index) in actions">
                                        <component 
                                            :is="type === 'action' ? 'v-combobox' : 'v-textarea'" 
                                            :key="`interaction_${id}_action_${index}`"

                                            :items="actionsAll"

                                            auto-grow
                                            rows="1"
                                            
                                            :value="value"
                                            dense
                                            hide-details
                                            :title="type"
                                            style="position:relative"
                                            @change="renameUtterAction(id, index, ...arguments)"
                                        >
                                            <template #prepend>
                                                <v-icon 
                                                    small 
                                                    :color="type === 'action' ? 'info' : 'warning'" 
                                                    style="position:absolute;top:7px;left:-10px"
                                                    >
                                                    {{ type === 'action' ? 'mdi-flash' : 'mdi-message-reply-text' }}
                                                </v-icon>
                                            </template>
                                            <template #append-outer>
                                                <v-btn 
                                                    v-show="hoverItem"
                                                    style="position:absolute;top:0;right:-15px"
                                                    icon
                                                    small
                                                    :title="`Delete this ${type}`"
                                                    @click.stop="deleteUtterAction(id, index, ...arguments)"
                                                    >
                                                    <v-icon>mdi-delete-forever</v-icon>
                                                </v-btn>
                                            </template>
                                        </component>
                                    </template>
                                    <div class="text-center mt-4 mb-2">
                                        <v-btn x-small title="Add new Utter" @click="addUtterAction(id, 'utter')">
                                            <v-icon left>
                                                mdi-plus-circle-outline
                                            </v-icon> 
                                            <v-icon small color="warning">mdi-message-reply-text</v-icon>
                                            &nbsp;Utter
                                        </v-btn>
                                        <v-btn x-small title="Add new Action" @click="addUtterAction(id, 'action')">
                                            <v-icon left>
                                                mdi-plus-circle-outline
                                            </v-icon> 
                                            <v-icon small color="info">mdi-flash</v-icon>
                                            Action
                                        </v-btn>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>
                    </v-list-item>
                </v-hover>
            </v-list>
        </v-card>
    </v-hover>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';

    import  { VCombobox, VTextarea } from 'vuetify/lib';
    
    import ItaBtnIcon from '~/components/ItaBtnIcon';
    import ItaTextareaToggleEdit from '~/components/ItaTextareaToggleEdit';
    import ItaAutocompleteToggleEdit from '~/components/ItaAutocompleteToggleEdit';

    export default {
        components: {
            ItaTextarea: ItaTextareaToggleEdit,
            ItaAutocomplete: ItaAutocompleteToggleEdit,
            ItaBtnIcon,
            VCombobox,
            VTextarea
        },
        props: {
            toolbarColor: {
                type: String,
                default: "",
            },
            toolbarIcon: {
                type: String,
                default: "",
            },
            title: {
                type: String,
                default: "",
            },
            storeItems: {
                type: String,
                default: '',
            },
            intents: {
                type: Array,
                default: () => [],
            },
            names: {
                type: Array,
                default: () => ["item", "items"],
            },
            disabled: {
                type: Boolean,
                default: false,
            },
        },
        data (){
            return {
                item_new: '',
            }
        },
        computed: {
            ...mapState([
                'recommendations',
                'isBusy'
            ]),
            ...mapGetters([
                'interaction',
                'story'
            ]),
            ...mapGetters({
                actionsAll: 'actions'
            }),
            items (){
                return this.$store.state[this.storeItems] || [];
            },
            intentIdByName (){
                return name => (this.intents.find(i => i.name === name) || {}).id || '';
            },
        },
        mounted (){
            this.scrollToBottom();
            // conseguir todos los "actions";
            this.GET(['actions']);
        },
        methods: {
            ...mapActions([
                'GET',
                'ADD',
                'DELETE',
                'PATCH',
                'SET',
                'SETKEY',
            ]),
            async addItem (){ // item === {text, utter, intent}
                await this.ADD([
                        this.storeItems,
                        {
                            text: '',
                            utter: '',
                            intent: ''
                        }
                    ]);
                await this.$nextTick();
                this.scrollToBottom();
                // update stories
                this.GET(['stories']);
            },
            // scroll down to the bottom of STORY column
            async scrollToBottom (){
                await this.$nextTick();
                const ELE = this.$refs.story.$el;
                // try {
                    ELE.scrollTo(0, ELE.scrollHeight);
                    // no compatible IE
                    // ELE.scrollTo({
                    //     left: 0,
                    //     top: ELE.scrollHeight,
                    //     behavior: 'smooth',
                    // });
                // } catch (error) { 
                // }
            },
            deleteItem (itemId){
                if (confirm("Are you sure to delete "+ this.storeItems +": "+ itemId)){
                    const config = [
                            this.storeItems,
                            itemId,
                        ];
                    return this.DELETE(config)
                        .then(response => {
                            this.$emit('onItemDeleted', itemId);
                            // update stories
                            this.GET(['stories']);
                            return response;
                        })
                        .catch(error => {
                            this.$emit('onError', {config, method: 'delete', error})
                        });
                }
            },
            changeItem (id, key, value){ // id === index in interactions ARRAY...
                //const interaction = this.interactionById(id);
                this.SET(['interactionId', id]);
                //console.warn('changeItem', this.interaction);
                if (value !== undefined && key !== undefined){
                    this.SETKEY({ 
                        item: this.interaction, 
                        key, 
                        value 
                    });
                }
                this.patchInteraction(id, `change '${key}' in Interaction`)
            },
            addUtterAction (id, type = "utter") {
                this.SET(['interactionId', id]);
                this.SETKEY({ 
                    item: this.interaction.actions, 
                    key:  this.interaction.actions.length,  
                    value: { 
                        type, 
                        value: type === "action" ? "action_" : "" 
                    }
                })
                this.patchInteraction(id, `add '${type}' in Interaction`);
            },
            renameUtterAction (id, index, newName) {
                this.SET(['interactionId', id]);
                const { type } = this.interaction.actions[index]
                this.SETKEY({
                    item: this.interaction.actions,
                    key: index,
                    value: {
                        type,
                        value: newName
                    }
                });
                this.patchInteraction(id, `rename '${type}' in Interaction`);
            },
            deleteUtterAction (id, index) {
                this.SET(['interactionId', id]);
                const { type, value } = this.interaction.actions[index]
                if (confirm("Are you sure to delete this "+ type +": "+ value)){
                    const newACTIONS = [...this.interaction.actions];
                    const deletedACTION = newACTIONS.splice(index,1); // delete action[index]
                    this.SETKEY({
                        item: this.interaction,
                        key: "actions",
                        value: newACTIONS
                    });
                    this.patchInteraction(id, `delete '${type}': <pre><code>${JSON.stringify(deletedACTION, null, 4)}</code></pre> in Interaction`);
                }
            },
            async patchInteraction (id, method = "") {
                const config = [
                        this.storeItems,
                        this.interaction
                    ];
                try {
                    const response = await this.PATCH(config);
                    this.$emit('onItemChanged', id);
                    return response;
                } catch (error) {
                    this.$emit('onError', { config, method, error })
                }
            },
            clickOnRecommendedIntent (intentName, id){
                const intentId = this.intentIdByName(intentName);
                //const INTERACTION = this.interactionById(id);
                this.SET(['interactionId', id]);
                // filter INTENTS to recommended & show its TEMPLATES
                this.$root.$emit('select_intentId',intentId);
                // change value of INTENT in AUTOCOMPLETE
                this.SETKEY({ item: this.interaction, key: 'intent', value: intentName} );
                // this.interactions[index].intent = item;
                // save value of INTENT in SERVER
                this.changeItem(id, 'intent', intentName);
            },
            selectIntentByName (intentName){
                const intentId = this.intentIdByName(intentName);
                this.$root.$emit('select_intentId',intentId);
            },
        }
    }
</script>

<style>
    /********************************************************* */
    .mcb-card {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
        .mcb-card-toolbar {
            flex-grow: 0 !important;
        }
        .mcb-card-body {
            flex-grow: 1 !important;
            overflow-y: auto;
        }
    /********************************************************* */
        .mcb-story .v-list-item{
            height: auto;
            flex-direction: column;
            align-items: initial;
        }
        .mcb-story .v-input{
            align-items: center;
        }
        /* .mcb-story .v-input--is-focused input,
        .mcb-story .v-input--is-focused textarea, */
        .mcb-story .v-input--is-focused .v-text-field__slot,
        .mcb-story .v-input--is-focused .v-select__slot{
            background-color: #fff;
        }
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
        .story-bubble .imtte .btn-edit{
            position: absolute;
            /* top: 0; */
            right: .5rem;
        }
    .mcb-story .container .btn-invisible{
        display: none;
    }
        .mcb-story .container:hover .btn-invisible{
            display: inline-flex;
        }
    .mcb-story .recommended{
        margin-left: .5rem;
        display:block;
    }
        .mcb-story .recommended:hover{
            background-color: rgb(0,0,0,.05);
        }
    /* autocomplete */
    .v-autocomplete__content .v-list-item{
        height: 30px;
    }
        .v-autocomplete__content .theme--light.v-list  .v-list-item:hover{
            background-color: var(--v-accent-lighten2);
        }
    .mcb-story .imla{
        position: absolute;
        top: 1rem;
        left: 1rem;
        align-items: flex-start;
        /* bottom: 1rem;
        right:0;
        align-items: flex-end; */
    }

    .bgcolor-o02              { background-color: rgba(0,0,0,.035); }
    .theme--dark .bgcolor-o02 { background-color: rgba(255,255,255,.035); }
    .bgcolor-o05              { background-color: rgba(0,0,0,.075); }
    .theme--dark .bgcolor-o05 { background-color: rgba(255,255,255,.075); }
    .bgcolor-o1               { background-color: rgba(0,0,0,.175); }
    .theme--dark .bgcolor-o1  { background-color: rgba(255,255,255,.175); }

</style>
