"""
Letterboxd User Data Exporter

Exports comprehensive user data from Letterboxd profiles.
- Export all user data (films, reviews, lists, followers, etc.)
- Automatic JSON file generation
- Organized directory structure
- Progress tracking and timing
"""

__title__ = "User Data Exporter"
__description__ = "Exports comprehensive user data from Letterboxd profiles."
__version__ = "0.1.1"
__author__ = "fastfingertips"
__author_url__ = "https://github.com/fastfingertips"
__created_at__ = "2024-06-18"

import os
import sys
import time

from fastfingertips.terminal_utils import args_exists, get_input

from letterboxdpy import user
from letterboxdpy.utils.utils_directory import check_and_create_dirs
from letterboxdpy.utils.utils_file import JsonFile, build_click_url, build_path
from letterboxdpy.utils.utils_string import strip_prefix


def main():
    if not args_exists():
        print(f"Quick usage: python {sys.argv[0]} <username>\n")

    username = get_input("Enter username: ", index=1)
    user_instance = user.User(username)

    # Get the directory where this script is located (examples folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Export directories
    exports_dir = build_path(script_dir, "exports")
    users_folder = build_path(exports_dir, "users")
    user_folder = build_path(users_folder, user_instance.username)
    directories = [exports_dir, users_folder, user_folder]
    check_and_create_dirs(directories)

    start_time = time.time()

    # Save user instance data
    user_data_path = build_path(user_folder, "user")
    JsonFile.save(user_data_path, user_instance.jsonify())

    # Export data for each method
    methods = [
        user.User.get_activity,
        user.User.get_activity_following,
        user.User.get_diary,
        user.User.get_wrapped,
        user.User.get_films,
        user.User.get_films_not_rated,
        user.User.get_genre_info,
        user.User.get_liked_films,
        user.User.get_liked_reviews,
        user.User.get_liked_lists,
        user.User.get_lists,
        user.User.get_following,
        user.User.get_followers,
        user.User.get_reviews,
        user.User.get_user_tags,
        user.User.get_watchlist,
    ]
    methods_str_length = len(str(len(methods)))

    print("\nExporting data...")
    for no, method in enumerate(methods, 1):
        method_start_time = time.time()

        args = {}
        if isinstance(method, list):
            method, args = method

        method_name = method.__name__
        method_name_without_prefix = strip_prefix(method_name)

        os.system(
            f"title [{len(methods)}/{no:0>{methods_str_length}}] Exporting {method_name}..."
        )
        print(
            f'[{len(methods)}/{no:0>{methods_str_length}}]: Processing "{method_name}" method',
            end=f" with args: {args}...\r" if args else "...\r",
        )

        try:
            data = method(user_instance, **args) if args else method(user_instance)

            file_path = build_path(user_folder, method_name_without_prefix)
            JsonFile.save(file_path, data)

            print(
                f"{time.time() - method_start_time:<7.2f} seconds - {method_name:<22} - {build_click_url(file_path)}.json"
            )
        except Exception as e:
            print(
                f"{time.time() - method_start_time:<7.2f} seconds - {method_name:<22} - Error: {e}"
            )

    os.system("title Completed!")
    print("\nProcessing complete!")
    print(f"\tTotal time: {time.time() - start_time:.2f} seconds")

    print("\tAt", build_click_url(user_folder), end="\n\n")
    if not args_exists():
        os.system("pause")


if __name__ == "__main__":
    main()
