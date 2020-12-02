module.exports = function ( sessionId ) {
    return [
        {
            '$match': {
                'session_id': sessionId
            }
        },
        {
            '$unwind': '$interactions'
        },
        {
            '$replaceRoot': {
                'newRoot': '$interactions'
            }
        }
    ]
}
