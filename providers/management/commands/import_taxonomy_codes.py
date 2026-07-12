import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from providers.models import TaxonomyCode


class Command(BaseCommand):
    help = "Import NUCC taxonomy code data from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            type=str,
            help="Path to the NUCC taxonomy CSV file.",
        )
        parser.add_argument(
            "--source-version",
            type=str,
            default="manual-import",
            help="Optional source version label for the imported taxonomy records.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])

        if not csv_path.exists():
            raise CommandError(f"CSV file not found: {csv_path}")

        created_count = 0
        updated_count = 0
        skipped_count = 0

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

            for row in reader:
                code = get_value(row, ["code", "taxonomy code", "taxonomy_code"])
                description = get_value(
                    row,
                    [
                        "display name",
                        "display_name",
                        "taxonomy description",
                        "taxonomy_description",
                        "classification",
                    ],
                )

                if not code or not description:
                    skipped_count += 1
                    continue

                _, created = TaxonomyCode.objects.update_or_create(
                    code=code,
                    defaults={
                        "taxonomy_description": description,
                        "grouping": get_value(row, ["grouping", "group"]),
                        "classification": get_value(row, ["classification"]),
                        "specialization": get_value(row, ["specialization"]),
                        "definition": get_value(row, ["definition", "notes"]),
                        "source_version": options["source_version"],
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS("NUCC taxonomy import completed."))
        self.stdout.write(f"Created: {created_count}")
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped: {skipped_count}")
        self.stdout.write(f"Total taxonomy codes: {TaxonomyCode.objects.count()}")
