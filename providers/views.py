from django.shortcuts import get_object_or_404, render

from .models import Provider


SEARCH_FIELDS = [
    "taxonomy_description",
    "provider_first_name",
    "provider_last_name",
    "city",
    "state",
    "zip_code",
]


def home(request):
    """Render provider search page and search results."""
    search_values = {
        field: request.GET.get(field, "").strip()
        for field in SEARCH_FIELDS
    }

    exact_match = request.GET.get("exact_match") == "on"
    has_query = any(search_values.values())

    providers = Provider.objects.none()
    result_count = 0

    if has_query:
        providers = (
            Provider.objects
            .prefetch_related("addresses", "provider_taxonomies__taxonomy_code")
            .order_by("provider_last_name", "provider_first_name", "organization_name")
        )

        if search_values["taxonomy_description"]:
            if exact_match:
                providers = providers.filter(
                    provider_taxonomies__taxonomy_code__taxonomy_description__iexact=search_values["taxonomy_description"]
                )
            else:
                providers = providers.filter(
                    provider_taxonomies__taxonomy_code__taxonomy_description__icontains=search_values["taxonomy_description"]
                )

        if search_values["provider_first_name"]:
            if exact_match:
                providers = providers.filter(
                    provider_first_name__iexact=search_values["provider_first_name"]
                )
            else:
                providers = providers.filter(
                    provider_first_name__icontains=search_values["provider_first_name"]
                )

        if search_values["provider_last_name"]:
            if exact_match:
                providers = providers.filter(
                    provider_last_name__iexact=search_values["provider_last_name"]
                )
            else:
                providers = providers.filter(
                    provider_last_name__icontains=search_values["provider_last_name"]
                )

        if search_values["city"]:
            if exact_match:
                providers = providers.filter(addresses__city__iexact=search_values["city"])
            else:
                providers = providers.filter(addresses__city__icontains=search_values["city"])

        if search_values["state"]:
            providers = providers.filter(addresses__state__iexact=search_values["state"])

        if search_values["zip_code"]:
            if exact_match:
                providers = providers.filter(addresses__zip_code=search_values["zip_code"])
            else:
                providers = providers.filter(addresses__zip_code__startswith=search_values["zip_code"])

        providers = providers.distinct()
        result_count = providers.count()

    context = {
        "search_values": search_values,
        "exact_match": exact_match,
        "has_query": has_query,
        "providers": providers[:20],
        "result_count": result_count,
    }
    return render(request, "providers/home.html", context)


def provider_detail(request, npi):
    """Render a single provider detail page."""
    provider = get_object_or_404(
        Provider.objects.prefetch_related(
            "addresses",
            "provider_taxonomies__taxonomy_code",
        ),
        npi=npi,
    )

    context = {
        "provider": provider,
    }
    return render(request, "providers/provider_detail.html", context)
