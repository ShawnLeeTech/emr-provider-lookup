# Database Documentation

This directory contains database design documentation for the EMRTS Provider Lookup project.

The database design supports a simplified healthcare provider lookup workflow using public provider data sources.

## Public Data Sources

The database design is based on:

- CMS NPPES downloadable data files
- NUCC Health Care Provider Taxonomy Code Set

## Search Fields

The current provider lookup interface supports six search fields:

- Taxonomy Description
- Provider First Name
- Provider Last Name
- City
- State
- Zip Code

## Files

Current database documentation includes:

- `provider-lookup-erd.dbml` - DBML ERD file for dbdiagram
- `provider-lookup-mermaid.md` - Mermaid ERD documentation for GitHub review
- `schema.sql` - Initial PostgreSQL schema reference

## Design Principles

The database design follows these principles:

- Use system-assigned UUIDs as primary keys.
- Store real-world identifiers, such as NPI numbers and taxonomy codes, as data fields.
- Do not use NPI or other real provider data as primary keys.
- Apply `NOT NULL` only to required identifier, relationship, search, source, import-tracking, and timestamp fields.
- Keep optional NPPES fields nullable because some fields may be missing or may depend on provider type.
- Keep provider identity, address, taxonomy, source, and import tracking data in separate tables.

## Current Implementation Status

The database design has been implemented in Django models and an initial migration.

Current implementation includes:

- Provider identity model
- Provider address model
- Taxonomy code model
- Provider-taxonomy relationship model
- Public data source tracking model
- Import batch tracking model
- Local sample data command
- NUCC taxonomy CSV import command
- CMS NPPES-style provider CSV import command
- Django Admin registration for database management
- Automated tests for search and import workflows
