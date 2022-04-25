<template>
    <v-hover #default="{ hover }">
        <v-card class="mcb-card" tile>
            <v-toolbar
                :color="toolbarColor"
                :dark="!$vuetify.theme.dark"
                :light="$vuetify.theme.dark"
                dense
                class="mcb-card-toolbar"
                >
                <v-toolbar-title>
                    <v-icon>{{ toolbarIcon }}</v-icon> {{ title }}
                    <ita-num-sup :num="items_filtered" :total="items" class="text--lighten-1" />
                </v-toolbar-title>

                <slot name="after-title"></slot>

                <v-spacer />

                <ita-menu-action
                    v-model="item_filter"
                    :show-activator="showFilter && hover && !item_filter"
                    icon-activator="mdi-filter"
                    :tooltip-activator="`filter ${names[0]} by ${item_filter}`"
                    :label-input="`filter ${names[1]} » name contains`"
                    :color="toolbarColor"
                />
                <ita-menu-action
                    v-model="item_new"
                    :show-activator="hover && showAdd"
                    icon-activator="mdi-plus-circle-outline"
                    :tooltip-activator="`Add New ${names[1]}`"
                    :label-input="`${names[1]} names (each line)`"
                    :label-btn-action="`Add new ${names[1]}`"
                    :hint-input="`Do not repeat an existing name for a new ${names[0]}`"
                    :color="toolbarColor"
                    multiple
                    @action="addItem"
                />
                <slot
                    name="appendMenu"
                    :hover="hover"
                />
            </v-toolbar>
           
            <v-list class="mcb-card-body">
                <v-chip
                    v-show="item_filter"
                    close
                    small
                    class="ml-3"
                    @click:close="item_filter=''"
                    >
                    <v-icon small>
                        mdi-filter
                    </v-icon>
                    {{ item_filter }}
                </v-chip>
                <v-menu 
                    v-model="menu_show"
                    transition="scale-transition" 
                    :activator="menu_activator"
                    >
                    <v-list dense>
                        <v-subheader>
                            with {{ names[0] }}&nbsp;
                            <strong>"{{ menu_item.name }}"</strong>
                            :
                        </v-subheader>
                        <vDivider />
                        <v-list-item 
                            :title="`Rename ${names[0]}: '${menu_item.name}'`"
                            @click="item_editable = menu_item.id"
                            >
                            <v-list-item-title>
                                <v-icon>
                                    mdi-square-edit-outline
                                </v-icon>
                                Rename 
                            </v-list-item-title>
                        </v-list-item>
                        <v-list-item 
                            :title="`Delete ${names[0]}: '${menu_item.name}'`"
                            @click="deleteItem(menu_item.id)"
                            >
                            <v-list-item-title>
                                <v-icon>
                                    mdi-delete-forever
                                </v-icon>
                                Delete
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>

                <template
                    v-for="item in items_filtered"
                    >
                    <v-list-item
                        :ref="item.id"
                        :key="item.id"
                        :class="{'ita-active bgcolor-active': isItemActiveMode(item), 'bgcolor-o05': menu_item.id === item.id }"
                        class="bgcolor-hover"
                        :title="item.name"
                        :ripple="!isItemActiveMode(item)"
                        @click="if (!isItemActiveMode(item) && !isItemEditMode(item)) selectItemId(item.id, $event.target)"
                        >
                        <v-list-item-content class="py-0">
                            <slot name="content" :item="item">
                                <ita-list-edit
                                    v-if="isItemEditMode(item)"
                                    :value="item.name"
                                    @cancel="item_editable = ''"
                                    @action="changeItem(item, 'name', ...arguments)"
                                />
                                <v-list-item-title
                                    v-else
                                    class="ita-item"
                                    >
                                    <slot name="prependContent" :item="item" />
                                    <slot :item="item">
                                        {{ item.name }}
                                    </slot>
                                    <ita-num-sup
                                        v-if="numChildren(item) !== undefined"
                                        :num="numChildren(item)"
                                    />
                                    <slot name="appendContent" :item="item" />
                                </v-list-item-title>
                            </slot>
                        </v-list-item-content>

                        <slot name="prependAction" :item="item" />
            
                        <v-list-item-action 
                            v-show="!item.editable"
                            class="my-0"
                            >
                            <v-btn icon small @click.stop="showMenu($event, item)">
                                <v-icon>mdi-dots-vertical</v-icon>
                            </v-btn>
                        </v-list-item-action>

                        <slot name="appendAction" :item="item" />
                        
                    </v-list-item>
                </template>
            </v-list>
        </v-card>
    </v-hover>
</template>

