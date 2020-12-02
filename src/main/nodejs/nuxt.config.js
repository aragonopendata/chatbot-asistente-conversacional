const isPROD = process.env.NODE_ENV === 'production'

/*******************************************************************************
* proxy e iframes son dependientes del proyecto
*******************************************************************************/
const urlAPI =  'api:5006'
const urlTRAIN = 'train:5008'
const urlMongo =  'mongodb://mongodb:27017/'
const urlSocket = 'http://train:5008'
const base = process.env.BASE || process.env.npm_package_config_base || '' // definido en "package.json" => config.base=""

const proxy = {
        // '/api'
        [`${base}/api`]: {
            target: `http://${urlAPI}`,
            pathRewrite: {
                [`^${base}/api`]: ''
            }
        },
        // '/exec'
        [`${base}/exec`]: {
            target: `http://${urlTRAIN}`,
            pathRewrite: {
                [`^${base}/exec`]: ''
            }
        }
    }

const iframes = {
        '/restapi':           `http://${urlAPI}/apidocs`,
        '/rasa_nlu_trainer' : 'https://rasahq.github.io/rasa-nlu-trainer',
        '/rasa_talk_agents' : 'https://www.talk.jackdh.com/agents',
        
    }
/******************************************************************************/

const colors = require('vuetify/es5/util/colors').default

const polyfill = [
    'es2015',
    'es2016',
    'es2017',
    'fetch',
    'IntersectionObserver',
    'ResizeObserver'
]

module.exports = {
    env: {
        iframes,
        urlSocket,
        urlMongo
    },
    mode: 'spa',
    /*
     ** Headers of the page
     */
    head: {
        titleTemplate: '%s - ' + process.env.npm_package_name,
        title: process.env.npm_package_name || '',
        meta: [{
                charset: 'utf-8'
            },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1'
            },
            {
                hid: 'description',
                name: 'description',
                content: process.env.npm_package_description || ''
            }
        ],
        link: [{
                rel: 'icon',
                type: 'image/x-icon',
                href: '/favicon.ico'
            },
        ],
        script: [
            {
                src: `https://polyfill.io/v3/polyfill.min.js?flags=gated&features=${polyfill.join('%2C')}`,
                crossorigin: 'anonymous',
                body: true
            }
        ],
        script: [
          ]
    },
    router: {
        base // ver arriba
    },
    loading: {
        color: '#fff'
    },

    /*
     ** Global CSS
     */
    css: [],

    /*
     ** Plugins to load before mounting the App
     */
    // plugins: [
    //     '@/plugins/socket.io',
    // ],

    /*
     ** Nuxt.js build-modules
     */
    buildModules: [
        
        '@nuxtjs/eslint-module',
        '@nuxtjs/vuetify'
    ],
    /*
     ** Nuxt.js modules
     */
    modules: [
        // Doc: https://axios.nuxtjs.org/usage
        '@nuxtjs/axios'
    ],
        
    /*
     ** Axios module configuration
     */
    axios: {
        // See https://github.com/nuxt-community/axios-module#options
        baseURL: base + '/',
        browserBaseURL: base + '/',
        //port,
        debug: false,
        credentials: true,
        proxy: true
    },
    proxy,
    /*
     ** vuetify module configuration
     ** https://github.com/nuxt-community/vuetify-module
     ** from: node_modules\@nuxtjs\vuetify\lib\module.js#5
     */
    vuetify: {
        // customVariables: ['~/assets/style/variables.scss'],
        // defaultAssets: {
        //     // font: false, // en vez de 'Roboto' explicitamente 'Nunito'
        //     font: {
        //         family: 'Roboto'
        //     },
        //     icons: 'mdi' // mdi|md|fa|fa4
        // },
        treeShake: isPROD, // true with customVariables
        theme: {
            dark: false, // true
            themes: {
                dark: {
                    primary: colors.blue.darken2,
                    accent: colors.grey.darken3,
                    secondary: colors.amber.darken3,
                    info: colors.teal.lighten1,
                    warning: colors.amber.base,
                    error: colors.deepOrange.accent4,
                    success: colors.green.accent3
                }
            }
        }
    },
    /*
     ** Build configuration
     */
    build: {
        /*
         ** You can extend webpack config here
         */
        extend (config, ctx) {}
    }
}
