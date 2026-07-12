from django.db import models


class DataSource(models.Model):
    source_name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=100)
    source_url = models.TextField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "data_sources"

    def __str__(self):
        return self.source_name


class ImportBatch(models.Model):
    data_source = models.ForeignKey(
        DataSource,
        on_delete=models.PROTECT,
        related_name="import_batches",
        db_index=False,
    )
    file_name = models.CharField(max_length=255)
    source_version = models.CharField(max_length=100, null=True, blank=True)
    import_started_at = models.DateTimeField()
    import_completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "import_batches"
        indexes = [
            models.Index(fields=["data_source"], name="idx_imp_source"),
        ]

    def __str__(self):
        return f"{self.file_name} ({self.status})"


class Provider(models.Model):
    npi = models.CharField(max_length=10, unique=True)
    entity_type_code = models.CharField(max_length=1)
    provider_first_name = models.CharField(max_length=100, null=True, blank=True)
    provider_last_name = models.CharField(max_length=100, null=True, blank=True)
    provider_middle_name = models.CharField(max_length=100, null=True, blank=True)
    provider_credential = models.CharField(max_length=50, null=True, blank=True)
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    enumeration_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "providers"
        indexes = [
            models.Index(fields=["provider_first_name"], name="idx_prov_first_name"),
            models.Index(fields=["provider_last_name"], name="idx_prov_last_name"),
        ]

    def __str__(self):
        if self.organization_name:
            return self.organization_name
        full_name = " ".join(
            part for part in [
                self.provider_first_name,
                self.provider_middle_name,
                self.provider_last_name,
            ]
            if part
        )
        return full_name or self.npi


class ProviderAddress(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="addresses",
        db_index=False,
    )
    address_type = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=255, null=True, blank=True)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    telephone_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "provider_addresses"
        indexes = [
            models.Index(fields=["provider"], name="idx_addr_provider"),
            models.Index(fields=["city"], name="idx_addr_city"),
            models.Index(fields=["state"], name="idx_addr_state"),
            models.Index(fields=["zip_code"], name="idx_addr_zip_code"),
        ]

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"


class TaxonomyCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    taxonomy_description = models.CharField(max_length=255)
    grouping = models.CharField(max_length=255, null=True, blank=True)
    classification = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    definition = models.TextField(null=True, blank=True)
    source_version = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "taxonomy_codes"
        indexes = [
            models.Index(fields=["taxonomy_description"], name="idx_tax_desc"),
        ]

    def __str__(self):
        return f"{self.code} - {self.taxonomy_description}"


class ProviderTaxonomy(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="provider_taxonomies",
        db_index=False,
    )
    taxonomy_code = models.ForeignKey(
        TaxonomyCode,
        on_delete=models.PROTECT,
        related_name="provider_taxonomies",
        db_index=False,
    )
    is_primary = models.BooleanField(default=False)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    license_state = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "provider_taxonomies"
        indexes = [
            models.Index(fields=["provider"], name="idx_pt_provider"),
            models.Index(fields=["taxonomy_code"], name="idx_pt_taxonomy"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "taxonomy_code", "license_number", "license_state"],
                name="uq_provider_taxonomy_license",
            )
        ]

    def __str__(self):
        return f"{self.provider} - {self.taxonomy_code}"