<script>
    import { mapActions } from 'vuex';

    export default {
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
                default: "Projects",
            },
            storeItems: {
                type: String,
                default: '',
            },
            storeItem: {
                type: String,
                default: '',
            },
            names: {
                type: Array,
                default: () => ["item", "items"],
            },
            storeItemId: {
                type: String,
                default: '',
            },
            itemChildren: {
                type: String,
                default: ''
            },
            // threshold to show filter menu (0 => shows always)
            filterable: {
                type: Number,
                default: 10,
            },
            showAdd: {
                type: Boolean,
                default: true,
            }
        },
        data () {
            return {
                item_filter: '',
                item_new: '',
                item_editable: '', // id
                menu_show: false,
                menu_item: {},
                menu_activator: null,
            }
        },
        computed: {
            itemId (){
                return this.$store.state[this.storeItemId] || '';
            },
            items (){
                return  this.$store.getters[this.storeItems] ||
                        this.$store.state[this.storeItems] ||
                        [];
            },
            item_selected (){
                return this.$store.getters[this.storeItem] || {};
            },
            item_filter_noCaseDiacritic () {
                return this.noCaseDiacritic(this.item_filter);
            },
            items_filtered (){
                return this.item_filter_noCaseDiacritic
                    ? this.items.filter(i => this.noCaseDiacritic(i.name).includes(this.item_filter_noCaseDiacritic))
                    : this.items
                    ;
            },
            showFilter (){
                return this.items.length >= this.filterable;
            }
        },
        created (){
            // this.fetchItems();
            this.$root.$on(`select_${this.storeItemId}`, this.selectItemId);
        },
        mounted (){
            this.scrollToItemId();
        },
        beforeDestroy (){
            this.$root.$off(`select_${this.storeItemId}`);
        },
        methods: {
            noCaseDiacritic: str => str && str.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""),
            showMenu (e, item) {
                e.preventDefault();
                this.menu_show = false;
                this.menu_item = item;
                this.menu_activator = e.target;
                this.$nextTick(() => {
                    this.menu_show = true
                })
            },
            isItemActiveMode (item) {
                return this.itemId === item.id;
            },
            isItemEditMode (item) {
                return this.item_editable === item.id;
            },
            ...mapActions([
                'ADD',
                'DELETE',
                'PATCH',
                'SET',
                'RESET',
            ]),
            numChildren (item){
                const CHILDS = item[this.itemChildren];
                return Array.isArray(CHILDS) ? CHILDS.length : CHILDS;
            },
            addItem (){
                if (this.item_new){
                    const newItems = [].concat(this.item_new); // = ['name1', 'name2', ....]
                    this.ADD([this.storeItems, newItems])
                        .then(() => {
                            this.$emit('onItemAdded');
                            // por aquí podría seleccionar el primero añadido...
                            // pero ojo, sólo por name, no por id...
                            const itemIdChanged = (this.items.find(i => i.name === newItems[0]) || {}).id;
                            if (itemIdChanged){
                                this.selectItemId( itemIdChanged );
                            }
                        });
                    this.item_new = '';
                }
            },
            scrollToItemId (){
                if (this.itemId && this.itemId in this.$refs){
                    this.$refs[this.itemId][0].$el.scrollIntoView();
                }
            },
            async selectItemId (itemId, target){
                // if not SHOWED remove INTENTS FILTER
                if ( !this.items_filtered.map(i => i.id).includes(itemId) ){
                    this.item_filter = '';
                }
                this.SET([this.storeItemId, itemId]);
                await this.$nextTick();
                this.scrollToItemId();
                this.$emit('onItemSelected', itemId, target);
            },
            deleteItem (itemId){
                if (confirm("Are you sure to delete "+ this.storeItems +": "+ itemId)){
                    const config = [
                            this.storeItems,
                            itemId,
                            this.itemId === itemId, // <= resetea y deselecciona
                        ];
                    return this.DELETE(config)
                        .then(response => {
                            this.$emit('onItemDeleted', itemId);
                            return response;
                        })
                        .catch(error => {
                            this.$emit('onError', {config, method: 'delete', error})
                        });
                }
            },
            changeItem (itemOriginal, key, value){
                // cambio el ITEM con el nuevo "key:value"
                const item = Object.assign( {}, itemOriginal, { [key]: value} );
                const config = [
                        this.storeItems,
                        item
                    ];
                return this.PATCH(config)
                    .then( response => {
                        this.$emit('onItemChanged', item.id);
                        return response;
                    })
                    .catch(error => {
                        this.$emit('onError', {config, method: 'patch', error})
                    })
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
        }
    /********************************************************* */
    .mcb-card-toolbar .v-btn:not(:last-of-type){
        margin-right: 1rem;
    }
    .mcb-card .v-list-item {
        min-height: 30px; /*48px*/
    }
        .mcb-card .v-list-item__action {
            max-height: 30px;
        }
    .mcb-card .v-list{
        overflow-y: auto;
    }
    .mcb-card .ita-active {
        border-radius: 1rem 0 0 1rem !important;
        margin-left: 1em;
        font-weight: 700;
    }
    .mcb-card .v-list-item__action:not(.visible) {
        display: none;
    }
        .mcb-card .v-list-item:hover .v-list-item__action:not(.visible) {
            display: flex;
        }

    .bgcolor-hover:not(.bgcolor-active):hover  { 
        cursor: pointer;
        background-color: rgba(0,0,0,.02); 
    }
        .theme--dark .bgcolor-hover:not(.bgcolor-active):hover  { 
            background-color: rgba(255,255,255,.02); 
        }

    .bgcolor-active { 
        cursor: inherit;
        background-color: rgba(0,0,0,.2); 
    }
        .theme--dark .bgcolor-active { 
            background-color: rgba(255,255,255,.2); 
        }

</style>
