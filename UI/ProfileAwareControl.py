import Page
import Profile
from collections.abc import Callable
# Mixin to give any control a self.Profile that dtrt

class ProfileAwareControlMixin:
    GetParent : Callable
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.Page = None
        self.Profile = None
        # Set self.Page to the nearest Page in the parent chain;  self.Profile ditto
        testwin = self
        while parent := testwin.GetParent():
            if isinstance(parent, Page.Page) and not self.Page:
                self.Page = parent
            elif isinstance(parent, Profile.Profile) and not self.Profile:
                self.Profile = parent
            testwin = parent

