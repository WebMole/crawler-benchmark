from project import db
from project.models.generic_entry_mixin import GenericEntryMixin


class Newsfeed(GenericEntryMixin, db.Model):
    pass
