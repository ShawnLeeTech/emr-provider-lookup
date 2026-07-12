from django.shortcuts import render


def home(request):
    """Render the initial provider lookup search page."""
    search_fields = [
        "Taxonomy Description",
        "Provider First Name",
        "Provider Last Name",
        "City",
        "State",
        "Zip Code",
    ]

    context = {
        "search_fields": search_fields,
    }
    return render(request, "providers/home.html", context)
