const isPROD = process.env.NODE_ENV === 'production'

/*******************************************************************************
* proxy e iframes son dependientes del proyecto
*******************************************************************************/
const urlAPI =   isPROD ? 'api:5006' :   '127.0.0.1:5006' // '193.144.225.63:5007' //bitvise tunneling DGA
const urlTRAIN = isPROD ? 'train:5008' : '127.0.0.1:5008' // '193.144.225.63:5009' //bitvise tunneling DGA
const urlMongo = isPROD ? 'mongodb://mongodb:27017/' : 'mongodb://127.0.0.1:27017/'
const urlSocket = 'http://train:5008'
// const urlSOLR = isPROD ?      'argon-solr:8975'       : '212.166.71.148:8889'
// const urlJETTY4APPS= isPROD ? 'argon-jetty4apps:8080' : '212.166.71.148:8889'
// const urlJETTY= isPROD ?      'argon-jetty:8080'      : '212.166.71.148:8889'
// const urlCHAT = isPROD ?      'argon-asistente:5000'  : '193.144.225.63:5010' // volver al de alvaro
// const urlADMIN = isPROD ?     ''                      : 'http://212.166.71.148:8889'

//const base =  '/loginchat/'; // '/'  por defecto | '/meditor/' | '/lo/que/sea/'
// definido en "package.json" => config.base
// sin definir ó config.base = "" => la base es desde el root "/"
// config.base = "/lo/que/sea"    => la base es desde "/lo/que/sea/"
// importante NO poner al final "/" en config.base
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
        // OJO!!!! las rutas no deben empezar igual que en proxy, porque lo "captura" antes...
        '/restapi':           `http://${urlAPI}/apidocs`,
        '/rasa_nlu_trainer' : 'https://rasahq.github.io/rasa-nlu-trainer',
        '/rasa_talk_agents' : 'https://www.talk.jackdh.com/agents',
        // '/sentiment' :  'social/sentimiento.html',
        // '/admin' : `${urlADMIN}/SMAdminPrecog`,
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
    telemetry: false,
    
    env: {
        iframes,
        urlSocket,
        urlMongo
    },
    // https://nuxtjs.org/docs/directory-structure/nuxt-config#runtimeconfig
    publicRuntimeConfig: {
        urlAPI: `http://${urlAPI}`,
        base
    },
    // Disable server-side rendering (https://go.nuxtjs.dev/ssr-mode)
    ssr: false, //mode: 'universal',
    
    // Target: https://go.nuxtjs.dev/config-target
    // target: 'static', // 'server' default

    // Auto import components: https://go.nuxtjs.dev/config-components
    components: true,
    
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
            // {
            //     rel: 'stylesheet',
            //     href: 'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons'
            // }
        ],
        script: [
            {
                src: `https://polyfill.io/v3/polyfill.min.js?flags=gated&features=${polyfill.join('%2C')}`,
                crossorigin: 'anonymous',
                body: true
            }
        ]
    },
    router: {
        // '/' default | '/meditorclassic' ,'/lo/que/sea'
        base // ver arriba
    },
    /*
     ** Customize the progress-bar color
     */
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
    plugins: [],

    /*
     ** Nuxt.js build-modules
     */
    buildModules: [
        // Doc: https://github.com/nuxt-community/eslint-module
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
