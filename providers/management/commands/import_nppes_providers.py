import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
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
    help = "Import provider records from a CMS NPPES-style CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            type=str,
            help="Path to the CMS NPPES provider CSV file.",
        )
        parser.add_argument(
            "--source-version",
            type=str,
            default="manual-import",
            help="Optional source version label for the imported provider records.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Optional maximum number of rows to import. Use 0 for all rows.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])

        if not csv_path.exists():
            raise CommandError(f"CSV file not found: {csv_path}")

        source, _ = DataSource.objects.get_or_create(
            source_name="CMS NPPES Downloadable Data Files",
            defaults={
                "source_type": "provider_data",
                "source_url": "https://download.cms.gov/nppes/NPI_Files.html",
                "description": "Public downloadable provider data files from CMS NPPES.",
            },
        )

        batch = ImportBatch.objects.create(
            data_source=source,
            file_name=csv_path.name,
            source_version=options["source_version"],
            import_started_at=timezone.now(),
            status="running",
            notes="Provider CSV import started.",
        )

        created_count = 0
        updated_count = 0
        skipped_count = 0
        address_count = 0
        taxonomy_count = 0

        try:
            with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
                reader = csv.DictReader(file)

                if not reader.fieldnames:
                    raise CommandError("CSV file does not contain a header row.")

                normalized_fields = {
                    field.lower().strip(): field
                    for field in reader.fieldnames
                    if field
                }

                def get_value(row, possible_names):
                    for name in possible_names:
                        field = normalized_fields.get(name.lower())
                        if field:
                            return (row.get(field) or "").strip()
                    return ""

                for row_number, row in enumerate(reader, start=1):
                    if options["limit"] and row_number > options["limit"]:
                        break

                    npi = get_value(row, ["npi", "NPI"])
                    entity_type_code = get_value(row, ["entity type code", "entity_type_code"])

                    if not npi or not entity_type_code:
                        skipped_count += 1
                        continue

                    provider, created = Provider.objects.update_or_create(
                        npi=npi,
                        defaults={
                            "entity_type_code": entity_type_code,
                            "provider_first_name": get_value(
                                row,
                                [
                                    "provider first name",
                                    "provider_first_name",
                                    "Provider First Name",
                                ],
                            ) or None,
                            "provider_last_name": get_value(
                                row,
                                [
                                    "provider last name",
                                    "provider last name (legal name)",
                                    "provider_last_name",
                                    "Provider Last Name (Legal Name)",
                                ],
                            ) or None,
                            "provider_middle_name": get_value(
                                row,
                                [
                                    "provider middle name",
                                    "provider_middle_name",
                                    "Provider Middle Name",
                                ],
                            ) or None,
                            "provider_credential": get_value(
                                row,
                                [
                                    "provider credential text",
                                    "provider credential",
                                    "provider_credential",
                                    "Provider Credential Text",
                                ],
                            ) or None,
                            "organization_name": get_value(
                                row,
                                [
                                    "provider organization name (legal business name)",
                                    "organization name",
                                    "organization_name",
                                    "Provider Organization Name (Legal Business Name)",
                                ],
                            ) or None,
                            "enumeration_date": None,
                            "last_update_date": None,
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                    city = get_value(
                        row,
                        [
                            "provider business practice location address city name",
                            "city",
                            "practice_city",
                        ],
                    )
                    state = get_value(
                        row,
                        [
                            "provider business practice location address state name",
                            "state",
                            "practice_state",
                        ],
                    )
                    zip_code = get_value(
                        row,
                        [
                            "provider business practice location address postal code",
                            "zip code",
                            "zip_code",
                            "postal code",
                            "practice_zip",
                        ],
                    )

                    if city and state and zip_code:
                        ProviderAddress.objects.update_or_create(
                            provider=provider,
                            address_type="practice",
                            defaults={
                                "address_line_1": get_value(
                                    row,
                                    [
                                        "provider first line business practice location address",
                                        "address_line_1",
                                        "practice_address_1",
                                    ],
                                ) or None,
                                "address_line_2": get_value(
                                    row,
                                    [
                                        "provider second line business practice location address",
                                        "address_line_2",
                                        "practice_address_2",
                                    ],
                                ) or None,
                                "city": city,
                                "state": state,
                                "zip_code": zip_code,
                                "country_code": get_value(
                                    row,
                                    [
                                        "provider business practice location address country code (if outside u.s.)",
                                        "country_code",
                                    ],
                                ) or None,
                                "telephone_number": get_value(
                                    row,
                                    [
                                        "provider business practice location address telephone number",
                                        "telephone_number",
                                        "phone",
                                    ],
                                ) or None,
                            },
                        )
                        address_count += 1

                    for index in range(1, 16):
                        taxonomy_code_value = get_value(
                            row,
                            [
                                f"healthcare provider taxonomy code_{index}",
                                f"taxonomy_code_{index}",
                                "taxonomy code",
                                "taxonomy_code",
                            ],
                        )

                        if not taxonomy_code_value:
                            continue

                        taxonomy_description = get_value(
                            row,
                            [
                                f"taxonomy description_{index}",
                                "taxonomy description",
                                "taxonomy_description",
                            ],
                        )

                        taxonomy, _ = TaxonomyCode.objects.get_or_create(
                            code=taxonomy_code_value,
                            defaults={
                                "taxonomy_description": taxonomy_description or taxonomy_code_value,
                                "source_version": "created-during-provider-import",
                            },
                        )

                        primary_switch = get_value(
                            row,
                            [
                                f"healthcare provider primary taxonomy switch_{index}",
                                f"primary_taxonomy_switch_{index}",
                                "primary taxonomy switch",
                            ],
                        ).upper()

                        ProviderTaxonomy.objects.update_or_create(
                            provider=provider,
                            taxonomy_code=taxonomy,
                            license_number=get_value(
                                row,
                                [
                                    f"provider license number_{index}",
                                    f"license_number_{index}",
                                    "license_number",
                                ],
                            ) or "",
                            license_state=get_value(
                                row,
                                [
                                    f"provider license number state code_{index}",
                                    f"license_state_{index}",
                                    "license_state",
                                ],
                            ) or "",
                            defaults={
                                "is_primary": primary_switch in {"Y", "YES", "TRUE", "1"},
                            },
                        )
                        taxonomy_count += 1

            batch.status = "completed"
            batch.import_completed_at = timezone.now()
            batch.notes = "Provider CSV import completed successfully."
            batch.save(update_fields=["status", "import_completed_at", "notes"])

        except Exception as exc:
            batch.status = "failed"
            batch.import_completed_at = timezone.now()
            batch.notes = str(exc)
            batch.save(update_fields=["status", "import_completed_at", "notes"])
            raise

        self.stdout.write(self.style.SUCCESS("NPPES provider import completed."))
        self.stdout.write(f"Created providers: {created_count}")
        self.stdout.write(f"Updated providers: {updated_count}")
        self.stdout.write(f"Addresses processed: {address_count}")
        self.stdout.write(f"Taxonomy links processed: {taxonomy_count}")
        self.stdout.write(f"Skipped rows: {skipped_count}")
