import webbrowser
from steam_web_api import Steam
import sys

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="config\.env")

STEAM_API_KEY = os.getenv("STEAM_API_KEY")

# Get user's owned games
# user = steam.users.get_owned_games("76561198995017863")

def get_game_id(game_name):
    try:
        steam = Steam(STEAM_API_KEY)
        app_list = steam.apps.search_games(game_name)
        if app_list:
            return app_list["apps"][0]["id"][0]
        return None
    except Exception as e:
        print(f"An error occured: {e}")
        return None

def main(query):
    steam_id = get_game_id(query)

    if steam_id:
        try:
            url = f"steam://run/{steam_id}"
            webbrowser.open(url)
            print(f"Opening {query} on Steam...")
        except Exception as e:
            return f"An error occured: {e}"
    else:
        return f"An error occured: {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = "_".join(sys.argv[1:])
        main(query)
    else:
        print("Please provide a query.")
        