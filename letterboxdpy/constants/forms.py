"""Form field definitions."""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class FormField:
    """Single form field."""
    key: str
    label: str
    field_type: str
    options: Tuple[str, ...] = ()
    required: bool = False
    
    def get_options(self) -> Tuple[str, ...]:
        return self.options
    
    def is_valid_value(self, value: str) -> bool:
        if not self.options: return True
        return value in self.options


# PROFILE FORM FIELDS
# Visual order as they appear on Letterboxd settings

PROFILE_EDITABLE_FIELDS: Tuple[FormField, ...] = (
    # Name
    FormField(key="username", label="Username", field_type="text"),
    FormField(key="givenName", label="Given Name", field_type="text"),
    FormField(key="familyName", label="Family Name", field_type="text"),
    
    # Contact/Location
    FormField(key="emailAddress", label="Email Address", field_type="text"),
    FormField(key="location", label="Location", field_type="text"),
    FormField(key="website", label="Website", field_type="text"),
    
    # Bio
    FormField(key="bio", label="Bio", field_type="textarea"),
    
    # Identity
    FormField(
        key="pronoun", 
        label="Pronoun", 
        field_type="select",
        options=("They", "He", "HeThem", "She", "SheThem", "Xe", "ZeHir", "ZeZir", "It")
    ),
    
    # Preferences
    FormField(
        key="posterMode", 
        label="Posters",
        field_type="select",
        options=("All", "Theirs", "Yours", "None")
    ),
    FormField(
        key="commentPolicy", 
        label="Replies", 
        field_type="select",
        options=("Anyone", "Friends", "You")
    ),
    
    # Checkboxes
    FormField(key="privacyIncludeInPeopleSection", label="Show in Members", field_type="toggle"),
    FormField(key="showAdultContent", label="Adult Content", field_type="toggle"),
)

# Helper lists
PROFILE_TEXT_FIELDS = tuple(f for f in PROFILE_EDITABLE_FIELDS if f.field_type == "text")
PROFILE_TEXTAREA_FIELDS = tuple(f for f in PROFILE_EDITABLE_FIELDS if f.field_type == "textarea")
PROFILE_SELECT_FIELDS = tuple(f for f in PROFILE_EDITABLE_FIELDS if f.field_type == "select")
PROFILE_TOGGLE_FIELDS = tuple(f for f in PROFILE_EDITABLE_FIELDS if f.field_type == "toggle")


@dataclass
class ProfileFormFields:
    """Field definitions for user profile form."""
    
    FORM_ID: str = "user-update"
    CSRF_FIELD: str = "__csrf"
    
    # Hidden/system fields
    COMPLETE_SETTINGS_FIELD: str = "completeSettings"
    EMAIL_FIELD: str = "emailAddress"
    PASSWORD_FIELD: str = "password"
    
    # Favorite films
    FAVORITE_FILMS_FIELD: str = "favouriteFilmIds"
    
    def get_all_fields(self) -> Tuple[FormField, ...]:
        return PROFILE_EDITABLE_FIELDS
    
    def get_field(self, key: str) -> Optional[FormField]:
        for f in PROFILE_EDITABLE_FIELDS:
            if f.key == key: return f
        return None
    
    def get_text_field_keys(self) -> Tuple[str, ...]:
        return tuple(f.key for f in PROFILE_TEXT_FIELDS)
    
    def get_textarea_field_keys(self) -> Tuple[str, ...]:
        return tuple(f.key for f in PROFILE_TEXTAREA_FIELDS)
    
    def get_select_field_keys(self) -> Tuple[str, ...]:
        return tuple(f.key for f in PROFILE_SELECT_FIELDS)
    
    def get_toggle_field_keys(self) -> Tuple[str, ...]:
        return tuple(f.key for f in PROFILE_TOGGLE_FIELDS)
    
    def get_select_options(self, key: str) -> Tuple[str, ...]:
        f = self.get_field(key)
        return f.options if f else ()


@dataclass  
class FavoriteFilmAttributes:
    """HTML attributes for favorite film extraction."""
    COMPONENT_CLASS: str = "react-component"
    FILM_ID_ATTR: str = "data-film-id"
    FILM_NAME_ATTR: str = "data-item-name"
    FILM_SLUG_ATTR: str = "data-item-slug"
    FILM_LINK_ATTR: str = "data-item-link"


# Convenience instances
PROFILE_FORM = ProfileFormFields()
FAVORITE_ATTRS = FavoriteFilmAttributes()
