module.exports = function ( daterange ) {
    const validDateRanges = [
        'year', // 2014
        'week', // 0 - 52/53
        'month', // 1 (January) - 12 (December)
        'hour', // 0 - 23
        'dayOfYear', // 1 - 365/366
        'dayOfWeek', // 1 (Sunday) - 7 (Saturday)
        'isoDayOfWeek', // 1 (Monday) - 7 (Sunday)
        'dayOfMonth', // 1 - 31
    ]
    if (!validDateRanges.includes(daterange)){
        daterange = 'dayOfWeek'
    }
    return [
        {
            '$group': {
                '_id': {
                    [`$${daterange}`]: '$date_start'
                },
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
    ];
}
