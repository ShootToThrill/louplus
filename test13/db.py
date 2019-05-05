# db.contests.createIndex({user_id:1})

# db.contests.aggregate([
#     {
#         $group: {_id:'$user_id',submit_time:{$sum:'$submit_time'},score: {$sum:'$score'}}
#     },{
#         $sort: {score:1,submit_time:-1}
#     }
# ])