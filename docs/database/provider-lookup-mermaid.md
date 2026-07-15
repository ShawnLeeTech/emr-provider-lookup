# Provider Lookup ERD

Primary keys use UUIDs. Real-world identifiers such as NPI numbers and taxonomy codes are stored as unique data fields, not primary keys.

```mermaid
erDiagram
    DATA_SOURCES {
        uuid id PK
        varchar source_name
        varchar source_type
        text source_url
        text description
        timestamp created_at
        timestamp updated_at
    }

    PROVIDERS {
        uuid id PK
        varchar npi UK
        varchar entity_type_code
        varchar provider_first_name
        varchar provider_last_name
        varchar provider_middle_name
        varchar provider_credential
        varchar organization_name
        date enumeration_date
        date last_update_date
        timestamp created_at
        timestamp updated_at
    }

    TAXONOMY_CODES {
        uuid id PK
        varchar code UK
        varchar taxonomy_description
        varchar grouping
        varchar classification
        varchar specialization
        text definition
        varchar source_version
        timestamp created_at
        timestamp updated_at
    }

    IMPORT_BATCHES {
        uuid id PK
        uuid data_source_id FK
        varchar file_name
        varchar source_version
        timestamp import_started_at
        timestamp import_completed_at
        varchar status
        text notes
    }

    PROVIDER_ADDRESSES {
        uuid id PK
        uuid provider_id FK
        varchar address_type
        varchar address_line_1
        varchar address_line_2
        varchar city
        varchar state
        varchar zip_code
        varchar country_code
        varchar telephone_number
        timestamp created_at
        timestamp updated_at
    }

    PROVIDER_TAXONOMIES {
        uuid id PK
        uuid provider_id FK
        uuid taxonomy_code_id FK
        boolean is_primary
        varchar license_number
        varchar license_state
        timestamp created_at
        timestamp updated_at
    }

    DATA_SOURCES ||--o{ IMPORT_BATCHES : tracks
    PROVIDERS ||--o{ PROVIDER_ADDRESSES : has
    PROVIDERS ||--o{ PROVIDER_TAXONOMIES : has
    TAXONOMY_CODES ||--o{ PROVIDER_TAXONOMIES : describes
```

## Design Notes

- UUID primary keys are used for internal database identity.
- NPI numbers remain unique provider identifiers, but they are not primary keys.
- NUCC taxonomy codes remain unique taxonomy identifiers, but they are not primary keys.
- Provider identity, address, taxonomy, data source, and import tracking data are stored in separate tables.
