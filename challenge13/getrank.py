import sys
from pymongo import MongoClient

def get_rank(user_id):
    print(user_id)
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    user_data = contests.aggregate([{
        '$group': {'_id':'$user_id','submit_time':{'$sum':'$submit_time'},'score': {'$sum':'$score'}}
    },{
        '$sort': {'score':-1,'submit_time':1}
    }])
    for i,v in enumerate(user_data):
        if v.get('_id') == user_id:
            return i+1,v.get('score'),v.get('submit_time')

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Parameter Error")
        sys.exit(-1)
    if not sys.argv[1].isdigit():
        print("Parameter Error")
    user_id = int(sys.argv[1])
    userdata = get_rank(user_id)
    print(userdata)
