module.exports = function () {
    return [
        {
            '$group': {
                '_id': '$score',
                'count': {
                    '$sum': 1
                }
            }
        },
        // {
        //     '$sort': {
        //         'count': -1
        //     }
        // }
    ]
}
