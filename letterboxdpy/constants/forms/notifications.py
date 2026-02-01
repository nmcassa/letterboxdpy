"""Notification form field definitions."""

from dataclasses import dataclass

@dataclass
class NotificationFormFields:
    """Field definitions for notification settings (email & push)."""
    
    # Email Notifications (Activity)
    NEW_FOLLOWERS_EMAIL: str = "notifyWhenFollowed"
    COMMENT_REPLIES_EMAIL: str = "audienceParticipant"
    FOLLOWED_ONLY_EMAIL: str = "notifyFromFollowedOnly"
    
    # Email Notifications (Watchlist)
    WATCHLIST_BUY_EMAIL: str = "notifyBuyAvailability"
    WATCHLIST_RENT_EMAIL: str = "notifyRentAvailability"
    WATCHLIST_STREAM_EMAIL: str = "notifyAvailability"
    WATCHLIST_VIDEO_STORE_EMAIL: str = "notifyVideoStoreAvailability"
    
    # Email Notifications (General/Newsletters)
    NEWS_EDITORIAL: str = "optinEditorial"
    NEWS_WEEKLY_RUSHES: str = "optinWeeklyDigest"
    NEWS_GENERAL: str = "optin"
    NEWS_SHELF_LIFE: str = "optinShelfLife"
    NEWS_BEST_IN_SHOW: str = "optinBestInShow"
    NEWS_PARTNER_OFFERS: str = "optinPartners"
    
    # Push Notifications (Activity)
    NEW_FOLLOWERS_PUSH: str = "pushNotificationsForNewFollowers"
    COMMENT_REPLIES_PUSH: str = "pushNotificationsForComments"
    REVIEW_LIKES_PUSH: str = "pushNotificationsForReviewLikes"
    LIST_LIKES_PUSH: str = "pushNotificationsForListLikes"
    FOLLOWED_ONLY_PUSH: str = "pushNotificationsFromFollowedOnly"
    
    # Push Notifications (Watchlist)
    WATCHLIST_BUY_PUSH: str = "pushNotificationsForBuyAvailability"
    WATCHLIST_RENT_PUSH: str = "pushNotificationsForRentAvailability"
    WATCHLIST_STREAM_PUSH: str = "pushNotificationsForAvailability"
    
    # Push Notifications (General)
    ALERTS_GENERAL_PUSH: str = "pushNotificationsForGeneralAnnouncements"
    PARTNER_OFFERS_PUSH: str = "pushNotificationsForPartnerMessages"

# Notification groups with labels for UI presentation
NOTIFICATION_GROUPS = {
    "Email - Activity": (
        ("New Followers", NotificationFormFields.NEW_FOLLOWERS_EMAIL),
        ("Comment Replies", NotificationFormFields.COMMENT_REPLIES_EMAIL),
        ("Followed Only", NotificationFormFields.FOLLOWED_ONLY_EMAIL),
    ),
    "Email - Watchlist": (
        ("Watchlist Buy", NotificationFormFields.WATCHLIST_BUY_EMAIL),
        ("Watchlist Rent", NotificationFormFields.WATCHLIST_RENT_EMAIL),
        ("Watchlist Stream", NotificationFormFields.WATCHLIST_STREAM_EMAIL),
        ("Video Store", NotificationFormFields.WATCHLIST_VIDEO_STORE_EMAIL),
    ),
    "Email - General": (
        ("Editorial", NotificationFormFields.NEWS_EDITORIAL),
        ("Weekly Rushes", NotificationFormFields.NEWS_WEEKLY_RUSHES),
        ("General News", NotificationFormFields.NEWS_GENERAL),
        ("Shelf Life", NotificationFormFields.NEWS_SHELF_LIFE),
        ("Best in Show", NotificationFormFields.NEWS_BEST_IN_SHOW),
        ("Partner Offers", NotificationFormFields.NEWS_PARTNER_OFFERS),
    ),
    "Push - Activity": (
        ("New Followers", NotificationFormFields.NEW_FOLLOWERS_PUSH),
        ("Comment Replies", NotificationFormFields.COMMENT_REPLIES_PUSH),
        ("Review Likes", NotificationFormFields.REVIEW_LIKES_PUSH),
        ("List Likes", NotificationFormFields.LIST_LIKES_PUSH),
        ("Followed Only", NotificationFormFields.FOLLOWED_ONLY_PUSH),
    ),
    "Push - Watchlist & General": (
        ("Watchlist Buy", NotificationFormFields.WATCHLIST_BUY_PUSH),
        ("Watchlist Rent", NotificationFormFields.WATCHLIST_RENT_PUSH),
        ("Watchlist Stream", NotificationFormFields.WATCHLIST_STREAM_PUSH),
        ("General Alerts", NotificationFormFields.ALERTS_GENERAL_PUSH),
        ("Partner Offers", NotificationFormFields.PARTNER_OFFERS_PUSH),
    )
}

# Convenience instances
NOTIFICATIONS_FORM = NotificationFormFields()
