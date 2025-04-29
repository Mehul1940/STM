from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RoomForm(forms.ModelForm):
    resident = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False, is_staff=False),
        required=False,
        empty_label="Select a Resident",
        help_text="Assign a resident to this room."
    )

    class Meta:
        model = Room
        fields = ['block', 'room_number', 'room_type', 'status', 'resident']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = "__all__"
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'event_date', 'image', 'total_fund_needed']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'contact_number', 'visitor_type', 'visiting_flat', 'purpose', 'vehicle_type', 'vehicle_number']


class CustomUserForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label="Full Name")
    contact_number = forms.CharField(max_length=15, required=True, label="Contact Number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'full_name', 'contact_number', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = "" 

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.update_or_create(user=user, defaults={
                "full_name": self.cleaned_data['full_name'],
                "contact_number": self.cleaned_data['contact_number']
            })
        return user

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['amount', 'screenshot']


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ["facility", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['room', 'category', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your issue...'}),
        }


class ComplaintResolutionForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['admin_remarks']
        widgets = {
            'admin_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your remarks...'}),
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'amount', 'received_from', 'description', 'date_received']
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'paid_to', 'description', 'date_paid']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'


class BookingApprovalForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }

class ContributionApprovalForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class MaintenanceApprovalForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ["status"]
        widgets = {
            "status": forms.Select(choices=[
                ("pending", "Pending"),
                ("verified", "Verified"),
                ("rejected", "Rejected"),
            ], attrs={"class": "form-select"}),
        }
