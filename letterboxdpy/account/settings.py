"""
User Settings Page Operations

Provides functionality to read and update user profile settings
on Letterboxd. Requires authenticated session.
"""

from typing import Dict, List, Any, Optional
from letterboxdpy.core.scraper import Scraper
from letterboxdpy.constants.project import SETTINGS_URL, PROFILE_UPDATE_URL
from letterboxdpy.constants.forms import PROFILE_FORM, FAVORITE_ATTRS


class UserSettings:
    """User settings and profile management."""
    
    def __init__(self, session):
        self.session = session
        self._dom: Optional[Any] = None
        self._form: Optional[Any] = None
        self._payload: Optional[Dict[str, Any]] = None
    
    def _fetch(self):
        """Fetch and parse settings page."""
        self._dom = Scraper.get_page(SETTINGS_URL)
        self._form = self._dom.find("form", id=PROFILE_FORM.FORM_ID)
        if not self._form:
            raise ValueError("Profile form not found. Session may be invalid.")
    
    def _get_input_value(self, name: str) -> str:
        if not self._form: return ""
        elem = self._form.find("input", {"name": name})
        val = elem.get("value", "") if elem else ""
        return str(val) if val is not None else ""
    
    def _get_textarea_value(self, name: str) -> str:
        if not self._form: return ""
        elem = self._form.find("textarea", {"name": name})
        return elem.get_text() if elem else ""
    
    def _get_select_value(self, name: str) -> str:
        if not self._form: return ""
        select = self._form.find("select", {"name": name})
        if not select: return ""
        opt = select.find("option", selected=True)  # type: ignore
        val = opt.get("value", "") if opt else ""
        return str(val)
    
    def _is_checkbox_checked(self, name: str) -> bool:
        if not self._form: return False
        cb = self._form.find("input", {"name": name, "type": "checkbox"})
        return cb is not None and cb.has_attr("checked")  # type: ignore
    
    def _extract_favorite_films(self) -> List[Dict[str, str]]:
        """Extract favorite films (ID, name) from DOM or fallback to inputs."""
        if not self._dom or not self._form: return []
        
        films = []
        for comp in self._dom.find_all("div", class_=FAVORITE_ATTRS.COMPONENT_CLASS):
            film_id = comp.get(FAVORITE_ATTRS.FILM_ID_ATTR)
            film_name = comp.get(FAVORITE_ATTRS.FILM_NAME_ATTR)
            if film_id:
                films.append({
                    "id": str(film_id),
                    "name": str(film_name) or f"Film #{film_id}"
                })
        
        if not films:
            for inp in self._form.find_all("input", {"name": PROFILE_FORM.FAVORITE_FILMS_FIELD}):
                fid = inp.get("value")
                if fid:
                    films.append({"id": str(fid), "name": f"Film #{fid}"})
        
        return films
    
    def get_profile(self) -> Dict[str, Any]:
        """Fetch all profile settings and return valid payload."""
        self._fetch()
        
        payload: Dict[str, Any] = {
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
        
        self._payload = payload
        return payload
    
    def update_profile(self, payload: Dict[str, Any]) -> dict:
        """Submit profile updates."""
        form_data = []
        for key, value in payload.items():
            if key == PROFILE_FORM.FAVORITE_FILMS_FIELD and isinstance(value, list):
                for fid in value:
                    if fid:
                        form_data.append((key, str(fid)))
            elif key != "favouriteFilms":
                form_data.append((key, str(value)))
        
        headers = {
            "Referer": SETTINGS_URL,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        
        resp = self.session.api.post(PROFILE_UPDATE_URL, data=form_data, headers=headers)
        
        return {
            "success": resp.status_code == 200,
            "status_code": resp.status_code,
            "response": resp
        }
    
    def get_favorite_films(self) -> List[Dict[str, str]]:
        if not self._payload:
            self.get_profile()
            
        if self._payload:
            return self._payload.get("favouriteFilms", []) # type: ignore
        return []

    def set_favorite_films_order(self, new_order: List[str]) -> dict:
        if not self._payload:
            self.get_profile()
        
        if self._payload:
            self._payload[PROFILE_FORM.FAVORITE_FILMS_FIELD] = new_order
            return self.update_profile(self._payload)
        
        raise RuntimeError("Failed to load profile settings")
