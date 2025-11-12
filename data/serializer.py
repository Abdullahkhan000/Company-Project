from rest_framework import serializers
from .models import Social, Birth, Education, TotalInfo, Company
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError


class BaseSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class BirthSerializer(serializers.Serializer):
    name_id = serializers.IntegerField(source="id", read_only=True)
    slug = serializers.SlugField(max_length=255, required=False, allow_blank=True)
    name = serializers.CharField(max_length=20, default="name", allow_blank=True)
    anon_id = serializers.UUIDField(allow_null=True, required=False)
    age = serializers.IntegerField()
    religion = serializers.CharField(
        help_text="Enter your religion info and where you were born",
        default="Unknown",
        required=False,
        allow_blank=True,
    )
    date = serializers.DateField()

    def validate_age(self, value):

        if not isinstance(value, int):
            raise serializers.ValidationError("Value must be an integer")

        if value < 0:
            raise serializers.ValidationError("Age must be positive")

        return value

    def validate_religion(self, value):
        if not value or value.strip() == "":
            return "Unknown"
        return value

    def create(self, validated_data):
        if (
            not validated_data.get("religion")
            or validated_data["religion"].strip() == ""
        ):
            validated_data["religion"] = "Unknown"
        return Birth.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)

        religion = validated_data.get("religion", instance.religion)
        if not religion or religion.strip() == "":
            religion = "Unknown"
        instance.religion = religion

        instance.date = validated_data.get("date", instance.date)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.anon_id = validated_data.get("anon_id", instance.anon_id)
        instance.save()
        return instance


class SocialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    name = BirthSerializer()
    email = serializers.EmailField()
    accounts = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False)

    def create(self, validated_data):
        # pull nested Birth data
        birth_data = validated_data.pop("name")

        # create or get Birth
        birth_obj, _ = Birth.objects.get_or_create(**birth_data)

        # create Social linked to Birth
        social = Social.objects.create(name=birth_obj, **validated_data)
        return social

    # def update(self, instance, validated_data):
    #     birth_data = validated_data.pop("name", None)
    #     if birth_data:
    #         Birth.objects.filter(pk=instance.name.pk).update(**birth_data)
    #
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        """
        Update an existing Social instance and its nested Birth relationship.

        Args:
            instance (Social): The Social instance to update
            validated_data (dict): Validated field data including nested Birth

        Returns:
            Social: Updated Social object
        """
        # --- Nested Birth update ---
        if "name" in validated_data:
            birth_data = validated_data.pop("name")
            birth_serializer = BirthSerializer(
                instance=instance.name, data=birth_data, partial=True
            )
            birth_serializer.is_valid(raise_exception=True)
            birth_serializer.save()

        instance.email = validated_data.get("email", instance.email)
        instance.accounts = validated_data.get("accounts", instance.accounts)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.image = validated_data.get("image", instance.image)

        instance.save()
        return instance


# EducationSerializer Without BirthData

# class EducationSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     birth = serializers.PrimaryKeyRelatedField(queryset=Birth.objects.all())
#     school = serializers.CharField(
#         max_length=255, help_text="Enter Info About Your School"
#     )
#     class_number = serializers.IntegerField(help_text="Enter The Info About Your Class")
#
#     def create(self, validated_data):
#         birth = validated_data.get("birth")
#         school = validated_data.get("school")
#         class_number = validated_data.get("class_number")
#
#         user = self.context["request"].user if "request" in self.context else None
#
#         return Education.objects.create(
#             owner=user, birth=birth, school=school, class_number=class_number
#         )
#
#     def update(self, instance, validated_data):
#         """
#         Update an existing Education record.
#         """
#         instance.birth = validated_data.get("birth", instance.birth)
#         instance.school = validated_data.get("school", instance.school)
#         instance.class_number = validated_data.get(
#             "class_number", instance.class_number
#         )
#
#         instance.save()
#         return instance

# Education Serializer With BirthData


class EducationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    birth = BirthSerializer(read_only=True)
    birth_id = serializers.PrimaryKeyRelatedField(
        queryset=Birth.objects.all(), write_only=True
    )
    school = serializers.CharField(max_length=255)
    class_number = serializers.IntegerField()

    def create(self, validated_data):
        birth = validated_data.get("birth_id")
        school = validated_data.get("school")
        class_number = validated_data.get("class_number")
        user = self.context["request"].user if "request" in self.context else None

        return Education.objects.create(
            owner=user,
            birth=birth,
            school=school,
            class_number=class_number,
        )

    def update(self, instance, validated_data):
        instance.birth = validated_data.get("birth_id", instance.birth)
        instance.school = validated_data.get("school", instance.school)
        instance.class_number = validated_data.get(
            "class_number", instance.class_number
        )
        instance.save()
        return instance


class TotalInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")
    social = SocialSerializer(read_only=True)
    birth = BirthSerializer(read_only=True)
    education = EducationSerializer(read_only=True)


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    employee = serializers.StringRelatedField()

    name = serializers.CharField(max_length=255)
    total_workers = serializers.IntegerField()
    address = serializers.CharField()
    status = serializers.CharField()
    join = serializers.DateField()
    logo = serializers.ImageField(required=False, allow_null=True)
    website = serializers.URLField(required=False, allow_null=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.total_workers = validated_data.get(
            "total_workers", instance.total_workers
        )
        instance.address = validated_data.get("address", instance.address)
        instance.status = validated_data.get("status", instance.status)
        instance.join = validated_data.get("join", instance.join)
        instance.logo = validated_data.get("logo", instance.logo)
        instance.website = validated_data.get("website", instance.website)

        instance.save()
        return instance
