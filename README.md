# Google Cloud Utils

## Pypi publishing

https://www.digitalocean.com/community/tutorials/how-to-publish-python-packages-to-pypi-using-poetry-on-ubuntu-22-04

- Add token to `poetry`
- `poetry build`
- `poetry publish`

Note: package name has to be unique

## Pricing

### Google Cloud Storage

- Standard storage: $0.020 / GB for single region
- Operations:
  - Class A:  $0.005 per 1'000 operations.  1 million operations -> $5
    - insert
    - patch
    - update 
    - objects.list
  - Class B: $0.0004 per 1'000 operations. 10 million operations -> $4
    - get
  - Free:
    - buckets.delete
    - objects.delete

## Service Account with keys

- In the GCP console go to `IAM`
- Create new service Account
- Create new JSON key for service account
