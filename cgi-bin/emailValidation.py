def validateEmail(email):
    "not a proper email -> return False"
    # ghetto validation
    if "." in email and "@" in email and len(email) <= 100:
        return(True)
    else:
        return(False)
