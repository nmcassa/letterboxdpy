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
  "count": 3,
  "results": [
    {
      "no": 1,
      "page": 1,
      "type": "film",
      "slug": "inception",
      "title": "Inception",
      "year": 2010,
      "url": "https://letterboxd.com/film/inception/",
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
      "slug": "inception-1980",
      "title": "Inception",
      "year": 1980,
      "url": "https://letterboxd.com/film/inception-1980/",
      "directors": null
    },
    {
      "no": 3,
      "page": 1,
      "type": "film",
      "slug": "inception-the-cobol-job",
      "title": "Inception: The Cobol Job",
      "year": 2010,
      "url": "https://letterboxd.com/film/inception-the-cobol-job/",
      "directors": [
        {
          "name": "Ian Kirby",
          "slug": "ian-kirby",
          "url": "https://letterboxd.com/director/ian-kirby/"
        }
      ]
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
