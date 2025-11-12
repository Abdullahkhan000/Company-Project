from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils.text import slugify

# from django.core.exceptions import ValidationError


# Base model for timestamps
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # auto on create
    updated_at = models.DateTimeField(auto_now=True)  # auto on update
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Birth(BaseModel):

    slug = models.SlugField(max_length=255, unique_for_date="date", blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="births", null=True
    )
    name = models.CharField(max_length=20, default="name", blank=True)
    anon_id = models.UUIDField(null=True, blank=False)
    age = models.IntegerField()
    religion = models.TextField(
        help_text="Enter your religion info and where you were born",
        default="Unknown",
        blank=True,
    )
    date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.age < 0:
    #         raise ValidationError("Age cannot be negative.")


class Social(BaseModel):
    name = models.ForeignKey(
        Birth, on_delete=models.CASCADE, related_name="social_accounts"
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        help_text="Enter a valid email address",
    )

    accounts = models.TextField(
        help_text="Save multiple account links (e.g., Instagram, LinkedIn, Twitter). Separate them with commas."
    )

    phone = PhoneNumberField(
        blank=True, help_text="Enter phone number with country code (e.g., +92...)"
    )

    def __str__(self):
        return f"{self.name} - {self.email}"

    image = models.ImageField(upload_to="images/", blank=True)


class Education(BaseModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="educations", null=True
    )
    birth = models.ForeignKey(
        Birth, on_delete=models.CASCADE, related_name="education_records"
    )
    school = models.CharField(max_length=255, help_text="Enter Info About Your School")
    class_number = models.IntegerField(help_text="Enter The Info About Your Class")


class TotalInfo(BaseModel):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="main_user", null=True
    )
    social = models.ForeignKey(
        Social, on_delete=models.CASCADE, related_name="main_social"
    )
    birth = models.ForeignKey(
        Birth, on_delete=models.CASCADE, related_name="main_birth"
    )
    education = models.ForeignKey(
        Education, on_delete=models.CASCADE, related_name="main_education"
    )

    def __str__(self):
        return f"TotalInfo for {self.owner.username if self.owner else 'Unknown'}"


class Company(BaseModel):
    employee = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="company", null=True, blank=True
    )
    name = models.CharField(
        help_text="Enter the name of your current working company", max_length=255
    )
    total_workers = models.IntegerField(
        help_text="Total number of employees working"
    )
    address = models.TextField(help_text="Your company address")

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("on_leave", "On Leave"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    join = models.DateField(help_text="Enter your joining date")

    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        employee_name = self.employee if self.employee else "No Employee Assigned"
        return f"Company: {self.name} | Employee: {employee_name}"
