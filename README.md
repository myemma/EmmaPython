# Emma API Wrapper (Python)
[![Build Status](https://secure.travis-ci.org/dalanhurst/emma-api-wrapper-python.png)](http://travis-ci.org/dalanhurst/emma-api-wrapper-python)

## Examples
### Load all members

    from myemma import *
    emma_account = Account(account_id="x", public_key="y", private_key="z")
    members = emma_account.members.fetch_all()

### Lazy-load a single member by ID

    from myemma import *
    emma_account = Account(account_id="x", public_key="y", private_key="z")
    member = emma_account.members[200] # Member() or None

### Lazy-load a single member by email

    from myemma import *
    emma_account = Account(account_id="x", public_key="y", private_key="z")
    member = emma_account.members["test@example.com"] # Member() or None