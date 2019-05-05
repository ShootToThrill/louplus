import sys
from pymongo import MongoClient

# db.contests.aggregate(
# ... [
# ... {
# ... $project:{item:1,score_all:{$add:['$score','$submit_time']}}
# ... }
# ... ]
# ... )

def get_rank(user_id):
	print(user_id)
	client = MongoClient()
	db = client.shiyanlou
	contests = db.contests
	user_data = contests.find({'user_id':user_id})
	for i in user_data:
		print(i)


if __name__ == '__main__':

    if len(sys.argv) != 2:
    	print("Parameter Error")
    	sys.exit(-1)
    if not sys.argv[1].isdigit():
    	print("Parameter Error")
    user_id = int(sys.argv[1])
    userdata = get_rank(user_id)
    print(userdata)