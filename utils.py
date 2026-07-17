def format_balance(balance):
    return f"{balance:.2f} so'm"


def clean_username(username):
    if username:
        return "@" + username
    return "Username yo'q"
