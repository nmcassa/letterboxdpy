import sys
import os
from json import dumps as json_dumps

try:
    from letterboxdpy import user  # Package is installed
except ImportError:  # Not installed
    try:
        sys.path.append(os.path.join(sys.path[0], '..'))
        from letterboxdpy import user  # Use local copy
    except (ImportError, ValueError) as e:
        print("The 'letterboxdpy' module is not installed.")
        print(f"Error details: {e}")
        response = input("Would you like to install it? (y/n): ").lower()
        if response == 'y':
            os.system("pip install letterboxdpy --force")
            print("Installation complete. Running script again...")
            sys.exit(0)
        print("Exiting...")
        sys.exit(1)

def follow_stats(following_data: dict, followers_data: dict) -> dict:
    """Analyzes follow statistics and returns followback and fan lists."""
    not_followback = []
    followback = []
    fans = []

    following = set(following_data.keys())
    followers = set(followers_data.keys())

    followback = list(following & followers)
    not_followback = list(following - followers)
    fans = list(followers - following)

    return {
        'not_followback': not_followback,
        'followback': followback,
        'fans': fans
    }

def get_username() -> str:
    """Fetches username from command-line arguments or user input."""
    if len(sys.argv) > 1:
        return sys.argv[1].lower()
    else:
        print(f'Quick usage: python {sys.argv[0]} <username>')
        return input('Enter username: ').lower()

def main() -> None:
    """Main function to get follow statistics and print results."""
    username = get_username()
    user_instance = user.User(username)

    followers_data = user.user_followers(user_instance)
    following_data = user.user_following(user_instance)

    data = follow_stats(following_data, followers_data)
    print(json_dumps(data, indent=4))

if __name__ == "__main__":
    main()
