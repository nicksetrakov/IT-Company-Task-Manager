from django.contrib.auth import get_user_model
from social_core.pipeline.user import USER_FIELDS

User = get_user_model()


def create_user(
        strategy, details, backend, user=None, *args, **kwargs
) -> dict[str, bool] | None:
    if user:
        return {"is_new": False}

    fields = dict(
        (name, kwargs.get(name, details.get(name)))
        for name in backend.setting("USER_FIELDS", USER_FIELDS)
    )
    if not fields:
        return

    fields["password"] = User.objects.make_random_password()

    response = kwargs.get("response")
    fields["first_name"] = response.get("given_name")
    fields["last_name"] = response.get("family_name")
    fields["email"] = response.get("email")

    strategy.session_set("profile_picture", response.get("picture"))

    return {"is_new": True, "user": strategy.create_user(**fields)}
