from django.contrib import admin

from .models import (
    DataSource,
    ImportBatch,
    Provider,
    ProviderAddress,
    ProviderTaxonomy,
    TaxonomyCode,
)


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ("source_name", "source_type", "source_url", "created_at")
    search_fields = ("source_name", "source_type", "source_url")
    list_filter = ("source_type",)
    ordering = ("source_name",)


@admin.register(ImportBatch)
class ImportBatchAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "data_source",
        "source_version",
        "status",
        "import_started_at",
        "import_completed_at",
    )
    search_fields = ("file_name", "source_version", "status")
    list_filter = ("status", "data_source")
    ordering = ("-import_started_at",)


class ProviderAddressInline(admin.TabularInline):
    model = ProviderAddress
    extra = 0
    fields = (
        "address_type",
        "city",
        "state",
        "zip_code",
        "country_code",
        "telephone_number",
    )


class ProviderTaxonomyInline(admin.TabularInline):
    model = ProviderTaxonomy
    extra = 0
    fields = (
        "taxonomy_code",
        "is_primary",
        "license_number",
        "license_state",
    )
    autocomplete_fields = ("taxonomy_code",)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = (
        "npi",
        "display_name",
        "entity_type_code",
        "provider_credential",
        "updated_at",
    )
    search_fields = (
        "npi",
        "provider_first_name",
        "provider_last_name",
        "organization_name",
    )
    list_filter = ("entity_type_code",)
    ordering = ("provider_last_name", "provider_first_name", "organization_name")
    inlines = (ProviderAddressInline, ProviderTaxonomyInline)

    @admin.display(description="Provider Name")
    def display_name(self, obj):
        return str(obj)


@admin.register(ProviderAddress)
class ProviderAddressAdmin(admin.ModelAdmin):
    list_display = (
        "provider",
        "address_type",
        "city",
        "state",
        "zip_code",
        "telephone_number",
    )
    search_fields = (
        "provider__npi",
        "provider__provider_first_name",
        "provider__provider_last_name",
        "provider__organization_name",
        "city",
        "state",
        "zip_code",
    )
    list_filter = ("address_type", "state")
    ordering = ("state", "city", "zip_code")


@admin.register(TaxonomyCode)
class TaxonomyCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "taxonomy_description",
        "grouping",
        "classification",
        "source_version",
    )
    search_fields = (
        "code",
        "taxonomy_description",
        "grouping",
        "classification",
        "specialization",
    )
    list_filter = ("grouping", "classification")
    ordering = ("taxonomy_description",)


@admin.register(ProviderTaxonomy)
class ProviderTaxonomyAdmin(admin.ModelAdmin):
    list_display = (
        "provider",
        "taxonomy_code",
        "is_primary",
        "license_state",
    )
    search_fields = (
        "provider__npi",
        "provider__provider_first_name",
        "provider__provider_last_name",
        "provider__organization_name",
        "taxonomy_code__code",
        "taxonomy_code__taxonomy_description",
    )
    list_filter = ("is_primary", "license_state")
    autocomplete_fields = ("provider", "taxonomy_code")
    ordering = ("provider", "taxonomy_code")

admin.site.site_header = "EMRTS Provider Lookup Administration"
admin.site.site_title = "Provider Lookup Admin"
admin.site.index_title = "Provider Data Management"
