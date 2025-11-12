import django_filters
from .models import Birth, Social, Education, TotalInfo, Company


class BirthFilter(django_filters.FilterSet):

    min_age = django_filters.NumberFilter(field_name="age", lookup_expr="gte")
    max_age = django_filters.NumberFilter(field_name="age", lookup_expr="lte")

    religion = django_filters.CharFilter(field_name="religion", lookup_expr="icontains")

    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    anon_id = django_filters.UUIDFilter(field_name="anon_id", lookup_expr="exact")

    class Meta:
        model = Birth
        fields = ["age", "religion", "date", "owner", "name"]


class SocialFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="exact")

    class Meta:
        model = Social
        fields = ["name", "email"]


class EducationFilter(django_filters.FilterSet):
    school = django_filters.CharFilter(field_name="school", lookup_expr="exact")
    class_number = django_filters.NumberFilter(
        field_name="class_number", lookup_expr="exact"
    )
    min_class_number = django_filters.NumberFilter(
        field_name="class_number", lookup_expr="gte"
    )
    max_class_number = django_filters.NumberFilter(
        field_name="class_number", lookup_expr="lte"
    )

    class Meta:
        model = Education
        fields = ["school", "class_number"]


class TotalInfoFilterSet(django_filters.FilterSet):
    owner = django_filters.CharFilter(
        field_name="owner__username", lookup_expr="icontains"
    )
    school = django_filters.CharFilter(
        field_name="education__school", lookup_expr="icontains"
    )
    name = django_filters.CharFilter(field_name="birth__name", lookup_expr="icontains")
    social_email = django_filters.CharFilter(
        field_name="social__email", lookup_expr="icontains"
    )

    anon_id = django_filters.UUIDFilter(
        field_name="birth__anon_id", lookup_expr="exact"
    )

    class Meta:
        model = TotalInfo
        fields = ["owner", "name", "school", "social_email", "anon_id"]


class CompanyFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Search by company name"
    )

    total_workers_min = django_filters.NumberFilter(field_name="total_workers", lookup_expr='gte')
    total_workers_max = django_filters.NumberFilter(field_name="total_workers", lookup_expr='lte')

    address = django_filters.CharFilter(field_name="address", lookup_expr="icontains")

    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")

    joined_after = django_filters.DateFilter(field_name="join", lookup_expr="gte")
    joined_before = django_filters.DateFilter(field_name="join", lookup_expr="lte")

    website = django_filters.CharFilter(field_name="website", lookup_expr="icontains")

    class Meta:
        model = Company
        fields = ["name", "total_workers", "address", "status", "website", "join"]
