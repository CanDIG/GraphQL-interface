# Technical Debt

While the GraphQL interface is quite stable and serviceable in its current format, there are still several improvements that could be made to improve its use.

## Async GraphQL Interface

Currently, part of the reason the GraphQL interface is so slow is that it needs to call the Katsu and CanDIG variants service APIs. While we can't do anything to speed up these microservices, we can try to improve the speed of the GraphQL interface by implementing Async requests.

This may involve writing the requests using an async HTTP library, like aiohttp to perform the needed requests. It may also be beneficial to split the large katsu calls into smaller calls so that the async implementation may be more efficient.

We also may wish to improve the async functionality of the GraphQL interface by rebuilding many of the functions in a style consistent with asynchronous python, to take full advantage of what it offers (eg. using `async for` to complete loops instead of the regular `for` loops in an async function).

## Making .dockerignore Robust

The root `.dockerignore` file currently ignores the documentation and testing folders, however, we should also add some of the .gitignore file endings to it so that the creation of a Docker container doesn't include excess files & folders from the host, like a `venv` or `__pycache__`.

## Troubleshooting Aggregate Queries

The Aggregate Queries section is broken in its current implementation.

## Improving Beacon Resolver Function

After fixes to the GraphQL interface filter, it should now be possible to improve the GraphQL Beacon Implementation to allow for filtering by subject id.

This could be done by changing lines like this (api/schemas/beacon/beacon_data_models.py:237):

```python
all_mcode_data = await generic_resolver(info, "mcode_packets_loader", None, MCodePacket)
```

to something like this:

```python
all_mcode_data = await generic_resolver(info, "mcode_packets_loader", MCodePacketInputType(...), MCodePacket)
```

## Clean up Repo Branches

There are several branches that exist within the GraphQL interface repo. Some of these are old and out of date. We may need to delete these, or at least bring them up to date with the current default `master` branch.

We may need to delete the `main` branch if we are going to continue using the `master` branch as our default branch.

## Clean up utils.py file

The current `utils.py` is laid out in a way that can get complex to traverse. It may be worth splitting up into several files (eg. one for default values, like `POST_SEARCH_BODY`, another simply for requests, and another simply for filtering, etc.).

## Update Documentation

The documentation for this repo has not been meaningfully updated since the creation of the Beacon endpoint, so we may need to update it to incorporate recent changes.

## Updating Requirements

Not all of the requirements currently listed in the `requirements.txt` file are necessary for the GraphQL interface. Some, like `aiofiles`, are used simply for the scripts present in the documentation, and thus can be removed. Ensure that the documentation scripts have this change noted down.

## Connecting GraphQL interface to Data Backend

A long-term goal for our GraphQL interface should be to connect it to its own data services to improve its performance.

<hr/>

## Improvements
When adding any technical improvements that are listed in this file as technical debts, create a new branch called `technical-debt-<FEATURE_NAME>` and create a PR to merge the new branch into the `technical-debt` branch, from where we can merge the changes into `master`.
