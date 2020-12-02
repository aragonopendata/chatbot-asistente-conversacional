module.exports = function () {
    return [
        {
            '$unwind': '$interactions'
        }, 
        // {
        //     '$match': {
        //         'interactions.is_misunderstood': true
        //     }
        // }, 
        // {
        //     '$replaceRoot': {
        //         'newRoot': {
        //             '$mergeObjects': [
        //                 {
        //                     '_id': '$_id'
        //                 }, 
        //                 '$interactions'
        //             ]
        //         }
        //     }
        // }
        {
            '$group': {
                '_id': '$interactions.is_misunderstood',
                'count': { 
                    '$sum': 1
                }
            }
        },
        // quitamos valores de "null"
        {
            '$match': {
                '_id': { '$ne': null }
            }
        }
    ]
}
