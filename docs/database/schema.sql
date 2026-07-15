-- EMRTS Provider Lookup PostgreSQL schema reference
-- Primary keys use UUIDs. Real-world identifiers such as NPI numbers
-- and taxonomy codes are stored as unique data fields, not primary keys.

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(100) NOT NULL,
    source_url TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    npi VARCHAR(10) NOT NULL UNIQUE,
    entity_type_code VARCHAR(1) NOT NULL,
    provider_first_name VARCHAR(100),
    provider_last_name VARCHAR(100),
    provider_middle_name VARCHAR(100),
    provider_credential VARCHAR(50),
    organization_name VARCHAR(255),
    enumeration_date DATE,
    last_update_date DATE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE taxonomy_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(20) NOT NULL UNIQUE,
    taxonomy_description VARCHAR(255) NOT NULL,
    grouping VARCHAR(255),
    classification VARCHAR(255),
    specialization VARCHAR(255),
    definition TEXT,
    source_version VARCHAR(100),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE import_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data_source_id UUID NOT NULL REFERENCES data_sources(id),
    file_name VARCHAR(255) NOT NULL,
    source_version VARCHAR(100),
    import_started_at TIMESTAMP NOT NULL,
    import_completed_at TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    notes TEXT
);

CREATE TABLE provider_addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    address_type VARCHAR(50) NOT NULL,
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    country_code VARCHAR(10),
    telephone_number VARCHAR(50),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE provider_taxonomies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    taxonomy_code_id UUID NOT NULL REFERENCES taxonomy_codes(id),
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    license_number VARCHAR(100),
    license_state VARCHAR(50),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    CONSTRAINT uq_provider_taxonomy_license
        UNIQUE (provider_id, taxonomy_code_id, license_number, license_state)
);

CREATE INDEX idx_prov_first_name ON providers(provider_first_name);
CREATE INDEX idx_prov_last_name ON providers(provider_last_name);

CREATE INDEX idx_tax_desc ON taxonomy_codes(taxonomy_description);

CREATE INDEX idx_imp_source ON import_batches(data_source_id);

CREATE INDEX idx_addr_provider ON provider_addresses(provider_id);
CREATE INDEX idx_addr_city ON provider_addresses(city);
CREATE INDEX idx_addr_state ON provider_addresses(state);
CREATE INDEX idx_addr_zip_code ON provider_addresses(zip_code);

CREATE INDEX idx_pt_provider ON provider_taxonomies(provider_id);
CREATE INDEX idx_pt_taxonomy ON provider_taxonomies(taxonomy_code_id);
