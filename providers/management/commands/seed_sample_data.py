from django.core.management.base import BaseCommand
from django.utils import timezone

from providers.models import (
    DataSource,
    ImportBatch,
    Provider,
    ProviderAddress,
    ProviderTaxonomy,
    TaxonomyCode,
)


class Command(BaseCommand):
    help = "Create sample provider lookup data for local development."

    def handle(self, *args, **options):
        nppes_source, _ = DataSource.objects.get_or_create(
            source_name="CMS NPPES Downloadable Data Files",
            defaults={
                "source_type": "provider_data",
                "source_url": "https://download.cms.gov/nppes/NPI_Files.html",
                "description": "Public downloadable provider data files from CMS NPPES.",
            },
        )

        nucc_source, _ = DataSource.objects.get_or_create(
            source_name="NUCC Health Care Provider Taxonomy Code Set",
            defaults={
                "source_type": "taxonomy_data",
                "source_url": "https://www.nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40",
                "description": "Public health care provider taxonomy code set from NUCC.",
            },
        )

        ImportBatch.objects.get_or_create(
            data_source=nppes_source,
            file_name="sample-nppes-provider-data.csv",
            defaults={
                "source_version": "sample",
                "import_started_at": timezone.now(),
                "import_completed_at": timezone.now(),
                "status": "completed",
                "notes": "Sample local development import record.",
            },
        )

        taxonomy_data = [
            {
                "code": "207Q00000X",
                "taxonomy_description": "Family Medicine",
                "grouping": "Allopathic & Osteopathic Physicians",
                "classification": "Family Medicine",
            },
            {
                "code": "208D00000X",
                "taxonomy_description": "General Practice",
                "grouping": "Allopathic & Osteopathic Physicians",
                "classification": "General Practice",
            },
            {
                "code": "363A00000X",
                "taxonomy_description": "Physician Assistant",
                "grouping": "Physician Assistants & Advanced Practice Nursing Providers",
                "classification": "Physician Assistant",
            },
        ]

        taxonomy_lookup = {}
        for item in taxonomy_data:
            taxonomy, _ = TaxonomyCode.objects.update_or_create(
                code=item["code"],
                defaults={
                    "taxonomy_description": item["taxonomy_description"],
                    "grouping": item["grouping"],
                    "classification": item["classification"],
                    "source_version": "sample",
                },
            )
            taxonomy_lookup[item["taxonomy_description"]] = taxonomy

        provider_data = [
            {
                "npi": "1003000001",
                "entity_type_code": "1",
                "provider_first_name": "Emily",
                "provider_last_name": "Carter",
                "provider_credential": "MD",
                "organization_name": "",
                "taxonomy": "Family Medicine",
                "city": "Durham",
                "state": "NC",
                "zip_code": "27708",
                "telephone_number": "919-555-0101",
            },
            {
                "npi": "1003000002",
                "entity_type_code": "1",
                "provider_first_name": "Daniel",
                "provider_last_name": "Lee",
                "provider_credential": "DO",
                "organization_name": "",
                "taxonomy": "General Practice",
                "city": "Raleigh",
                "state": "NC",
                "zip_code": "27601",
                "telephone_number": "919-555-0102",
            },
            {
                "npi": "1003000003",
                "entity_type_code": "2",
                "provider_first_name": "",
                "provider_last_name": "",
                "provider_credential": "",
                "organization_name": "Triangle Community Health Center",
                "taxonomy": "Family Medicine",
                "city": "Cary",
                "state": "NC",
                "zip_code": "27513",
                "telephone_number": "919-555-0103",
            },
            {
                "npi": "1003000004",
                "entity_type_code": "1",
                "provider_first_name": "Sarah",
                "provider_last_name": "Nguyen",
                "provider_credential": "PA",
                "organization_name": "",
                "taxonomy": "Physician Assistant",
                "city": "Durham",
                "state": "NC",
                "zip_code": "27701",
                "telephone_number": "919-555-0104",
            },
        ]

        for item in provider_data:
            provider, _ = Provider.objects.update_or_create(
                npi=item["npi"],
                defaults={
                    "entity_type_code": item["entity_type_code"],
                    "provider_first_name": item["provider_first_name"] or None,
                    "provider_last_name": item["provider_last_name"] or None,
                    "provider_credential": item["provider_credential"] or None,
                    "organization_name": item["organization_name"] or None,
                },
            )

            ProviderAddress.objects.update_or_create(
                provider=provider,
                address_type="practice",
                defaults={
                    "city": item["city"],
                    "state": item["state"],
                    "zip_code": item["zip_code"],
                    "country_code": "US",
                    "telephone_number": item["telephone_number"],
                },
            )

            ProviderTaxonomy.objects.update_or_create(
                provider=provider,
                taxonomy_code=taxonomy_lookup[item["taxonomy"]],
                license_number="",
                license_state=item["state"],
                defaults={
                    "is_primary": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Sample provider data created successfully."))
        self.stdout.write(f"Providers: {Provider.objects.count()}")
        self.stdout.write(f"Addresses: {ProviderAddress.objects.count()}")
        self.stdout.write(f"Taxonomy codes: {TaxonomyCode.objects.count()}")
