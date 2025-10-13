from flask_admin.contrib.sqla.filters import BaseSQLAFilter

from app import db


class EnumFilter(BaseSQLAFilter):
    def __init__(self, column, name, enum_type, **kwargs):
        super(EnumFilter, self).__init__(column, name, **kwargs)
        self.enum_type = enum_type

    def apply(self, query, value, alias=None):
        return query.filter(self.column == self.enum_type(value))

    def operation(self):
        return "equals to"

    def get_options(self, view):
        return [
            (enum_member.value, enum_member.value)
            for enum_member in self.enum_type
        ]


class RelationshipFilter(BaseSQLAFilter):
    def __init__(
        self,
        column,
        name,
        related_model,
        related_field,
        join_model,
        join_condition,
        **kwargs,
    ):
        super(RelationshipFilter, self).__init__(column, name, **kwargs)
        self.related_model = related_model
        self.related_field = related_field
        self.join_model = join_model
        self.join_condition = join_condition

    def get_options(self, view):
        distinct_values = (
            db.session.query(self.related_model)
            .join(self.join_model, self.join_condition)
            .distinct(getattr(self.related_model, self.related_field))
            .all()
        )
        return [
            (
                getattr(item, self.related_field),
                getattr(item, self.related_field),
            )
            for item in distinct_values
        ]

    def apply(self, query, value, alias=None):
        return query.filter(self.column == value)

    def operation(self):
        return "equals to"
