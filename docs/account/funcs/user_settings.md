<h2 id="user_settings">UserSettings (Account Settings Management)</h2>

Allows reading and updating profile details and notification preferences on Letterboxd. Requires an active `UserSession`.

```python
from letterboxdpy.account.settings import UserSettings
from letterboxdpy.auth import UserSession

session = UserSession.ensure()
settings = UserSettings(session)

# 1. Profile operations
profile = settings.get_profile()
print(f"Current Bio: {profile.get('bio')}")
print(f"Current Location: {profile.get('location')}")

# Update profile fields
settings.update_profile({
    "location": "New York, USA",
    "website": "https://letterboxd.com",
    "bio": "Cinephile and developer."
})

# 2. Notification operations
notifications = settings.get_notifications()
print(notifications)

# Update notification preferences
settings.update_notifications({
    "emailEditorial": True,
    "pushFollowers": False
})
```

<details>
  <summary>Click to expand demo response for <code>get_profile</code></summary>

```json
{
  "__csrf": "<csrf-token>",
  "completeSettings": "true",
  "password": "",
  "givenName": "Jane",
  "familyName": "Doe",
  "emailAddress": "jane.doe@example.com",
  "location": "New York, USA",
  "website": "https://example.com",
  "bio": "Cinephile and developer.",
  "pronoun": "she/her",
  "favouriteFilms": [
    {
      "id": "51400",
      "name": "V for Vendetta"
    },
    {
      "id": "47447",
      "name": "Inception"
    },
    {
      "id": "240344",
      "name": "La La Land"
    },
    {
      "id": "20956",
      "name": "Black Swan"
    }
  ]
}
```
</details>

<details>
  <summary>Click to expand demo response for <code>get_notifications</code></summary>

```json
{
  "emailEditorial": true,
  "emailWeekly": false,
  "emailDigest": true,
  "emailFollowers": true,
  "emailReplies": true,
  "pushFollowers": false,
  "pushReplies": true,
  "pushLikes": true
}
```
</details>
