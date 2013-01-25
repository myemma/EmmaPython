# Emma API Wrapper (Python)
[![Build Status](https://secure.travis-ci.org/dalanhurst/emma-api-wrapper-python.png)](http://travis-ci.org/dalanhurst/emma-api-wrapper-python)

## Documentation
Full documentation located at [Read the Docs](https://emma-api-wrapper-python.readthedocs.org/en/latest/)

## Examples
### Load all members

    from emma.model.account import Account
    acct = Account(account_id="x", public_key="y", private_key="z")
    acct.members.fetch_all() # Get a dictionary of all members for the account (paginated)

### Lazy-load a single member by ID

    from emma.model.account import Account
    acct = Account(account_id="x", public_key="y", private_key="z")
    member = acct.members.get(200) # Member() or None

### Lazy-load a single member by email

    from emma.model.account import Account
    acct = Account(account_id="x", public_key="y", private_key="z")
    member = acct.members.get("test@example.com") # Member() or None