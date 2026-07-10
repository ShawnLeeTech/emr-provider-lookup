# Database Documentation

This directory contains database design documentation for the EMRTS Provider Lookup project.

The database design supports a simplified provider lookup interface based on the following search fields:

- Taxonomy Description
- Provider First Name
- Provider Last Name
- City
- State
- Zip Code

## Public Data Sources

The database design is based on the following public data sources:

- CMS NPPES downloadable data files
- NUCC Health Care Provider Taxonomy Code Set

## Planned Contents

Database documentation includes:

- dbdiagram ERD files
- Mermaid database diagrams
- PostgreSQL schema notes
- Data source mapping notes
- Database design decisions

## Diagram Standards

This project uses:

- dbdiagram for ERD documentation
- Mermaid for diagrams included in Markdown documentation

## Design Principles

The database design should use system-assigned numeric IDs as primary keys where appropriate.

Real-world identifiers, such as NPI numbers, should be stored as data fields rather than used as primary keys. These fields may use uniqueness constraints when required by the data model.

The first version of the database should stay focused on the simplified provider search workflow and avoid unnecessary complexity.

## Initial Data Model Areas

The initial data model focuses on:

- Providers
- Provider addresses
- Provider taxonomy codes
- Public data sources
- Data import tracking
