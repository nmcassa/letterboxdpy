import sys
import os
import csv

try:
    from letterboxdpy.search import Search
    from letterboxdpy.list import List
    from letterboxdpy.utils.utils_terminal import get_input, args_exists
except ImportError:
    try:
        sys.path.append(os.path.join(sys.path[0], '..'))
        from letterboxdpy.search import Search
        from letterboxdpy.list import List
        from letterboxdpy.utils.utils_terminal import get_input, args_exists
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

def save_results_to_csv(list_instance: List, csv_file: str) -> None:
    """Saves movie list results to a CSV file."""
    directory = os.path.join(os.getcwd(), 'exports', 'lists')
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_name = os.path.join(directory, csv_file)

    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['LetterboxdURI', 'Title'])
        movies = list_instance.movies
        for movie_data in movies.values():
            writer.writerow([movie_data['url'], movie_data['name']])
    print(f"Data successfully saved to {csv_file}. Movies: {len(movies)}")

if __name__ == "__main__":
    if not args_exists():
        print(f'Quick usage: python {sys.argv[0]} <search_query> <max_lists>')

    search_query = get_input("Enter your search query for lists: ", index=1)

    search_instance = Search(search_query, "lists")
    search_data = search_instance.results

    if search_data['available']:
        results = search_data['results']
        search_count = search_data['count']

        print(f'Found {search_count} lists. ')
        max_lists = get_input('How many to export? (0 for all): ', index=2, expected_type=int)

        if max_lists == 0:
            max_lists = search_count

        print(f'Exporting first {max_lists} lists...')
        results = results[:max_lists]

        for result in results:
            list_slug = result['slug']
            list_owner_username = result['owner']['username']

            list_instance = List(list_owner_username, list_slug)
            csv_filename = f"{list_owner_username}_{list_slug}.csv"
            save_results_to_csv(list_instance, csv_filename)
    else:
        print(f'No lists found for "{search_query}".')