module.exports = function () {
    return [
        {
            '$unwind': '$interactions'
        }, 
        {
            '$group': {
                '_id': '$interactions.frame',
                'count': {
                    '$sum': 1
                }
            }
        }, 
        {
            '$sort': {
                'count': -1
            }
        }
    ]
}
