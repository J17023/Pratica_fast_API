def User_schema(user) ->dict:
    return {
    "_id": str(user["_id"]),
    "username" : user["username"],
    "email":user["email"]
    }

def Users_list(users) ->list:
    return [User_schema(user) for user in users]
