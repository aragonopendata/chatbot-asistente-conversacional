module.exports = function ( params ) {
    if (params){
        const [limit, skip] = params.split("|");
        const LIMIT = limit ? [{ '$limit': limit }] : [];
        const SKIP  = skip ?  [{ '$skip': skip }] : [];
    }
    return [
        {
            '$addFields': {
                // extrae en "date_end" del array "interactions" el "date_bot" más reciente
                'date_end': {
                    '$max': "$interactions.date_bot"
                },
                // array "interactions".length
                'count_interactions': {
                    '$size': "$interactions"
                },
                // extrae cuenta de "is_misunderstood" === true del array "interactions"
                'count_misunderstood': {
                    '$size': {
                        '$filter': {
                            'input':'$interactions',
                            'as': "i",
                            'cond': { '$eq': ["$$i.is_misunderstood", true] }
                        }
                    }
                }
            }
        },
        {
            '$project': {
                'interactions': 0
            }
        },
        {
            '$sort': {
                'date_start': -1
            }
        }
        /*,
        ...SKIP,
        ...LIMIT
        */
    ]
}
