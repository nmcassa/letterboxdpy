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
