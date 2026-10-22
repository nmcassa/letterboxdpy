<h2 id="search_class">Search Class & SearchFilter</h2>

Provides multi-category searching across Letterboxd with filtering, pagination, and lazy caching.

```python
from letterboxdpy.search import Search, SearchFilter

# Search across films
search = Search("Inception", SearchFilter.FILMS)

# Get first 5 results
results = search.get_results(num_results=5)
print(f"Total results on page: {results['count']}")

# Fetch multiple pages (e.g. 2 pages = 40 results)
paged_results = search.get_pages(num_pages=2)

# Lazy-loaded cached results property (fetches 20 results by default)
print(search.results)

# Switch filter on the same query
member_search = search.with_filter(SearchFilter.MEMBERS)
```

<details>
  <summary>Click to expand demo response</summary>

```json
{
  "available": true,
  "query": "Inception",
  "filter": "films",
  "end_page": 1,
  "count": 5,
  "results": [
    {
      "no": 1,
      "page": 1,
      "type": "film",
      "slug": "inception",
      "name": "Inception",
      "year": 2010,
      "url": "https://letterboxd.com/film/inception/",
      "poster": "https://a.ltrbxd.com/resized/film-poster/4/7/4/4/7/47447-inception-0-230-0-345-crop.jpg",
      "directors": [
        {
          "name": "Christopher Nolan",
          "slug": "christopher-nolan",
          "url": "https://letterboxd.com/director/christopher-nolan/"
        }
      ]
    },
    {
      "no": 2,
      "page": 1,
      "type": "film",
      "slug": "the-inception-of-the-terminator",
      "name": "The Inception of 'The Terminator'",
      "year": 2001,
      "url": "https://letterboxd.com/film/the-inception-of-the-terminator/",
      "poster": null,
      "directors": []
    }
  ]
}
```
</details>

### SearchFilter Enum Values

- `SearchFilter.ALL` (`""`)
- `SearchFilter.FILMS` (`"films"`)
- `SearchFilter.REVIEWS` (`"reviews"`)
- `SearchFilter.LISTS` (`"lists"`)
- `SearchFilter.ORIGINAL_LISTS` (`"original-lists"`)
- `SearchFilter.STORIES` (`"stories"`)
- `SearchFilter.CAST_CREW` (`"cast-crew"`)
- `SearchFilter.MEMBERS` (`"members"`)
- `SearchFilter.TAGS` (`"tags"`)
- `SearchFilter.ARTICLES` (`"articles"`)
- `SearchFilter.EPISODES` (`"episodes"`)
- `SearchFilter.FULL_TEXT` (`"full-text"`)
