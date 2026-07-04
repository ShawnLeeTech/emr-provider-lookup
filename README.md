# EMRTS Provider Lookup

## Overview

EMRTS Provider Lookup is a web application project for searching and locating healthcare providers using public provider data sources.

The goal is to create a clearer, more usable provider lookup experience by organizing provider identity, location, taxonomy, and search-related information into a structured application.

## Objective

The objective is to build a functional provider lookup system that allows users to search for healthcare providers through a simplified interface.

The application is planned to support provider search and lookup workflows such as:

- Searching by provider name
- Looking up providers by NPI
- Searching by location
- Filtering by provider taxonomy
- Displaying organized provider profile information

## Public Data Sources

The project is based on public healthcare provider data sources, including:

- CMS NPI Registry
- CMS NPPES downloadable data files
- NUCC Health Care Provider Taxonomy Code Set

## Planned Technology Stack

The planned technology stack includes:

- Python
- Django
- PostgreSQL
- HTML, CSS, and JavaScript
- Mermaid for documentation diagrams
- dbdiagram for ERD documentation

## Documentation

Project documentation is organized under the `docs` directory.

Current documentation includes:

- `docs/database/` - Database design notes, ERD documentation, Mermaid diagrams, and schema planning

## Development Roadmap

Planned development milestones include:

1. Define the initial provider lookup data model.
2. Create database diagrams using dbdiagram and Mermaid.
3. Build the initial PostgreSQL schema.
4. Develop the Django application structure.
5. Implement provider search and lookup functionality.
6. Create a basic web interface for demonstrating provider search results.
7. Refine documentation and deployment instructions as the project evolves.

## Repository Maintenance

This README should be updated when major project milestones are completed, such as database design, schema implementation, application setup, search functionality, or web interface progress.
