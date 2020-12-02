<template>
    <v-app>
        <v-navigation-drawer 
            v-model="drawer" 
            :mini-variant="miniVariant" 
            :clipped="clipped" 
            fixed 
            app
            >
            <v-list subheader>
                <v-list-item>
                    <v-btn icon @click.stop="miniVariant = !miniVariant">
                        <v-icon>{{ `mdi-chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
                    </v-btn>
                </v-list-item>
                
                <template v-for="route in routes">
                    <v-list-item :to="route.to" router exact>
                        <v-list-item-action>
                            <v-icon>{{ route.icon }}</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>{{ route.title }}</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                    <v-divider />
                </template>
            </v-list>
            <template v-slot:append>
                <v-img :src="require('../assets/img/logo_aragonopendata.png')" class="mx-4 mb-4" />
            </template>
        </v-navigation-drawer>

        <v-app-bar :clipped-left="clipped" fixed app dense>
            <v-app-bar-nav-icon @click.native="drawer = !drawer" />
            <v-toolbar-title>
                {{ title }} <v-icon>mdi-chevron-double-right</v-icon> <span class="primary--text headline font-weight-bold">{{ pageTitle }}</span>
            </v-toolbar-title>

            <v-spacer />

            <img src="~assets/img/logo_aragonopendata.png" style="height:85%"/>
            <!-- <v-img 
                :src="require('../assets/img/logo_aragonopendata.png')" 
                class="mr-5"
                style="height:75%"
            /> -->

            <v-divider vertical class="ml-4" />
            <v-btn icon @click.stop="clipped = !clipped">
                <v-icon>mdi-page-layout-header</v-icon>
            </v-btn>
            <v-divider vertical class="ml-4" />
            <v-btn icon @click.stop="toggleThemeDark">
                <v-icon>mdi-invert-colors</v-icon>
            </v-btn>
        </v-app-bar>

        <v-content style="height:100vh">
            <v-container 
                class="pa-0" 
                :class="{'fill-height': isFillHeight}" 
                fluid
                >
                <v-progress-linear v-show="$store.state.isBusy" indeterminate absolute top />
                <nuxt />
            </v-container>
        </v-content>

        <ita-footer />

        <ita-notification
            v-bind="notification"
            @close="NOTIFICATION_RESET"
        />
    </v-app>
</template>

<script>
    import { mapState, mapActions } from 'vuex';

    import ItaFooter from './partials/ItaFooter'
    import ItaNotification from '~/components/ItaNotification';

    export default {
        components: {
            ItaFooter,
            ItaNotification,
        },
        data () {
            return {
                clipped: false,
                drawer: true,
                fixed: false,

                miniVariant: false,
                right: true,
                rightDrawer: false,
                title: 'Chat•Bot Panel de Control',

                routes: [
                    // {
                    //     title: "Inicio",
                    //     icon: "mdi-apps",
                    //     to: "/about"
                    // },
                    {
                        title: "Análisis y Estadísticas",
                        icon: "mdi-view-dashboard",
                        to: "/"
                    },
                    {
                        title: "Entrenamiento",
                        icon: "mdi-chat-processing",
                        to: "/training"
                    },
                    {
                        title: "API docs",
                        icon: "mdi-label",
                        to: "/restapi"
                    }
                ]
            }
        },
        computed: {
            ...mapState([
                'notification'
            ]),
            pageTitle () {
               const ROUTE = this.routes.filter(r => r.to === this.$route.path)
                return ROUTE.length === 1 ? ROUTE[0].title : 'página desconocida'
            },
            isFillHeight () {
                // return this.$route.path === '/training'
                return this.$route.path !== '/'
            }
        },
        methods: {
            ...mapActions([
                'RESET',
                'NOTIFICATION_RESET',
            ]),
            toggleThemeDark () {
                this.$vuetify.theme.dark = !this.$vuetify.theme.dark
            }
        }
    }
</script>
