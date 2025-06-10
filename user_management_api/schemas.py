from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import User

ma = Marshmallow()

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = (
            "user_id", "user_name", "user_nick_name", "phone_no",
            "user_address", "user_email", "user_bio",
            "user_date_of_birth", "user_age", "created_at", "updated_at"
        )
    
    # Explicitly define date field to handle serialization properly
    user_date_of_birth = fields.Date(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
