from src.Starter import Starter


def users_to_insert():
    """
    Gets the users to insert.
    :return: The users to insert.
    """

    return [
        {
            "id": 218810179590815744,
            "username": "Potpot",
        },
        {
            "id": 283869518609121280,
            "username": "Mat.",
        }
    ]

def insertions(clear=False):
    """
    Inserts data into the database.
    :param clear: If True, clears the database before inserting.
    :return: None
    """
    starter = Starter()

    if clear:
        starter.database.clear()

    users = users_to_insert()
    for user in users:
        starter.database.add_user(user["id"], user["username"])
    starter.database.add_favoris("dunk low", "bw", "39", "WTB", 218810179590815744, "DD1391-100")

if __name__ == "__main__":
    insertions(clear=True)