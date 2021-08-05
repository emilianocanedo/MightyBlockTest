from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
Base = declarative_base(metadata=meta)


class UpdateMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)