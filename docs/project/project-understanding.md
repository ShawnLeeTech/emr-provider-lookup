# Project Understanding

This document summarizes the current understanding of the EMRTS Provider Lookup project.

## Assigned Route

The assigned project route is the Provider Lookup project.

## Project Objective

The objective is to build a working provider lookup system that allows users to search for and locate healthcare providers.

The project is intended to improve and simplify the existing provider search experience on the Centers for Medicare & Medicaid Services website.

## Core Data Sources

The main public data sources for this project are:

- CMS NPI Registry
- CMS NPPES downloadable data files
- NUCC Health Care Provider Taxonomy Code Set

## Preferred Technology

The preferred technology stack is:

- Python
- Django
- PostgreSQL

Other supporting tools may be used when appropriate.

## Current Workflow Focus

The current focus is to establish a complete and reliable internship workflow before deeper application development begins.

Current workflow priorities include:

- Maintaining the project in GitHub
- Updating GitHub regularly after completed work
- Documenting the development environment
- Documenting server tools
- Preparing database documentation
- Preparing future database diagrams using dbdiagram and/or Mermaid
- Preparing future web application progress for meeting demonstrations

## Database Design Principle

Real provider data should not be used as primary keys.

System-assigned numeric IDs should be used where appropriate, and real-world identifiers such as NPI numbers should be stored as data fields with appropriate uniqueness constraints when needed.

## Current Status

The project repository and documentation structure have been initialized.

Application code and detailed database design have not started yet.
