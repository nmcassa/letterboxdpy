from user import User
from movie import Movie 

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter()

    nick = User("nmcassa")
    print("JSON of my User Object:\n")
    print(nick.jsonify())

    king = Movie("the king of comedy")
    print(king.jsonify())
    

    
