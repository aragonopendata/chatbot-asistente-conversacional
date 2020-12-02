module.exports = function () {
    return [
        {
            '$unwind': '$interactions'
        }, 
        {
            '$count': 'count'
        }
    ]
}
