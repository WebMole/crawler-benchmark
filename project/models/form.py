from project import db
from project.models.generic_entry_mixin import GenericEntryMixin


class Form(GenericEntryMixin, db.Model):
    pass
