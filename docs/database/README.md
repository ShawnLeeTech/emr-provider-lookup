# Database Documentation

This directory contains database design documentation for the EMRTS Provider Lookup project.

The database design supports a simplified healthcare provider lookup workflow using public provider data sources.

## Public Data Sources

The database design is based on:

- CMS NPPES downloadable data files
- NUCC Health Care Provider Taxonomy Code Set

## Search Fields

The first version of the application focuses on six search fields:

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
- `schema.sql` - Initial PostgreSQL schema

## Design Principles

The database design follows these principles:

- Use system-assigned numeric IDs as primary keys.
- Store real-world identifiers, such as NPI numbers, as data fields.
- Do not use NPI or other real provider data as primary keys.
- Apply `NOT NULL` only to required identifier, relationship, search, source, import-tracking, and timestamp fields.
- Keep optional NPPES fields nullable because some fields may be missing or may depend on provider type.
- Keep provider identity, address, taxonomy, and import tracking data in separate tables.

## Initial Data Model Areas

The initial data model focuses on:

- Providers
- Provider addresses
- Provider taxonomy codes
- Public data sources
- Data import tracking

## Implementation Direction

The database design is prepared for future Django and PostgreSQL implementation.

The next development phase will focus on creating a clean provider search interface and connecting it to the database structure.
