module.exports = function () {
    return [
        {
            '$project': {
                'date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d', 
                        'date': '$date_start'
                    }
                }
            }
        }, {
            '$group': {
                '_id': '$date', 
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
        },
        {
            '$sort': {
                '_id': -1
            }
        }
    ];
}
