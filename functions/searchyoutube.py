import sys
import webbrowser


def main(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)
    print(f"Searching for: {query} on YouTube...; include no extra information")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = "+".join(sys.argv[1:])
        main(query)
    else:
        print("Please provide a search query.")