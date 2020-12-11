# pgeu-system <br/> Non-Profit Organization and Conference Management System

## Introduction

pgeu-system is a system for managing non-profit organizations along with an
extensive conference management system.

## Features

### Conference Administration

The conference management system includes time reports, cross conference emails,
conference series and individual conference management including registration,
waitlisting, attendee emails, a wiki, individual signups, invoicing, sessions,
scheduling, sponsorship management, news, prepaid vouchers and discount codes,
volunteer scheduling, lots of reports, and more.

### Invoice Management

The invoicing system supports creating individual invoices, and is linked into
the conference and membership parts of the system, and into the accounting
system.

### News

News posts to the main website as well as integration with social media systems
is included.

### Accounting

A structured accounting system with account classes, groups, individual accounts
and objects is built into the system and integrated with the conference management,
membership, and invoice systems.

### Membership

Simple membership tracking and membership dues are suppoerted.

### Elections

Multi-seat elections are supported (eg: for voting in new board members).

## Contributions

Contributions to pgeu-system are certainly welcome!

Please feel free to create PRs or issues for any bugs found in the pgeu-system-
note that the specific websites which are running pgeu-system are able to 'skin'
the system, so in many cases if you find a 404 or similar on a website running
pgeu-system, that's an issue you'll need to address with that particular organization
and is not a pgeu-system bug or issue.

If you are interested in contributing to the development of pgeu-system by
working on new features, please reach out to us first and discuss your feature
idea.  Once a feature has been discussed and the general concept agreed to, a
feature issue can be opened to work on the details of the implementation.

The mailing list for discussing pgeu-system is <pgeu-system@lists.postgresql.eu>.

### dev environment

A suggested way to get started developing is to have create a `.env` based on `environment.env` and change your secrets. `.env` is in the `.gitignore` to help you keep these secret.

Also choose 1 of the following.

#### virtualenv

This will setup a venv that has the requirements installed.

```sh
python3 -m venv .venv
.venv/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' .env | xargs -d '\r\n');
```

#### pipenv

A alternative that uses Pipfile and Pipfile.lock

```sh
python3 -m pip install pipenv
python3 -m pipenv install
python3 -m pipenv shell
```

Keep `requirements.txt` upto date for those without `pipenv`

```sh
jq -r '.default
        | to_entries[]
        | .key + .value.version' \
    Pipfile.lock > requirements.txt
```

### Database migrations

```sh
python manage.py migrate
```

### Run django

```sh
python manage.py runserver
```
