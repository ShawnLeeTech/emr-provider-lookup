# EMRTS Provider Lookup

EMRTS Provider Lookup is a Django web application for searching and reviewing healthcare provider records through a simplified provider lookup workflow.

The project is designed around public healthcare provider data sources, including CMS NPPES downloadable data files and the NUCC Health Care Provider Taxonomy Code Set.

## Features

- Search provider records by taxonomy description, provider first name, provider last name, city, state, and zip code
- Support optional exact-match search
- Display provider search results with NPI, provider type, taxonomy, practice location, and phone information
- Provide a provider detail page with identity, practice location, and taxonomy profile information
- Configure Django Admin for managing providers, addresses, taxonomy codes, data sources, and import batches
- Provide sample data for local development
- Support NUCC taxonomy CSV import
- Support CMS NPPES-style provider CSV import
- Include automated tests for search views and import commands

## Technology Stack

- Python
- Django
- SQLite for local development
- HTML, CSS, and Django templates
- uv for Python dependency management

## Data Model

The application uses a normalized provider lookup data model:

- `providers` stores core provider identity information
- `provider_addresses` stores provider practice location information
- `taxonomy_codes` stores NUCC taxonomy code information
- `provider_taxonomies` connects providers with taxonomy codes
- `data_sources` tracks public data source references
- `import_batches` tracks data import activity

System-generated UUIDs are used as primary keys. Real-world identifiers, such as NPI numbers and taxonomy codes, are stored as data fields with uniqueness constraints where appropriate.

## Search Fields

The current provider lookup interface supports:

- Taxonomy Description
- Provider First Name
- Provider Last Name
- City
- State
- Zip Code

## Local Setup

Install dependencies:

    uv sync

Create a local environment file:

    cp .env.example .env

Apply database migrations:

    uv run python manage.py migrate

Load sample development data:

    uv run python manage.py seed_sample_data

Run the development server:

    uv run python manage.py runserver 127.0.0.1:8000

Open the application:

    http://127.0.0.1:8000/

## Admin Access

Create a local admin user:

    uv run python manage.py createsuperuser

Open the admin panel:

    http://127.0.0.1:8000/admin/

The admin panel includes provider records, provider addresses, taxonomy codes, provider taxonomy links, data sources, and import batches.

## Import Commands

Import NUCC taxonomy codes from a CSV file:

    uv run python manage.py import_taxonomy_codes path/to/taxonomy.csv --source-version manual-import

Import CMS NPPES-style provider records from a CSV file:

    uv run python manage.py import_nppes_providers path/to/nppes.csv --source-version manual-import

Optionally limit the number of provider rows imported:

    uv run python manage.py import_nppes_providers path/to/nppes.csv --source-version manual-import --limit 1000

## Testing

Run the provider app tests:

    uv run python manage.py test providers

The current tests cover:

- Homepage loading
- Provider search behavior
- Exact-match search behavior
- Provider detail page loading
- NUCC taxonomy import command
- CMS NPPES-style provider import command

## Current Status

The current implementation includes:

- Database model and initial migration
- Searchable provider lookup interface
- Provider detail page
- Django Admin configuration
- Local sample data command
- NUCC taxonomy CSV import command
- CMS NPPES-style provider CSV import command
- Automated tests for core search and import workflows

Future improvements may include larger NPPES data ingestion, pagination, advanced filters, deployment configuration, and additional validation rules.
