# Database Documentation

This directory contains database design documentation for the EMRTS Provider Lookup project.

The database documentation will be used to describe the provider lookup data model, entity relationships, schema decisions, and diagram-based planning.

## Planned Contents

Planned database documentation includes:

- dbdiagram ERD files
- Mermaid database diagrams
- PostgreSQL schema notes
- Data source mapping notes
- Database design decisions

## Diagram Standards

This project will use:

- dbdiagram for ERD documentation
- Mermaid for diagrams included in Markdown documentation

## Design Principles

The database design should use system-assigned numeric IDs as primary keys where appropriate.

Real-world identifiers, such as NPI numbers, should be stored as data fields rather than used as primary keys. These fields may use uniqueness constraints when required by the data model.

## Planned Data Model Areas

The initial data model will focus on:

- Providers
- Provider identifiers
- Provider locations
- Provider taxonomy codes
- Public data source references
- Data import and update tracking
