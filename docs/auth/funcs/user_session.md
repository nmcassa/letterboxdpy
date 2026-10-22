<h2 id="user_session">UserSession (Authentication & Sessions)</h2>

Handles session management, login flows, and cookie persistence for authenticated Letterboxd actions.

```python
from pathlib import Path
from letterboxdpy.auth import UserSession

# 1. Automatic session handling: loads saved cookie or prompts for credentials
session = UserSession.ensure()

# 2. Programmatic fresh login and save to custom location
# session = UserSession.login("username", "password", Path(".cookie/session.json"))

# 3. Load saved session from disk
# session = UserSession.load(Path(".cookie/session.json"))

# Validate if current session is still active
if session.validate():
    print(f"Authenticated as: {session.username}")
    print(f"Session CSRF token: {session.csrf}")
```

<details>
  <summary>Click to expand demo output</summary>

```text
Authenticated as: nmcassa
Session CSRF token: 9a8b7c6d5e4f3a2b1c0d
```
</details>

### CLI Authentication

You can authenticate directly from the command line:

```bash
# Check current saved session or prompt if missing/expired
python -m letterboxdpy.auth

# Force re-authentication with new credentials
python -m letterboxdpy.auth --login -u <username>
```
