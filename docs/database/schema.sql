-- Provider Lookup Database Schema
-- Initial PostgreSQL schema for the EMRTS Provider Lookup project.
-- The design supports a simplified provider search workflow using:
-- Taxonomy Description, Provider First Name, Provider Last Name, City, State, and Zip Code.

CREATE TABLE data_sources (
    id BIGSERIAL PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(100) NOT NULL,
    source_url TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE import_batches (
    id BIGSERIAL PRIMARY KEY,
    data_source_id BIGINT NOT NULL REFERENCES data_sources(id),
    file_name VARCHAR(255) NOT NULL,
    source_version VARCHAR(100),
    import_started_at TIMESTAMP NOT NULL,
    import_completed_at TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    notes TEXT
);

CREATE TABLE providers (
    id BIGSERIAL PRIMARY KEY,
    npi VARCHAR(10) NOT NULL UNIQUE,
    entity_type_code VARCHAR(1) NOT NULL,
    provider_first_name VARCHAR(100),
    provider_last_name VARCHAR(100),
    provider_middle_name VARCHAR(100),
    provider_credential VARCHAR(50),
    organization_name VARCHAR(255),
    enumeration_date DATE,
    last_update_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE provider_addresses (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    address_type VARCHAR(50) NOT NULL,
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country_code VARCHAR(10),
    telephone_number VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE taxonomy_codes (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    taxonomy_description VARCHAR(255) NOT NULL,
    grouping VARCHAR(255),
    classification VARCHAR(255),
    specialization VARCHAR(255),
    definition TEXT,
    source_version VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE provider_taxonomies (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    taxonomy_code_id BIGINT NOT NULL REFERENCES taxonomy_codes(id),
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    license_number VARCHAR(100),
    license_state VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (provider_id, taxonomy_code_id, license_number, license_state)
);

CREATE INDEX idx_providers_first_name
    ON providers (provider_first_name);

CREATE INDEX idx_providers_last_name
    ON providers (provider_last_name);

CREATE INDEX idx_provider_addresses_city
    ON provider_addresses (city);

CREATE INDEX idx_provider_addresses_state
    ON provider_addresses (state);

CREATE INDEX idx_provider_addresses_zip_code
    ON provider_addresses (zip_code);

CREATE INDEX idx_taxonomy_codes_description
    ON taxonomy_codes (taxonomy_description);

CREATE INDEX idx_provider_taxonomies_provider_id
    ON provider_taxonomies (provider_id);

CREATE INDEX idx_provider_taxonomies_taxonomy_code_id
    ON provider_taxonomies (taxonomy_code_id);
