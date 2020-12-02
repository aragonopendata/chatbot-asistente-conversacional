const express = require('express');
const app = express();

// app.use(express.json()) // for parsing application/json
// app.use(express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

const MongoClient = require('mongodb').MongoClient;
// const pkg = require('../package');
const { env: { urlMongo } } = require('../nuxt.config.js');
const DB_NAME = "rasa";
const COLLECTION = "sessions";

// ------------------------------------------------------------------------------------------------
// definido en "package.json" => config.base
// sin definir | config.base = "" => la base es desde el root "/"
// config.base = "/lo/que/sea"    => la base es desde "/lo/que/sea/"
// importante NO poner al final "/" en config.base
const base = process.env.BASE || process.env.npm_package_config_base || '' // definido en "package.json" => config.base=""

let dbo = null;

// function isConnected() {
//     return !!client && !!client.topology && client.topology.isConnected()
// }

const $connect = async function (){
    if (dbo) { return; }
    try {
        const db = await MongoClient.connect(urlMongo, { useNewUrlParser: true, useUnifiedTopology: true });
        dbo = db.db(DB_NAME); // db.topology.isConnected()
        // console.log(Object.keys(dbo));
    } catch (err) {
        throw err;
    }
}

// Initialize connection to mongoDB only when needed
$connect();

const $aggregate = function (aggregate){
    return dbo.collection(COLLECTION).aggregate(aggregate).toArray()
}

const AGGREGATIONS = [
    'sessions',
    'count_sessions',
    'count_interactions',
    'facet_sessions_per_date',
    'facet_interactions_per_frame',
    'facet_interactions_per_misunderstood',
    'facet_sessions_per_score',
    // xxx
    'facet_sessions_per|year', // 2014
    'facet_sessions_per|week', // 0 - 52/53
    'facet_sessions_per|month', // 1 (January) - 12 (December)
    'facet_sessions_per|hour', // 0 - 23
    'facet_sessions_per|dayOfYear', // 1 - 365/366
    'facet_sessions_per|dayOfWeek', // 1 (Sunday) - 7 (Saturday)
    'facet_sessions_per|isoDayOfWeek', // 1 (Monday) - 7 (Sunday)
    'facet_sessions_per|dayOfMonth', // 1 - 31
];
const isValidQuery = function (query) {
    return AGGREGATIONS.includes(query) || query.startsWith('interactions|')
};
// const isValidFile = function (path) {
//     try {
//         require.resolve(path);
//         return path;
//     } catch (e) {
//         return false;
//     }
// }
const getAggregationFromFile = function (name) {
    const [ filename, params ] = name.split("|");
    // const opcion_1 = isValidFile(`./mongo/aggregation/${filename}`);
    return require(`./mongo/aggregation/${filename}`)(params)
}

app.use(`${base}/api/aggregation/:facet`, express.json()) // for parsing application/json
app.use(`${base}/api/aggregation/:facet`, express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded
app.all(`${base}/api/aggregation/:facet`, async function (req, res) {
    // conecta sólo si hace falta
    await $connect();
    const facets = req.params.facet.split(',').filter(isValidQuery);
    // console.warn(facets);
    // FILTERS format:
    // {
    //     'interaction.frame': {
    //         values: ['smalltalk', 'aragon'],
    //         operator: 'or'
    //     }
    // }
    const FILTERS = req.body || {};
    const FILTERS_KEYS = Object.keys(FILTERS);
    
    let result = [];
    try {
        if (facets.length > 1){
            //
            // compruebo si recibo filtros en el "body" como POST:
            // "$and": [
            //     {
            //         "$or": [  // tipo A
            //             {
            //                 { "interactions.frame": "smalltalk" },
            //                 { "interactions.frame": "aragon" },
            //             }
            //         ]
            //     },
            //     {
            //         "date_start": { // tipo B
            //             $gte: ISODate('2019-11-12T00:00:00'),
            //             $lt:  ISODate('2019-11-12T23:59:59')
            //         } 
            //     }
            // ]
            const filters = FILTERS_KEYS.length
                ? {
                    "$and": FILTERS_KEYS.map(key => {
                        const { operator, values } = FILTERS[key];
                        // tipo A:
                        if (operator === 'or') {
                            return {
                                "$or": values.map(v => ({ [key]: v }))
                            }
                        } else if (operator === 'range') { // tipo B:
                            return {
                                [key]: {
                                    "$gte": new Date(`${values[0]}T00:00:00.000Z`),
                                    "$lt" : new Date(`${values[1] || values[0]}T23:59:59.999Z`)
                                }
                            }
                        }
                    })
                }
                : {}
                ;
            const query = [
                {
                    '$match': filters
                },
                {
                    // <key>: <aggregation - stage>
                    '$facet': facets.reduce((o, facet) => {
                                o[facet] = getAggregationFromFile(facet);
                                return o;
                            }, {})
                }
            ];
            // console.log(JSON.stringify(query[0], null, 4));
            // console.log('-----------------------------------------------')
            
            result = await $aggregate(query);
            result = result[0];
        } else if (facets.length === 1) {
            result = await $aggregate( getAggregationFromFile(facets[0]) );
        }
        res.send(result);
    } catch (err){
        res.send(err)
    }
});
// app.get('/api/sessions/:limit/:skip', async function (req, res) {
//     // ya usaremos "limits" y "skip"....
//     await $connect();
//     try {
//         const result = await dbo.collection(COLLECTION).find({}).toArray();
//         res.send(result);
//     } catch (err){
//         res.send(err)
//     }
// });

module.exports = app;
