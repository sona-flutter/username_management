from flask_marshmallow import Marshmallow
ma = Marshmallow()

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "user_id", "user_name", "user_nick_name", "phone_no",
            "user_address", "user_email", "user_bio",
            "user_date_of_birth", "user_age", "created_at", "updated_at"
        )
