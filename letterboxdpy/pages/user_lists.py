from letterboxdpy.constants.project import DOMAIN
from letterboxdpy.utils.lists_extractor import ListsExtractor


class UserLists:
    def __init__(self, username: str) -> None:
        self.username = username
        self.url = f"{DOMAIN}/{self.username}/lists"

    def get_lists(self, max_lists: int | None = None) -> dict:
        return ListsExtractor.from_url(self.url, max_lists)


if __name__ == "__main__":
    lists_instance = UserLists("fastfingertips")

    for data in lists_instance.get_lists()["lists"].values():
        for key, value in data.items():
            print(f"{key}: {value}")
        print("-" * 100)
