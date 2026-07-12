# EMRTS Provider Lookup

## Overview

EMRTS Provider Lookup is a web application project for searching and locating healthcare providers using public provider data sources.

The goal is to create a simpler provider lookup experience by focusing on the most important search fields and presenting provider information in a clear and usable format.

## Objective

The objective is to build a functional provider lookup system that allows users to search for healthcare providers through a simplified interface.

The initial search interface will focus on:

- Taxonomy Description
- Provider First Name
- Provider Last Name
- City
- State
- Zip Code

## Public Data Sources

The project is based on the following public healthcare provider data sources:

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

- `docs/database/` - Database design notes, ERD documentation, Mermaid diagrams, DBML files, and PostgreSQL schema planning

## Project Roadmap

Completed foundation work includes:

1. Defined the initial provider lookup data model.
2. Created database diagrams using dbdiagram and Mermaid.
3. Built the initial PostgreSQL schema.
4. Set up the Django project structure.
5. Created the initial provider search homepage.

Next development milestones include:

1. Build Django models based on the approved database design.
2. Connect the application to PostgreSQL.
3. Implement provider search functionality using the simplified search fields.
4. Display provider search results in a clean and professional interface.
5. Refine documentation and implementation as the project evolves.

## Repository Maintenance

This README should be updated when major project milestones are completed, such as database design, schema implementation, application setup, search functionality, or web interface progress.

## Implementation Status

The project has moved from initial database design into application setup.

Current implementation progress includes:

- Python project configuration using `uv`
- Django project setup
- `providers` application setup
- Initial provider search homepage
- Static CSS styling for a clean professional interface
- Initial search form based on the six approved search fields

The current homepage is a front-end structure only. Search logic and database integration will be added in later steps.

## Current Application Structure

- `provider_lookup/` - Django project configuration
- `providers/` - Provider lookup application
- `templates/providers/home.html` - Initial provider search page
- `static/css/styles.css` - Initial UI styling
- `docs/database/` - Database design, ERD, DBML, and PostgreSQL schema documentation
