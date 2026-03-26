"""
User Settings Page Operations

Provides functionality to read and update user profile settings
on Letterboxd. Requires authenticated session.
"""

import contextlib
from typing import Any

from letterboxdpy.constants.forms.favorites import FAVORITE_ATTRS
from letterboxdpy.constants.forms.profile import PROFILE_FORM
from letterboxdpy.constants.project import (
    COMMUNICATION_AJAX_URL,
    NOTIFICATIONS_URL,
    PROFILE_UPDATE_URL,
    SETTINGS_URL,
)
from letterboxdpy.core.scraper import Scraper


class UserSettings:
    """User settings and profile management."""

    def __init__(self, session):
        self.session = session
        self._dom: Any | None = None
        self._form: Any | None = None
        self._profile_payload: dict[str, Any] | None = None
        self._notification_payload: dict[str, bool] | None = None

    def _fetch(self):
        """Fetch and parse settings page."""
        self._dom = Scraper.get_page(SETTINGS_URL)
        self._form = self._dom.find("form", id=PROFILE_FORM.FORM_ID)
        if not self._form:
            raise ValueError("Profile form not found. Session may be invalid.")

    def _get_input_value(self, name: str) -> str:
        if not self._form:
            return ""
        elem = self._form.find("input", {"name": name})
        val = elem.get("value", "") if elem else ""
        return str(val) if val is not None else ""

    def _get_textarea_value(self, name: str) -> str:
        if not self._form:
            return ""
        elem = self._form.find("textarea", {"name": name})
        return elem.get_text() if elem else ""

    def _get_select_value(self, name: str) -> str:
        if not self._form:
            return ""
        select = self._form.find("select", {"name": name})
        if not select:
            return ""
        opt = select.find("option", selected=True)  # type: ignore
        val = opt.get("value", "") if opt else ""
        return str(val)

    def _is_checkbox_checked(self, name: str) -> bool:
        if not self._form:
            return False
        cb = self._form.find("input", {"name": name, "type": "checkbox"})
        return cb is not None and cb.has_attr("checked")  # type: ignore

    def _extract_favorite_films(self) -> list[dict[str, str]]:
        """Extract favorite films (ID, name) from DOM or fallback to inputs."""
        if not self._dom or not self._form:
            return []

        films = []
        for comp in self._dom.find_all("div", class_=FAVORITE_ATTRS.COMPONENT_CLASS):
            film_id = comp.get(FAVORITE_ATTRS.FILM_ID_ATTR)
            film_name = comp.get(FAVORITE_ATTRS.FILM_NAME_ATTR)
            if film_id:
                films.append(
                    {"id": str(film_id), "name": str(film_name) or f"Film #{film_id}"}
                )

        if not films:
            for inp in self._form.find_all(
                "input", {"name": PROFILE_FORM.FAVORITE_FILMS_FIELD}
            ):
                fid = inp.get("value")
                if fid:
                    films.append({"id": str(fid), "name": f"Film #{fid}"})

        return films

    def get_profile(self) -> dict[str, Any]:
        """Fetch all profile settings and return valid payload."""
        self._fetch()

        payload: dict[str, Any] = {
            PROFILE_FORM.CSRF_FIELD: self._get_input_value(PROFILE_FORM.CSRF_FIELD),
            PROFILE_FORM.COMPLETE_SETTINGS_FIELD: "true",
            PROFILE_FORM.PASSWORD_FIELD: "",
        }

        for field in PROFILE_FORM.get_text_field_keys():
            payload[field] = self._get_input_value(field)

        for field in PROFILE_FORM.get_textarea_field_keys():
            payload[field] = self._get_textarea_value(field)

        for field in PROFILE_FORM.get_select_field_keys():
            payload[field] = self._get_select_value(field)

        for field in PROFILE_FORM.get_toggle_field_keys():
            payload[field] = "true" if self._is_checkbox_checked(field) else "false"

        fav_films = self._extract_favorite_films()
        payload["favouriteFilms"] = fav_films
        payload[PROFILE_FORM.FAVORITE_FILMS_FIELD] = [f["id"] for f in fav_films]

        self._profile_payload = payload
        return payload

    def _ajax_post(self, url: str, data: Any, referer: str) -> dict:
        """Internal helper for AJAX POST requests."""
        headers = {
            "Referer": referer,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        resp = self.session.api.post(url, data=data, headers=headers)
        return {
            "success": resp.status_code == 200,
            "status_code": resp.status_code,
            "response": resp,
        }

    def update_profile(self, payload: dict[str, Any]) -> dict:
        """Submit profile updates."""
        form_data = []
        for key, value in payload.items():
            if key == PROFILE_FORM.FAVORITE_FILMS_FIELD and isinstance(value, list):
                form_data.extend((key, str(fid)) for fid in value if fid)
            elif key != "favouriteFilms":
                form_data.append((key, str(value)))

        return self._ajax_post(PROFILE_UPDATE_URL, form_data, SETTINGS_URL)

    def get_favorite_films(self) -> list[dict[str, str]]:
        if not self._profile_payload:
            self.get_profile()

        if self._profile_payload:
            return self._profile_payload.get("favouriteFilms", [])  # type: ignore
        return []

    def set_favorite_films_order(self, new_order: list[str]) -> dict:
        if not self._profile_payload:
            self.get_profile()

        if self._profile_payload:
            self._profile_payload[PROFILE_FORM.FAVORITE_FILMS_FIELD] = new_order
            return self.update_profile(self._profile_payload)

        raise RuntimeError("Failed to load profile settings")

    # --- Notifications ---

    def get_notifications(self) -> dict[str, bool]:
        """Fetch current notification settings (Email & Push)."""
        dom = Scraper.get_page(NOTIFICATIONS_URL)
        checkboxes = dom.find_all("input", {"class": "ajax-action", "type": "checkbox"})

        states = {}
        # Parse all toggleable settings from the DOM
        for cb in checkboxes:
            name = cb.get("name")
            if name:
                states[str(name)] = cb.has_attr("checked")  # type: ignore

        self._notification_payload = states
        return states

    def update_notifications(self, settings: dict[str, bool]) -> list[dict]:
        """Update notification settings via AJAX."""
        results = []
        for key, value in settings.items():
            payload = {key: "true" if value else "false", "__csrf": self.session.csrf}
            res = self._ajax_post(COMMUNICATION_AJAX_URL, payload, NOTIFICATIONS_URL)

            # Safe JSON parsing
            response_data = res["response"].text
            if res["success"]:
                with contextlib.suppress(Exception):
                    response_data = res["response"].json()

            results.append(
                {"field": key, "success": res["success"], "response": response_data}
            )

        return results
