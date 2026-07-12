from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.test import TestCase

from .models import (
    ImportBatch,
    Provider,
    ProviderAddress,
    ProviderTaxonomy,
    TaxonomyCode,
)


class ProviderLookupViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        taxonomy = TaxonomyCode.objects.create(
            code="207Q00000X",
            taxonomy_description="Family Medicine",
            grouping="Allopathic & Osteopathic Physicians",
            classification="Family Medicine",
        )

        provider = Provider.objects.create(
            npi="1003000001",
            entity_type_code="1",
            provider_first_name="Emily",
            provider_last_name="Carter",
            provider_credential="MD",
        )

        ProviderAddress.objects.create(
            provider=provider,
            address_type="practice",
            city="Durham",
            state="NC",
            zip_code="27708",
            telephone_number="919-555-0101",
        )

        ProviderTaxonomy.objects.create(
            provider=provider,
            taxonomy_code=taxonomy,
            is_primary=True,
            license_state="NC",
        )

    def test_home_page_loads_without_search_results(self):
        response = self.client.get("/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Provider Search", html)
        self.assertIn("Ready to search", html)
        self.assertIn("Taxonomy Description", html)
        self.assertNotIn("NPI Number", html)
        self.assertNotIn("NPI Type", html)
        self.assertNotIn("Emily Carter", html)

    def test_city_search_returns_matching_provider(self):
        response = self.client.get("/?city=Durham")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Emily Carter", html)
        self.assertIn("Family Medicine", html)

    def test_exact_match_blocks_partial_first_name(self):
        response = self.client.get("/?provider_first_name=Em&exact_match=on")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Emily Carter", html)

    def test_exact_match_allows_full_first_name(self):
        response = self.client.get("/?provider_first_name=Emily&exact_match=on")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Emily Carter", html)

    def test_provider_detail_page_loads(self):
        response = self.client.get("/providers/1003000001/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Provider Information", html)
        self.assertIn("NPI Number", html)
        self.assertIn("Family Medicine", html)


class ImportCommandTests(TestCase):
    def test_import_taxonomy_codes_command(self):
        with TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "taxonomy.csv"
            csv_path.write_text(
                "Code,Grouping,Classification,Specialization,Definition,Display Name\n"
                "390200000X,Student,Student in Training,,Student training provider,Student in an Organized Health Care Education/Training Program\n",
                encoding="utf-8",
            )

            output = StringIO()
            call_command(
                "import_taxonomy_codes",
                str(csv_path),
                "--source-version",
                "test-taxonomy",
                stdout=output,
            )

        taxonomy = TaxonomyCode.objects.get(code="390200000X")
        self.assertEqual(taxonomy.source_version, "test-taxonomy")
        self.assertIn("NUCC taxonomy import completed", output.getvalue())

    def test_import_nppes_providers_command(self):
        with TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "nppes.csv"
            csv_path.write_text(
                "npi,entity type code,provider first name,provider last name (legal name),"
                "provider credential text,provider organization name (legal business name),"
                "provider first line business practice location address,"
                "provider business practice location address city name,"
                "provider business practice location address state name,"
                "provider business practice location address postal code,"
                "provider business practice location address telephone number,"
                "healthcare provider taxonomy code_1,taxonomy description_1,"
                "healthcare provider primary taxonomy switch_1,"
                "provider license number_1,provider license number state code_1\n"
                "1003000099,1,Michael,Roberts,MD,,100 Medical Plaza,Durham,NC,27705,"
                "919-555-0199,208000000X,Pediatrics,Y,NC-1099,NC\n",
                encoding="utf-8",
            )

            output = StringIO()
            call_command(
                "import_nppes_providers",
                str(csv_path),
                "--source-version",
                "test-nppes",
                stdout=output,
            )

        provider = Provider.objects.get(npi="1003000099")
        self.assertEqual(provider.provider_first_name, "Michael")
        self.assertTrue(provider.addresses.filter(city="Durham").exists())
        self.assertTrue(
            provider.provider_taxonomies.filter(
                taxonomy_code__code="208000000X"
            ).exists()
        )
        self.assertEqual(ImportBatch.objects.latest("id").status, "completed")
        self.assertIn("NPPES provider import completed", output.getvalue())
