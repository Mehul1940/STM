from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django import forms


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.full_name or self.user.username

class Room(models.Model):
    BLOCK_CHOICES = [
        ('A', 'Block A'),
        ('B', 'Block B'),
        ('C', 'Block C'),
        ('D', 'Block D'),
    ]

    ROOM_TYPES = [
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
        ('4BHK', '4BHK'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    ]

    block = models.CharField(max_length=1, choices=BLOCK_CHOICES)
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    resident = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="room")
    
    occupied_since = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.block} - {self.room_number} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if self.status == 'available':
            self.resident = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['block', 'room_number']
        constraints = [
            models.UniqueConstraint(fields=['block', 'room_number'], name='unique_block_room')
        ]




class Notice(models.Model):
    NOTICE_TYPES = [
        ('general', 'General'),
        ('maintenance', 'Maintenance'),
        ('event', 'Event'),
        ('security', 'Security'),
    ]

    title = models.CharField(max_length=255) 
    description = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES, default='general') 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateField(null=True, blank=True) 
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"{self.notice_type} - {self.title}"

    class Meta:
        ordering = ['-created_at']


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    total_fund_needed = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fund_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def fund_remaining(self):
        return max(0, self.total_fund_needed - self.total_fund_collected)
    

class Contribution(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributions")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="contributions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    screenshot = models.ImageField(upload_to="payment_proofs/")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing')
    contributed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ₹{self.amount} for {self.event.name} ({self.status})"
    

class Visitor(models.Model):
    VISITOR_TYPE_CHOICES = [
        ('guest', 'Guest'),
        ('delivery', 'Delivery Person'),
        ('service', 'Service Provider'),
        ('other', 'Other'),
    ]

    VEHICLE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('on_foot', 'On Foot'),
    ]

    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    visitor_type = models.CharField(max_length=20, choices=VISITOR_TYPE_CHOICES)
    visiting_flat = models.ForeignKey(Room, on_delete=models.CASCADE)
    purpose = models.TextField()

    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)
    vehicle_number = models.CharField(max_length=20, null=True, blank=True)

    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.vehicle_type == 'on_foot':
            self.vehicle_number = None 
        super().save(*args, **kwargs)

    def check_out(self):
        self.check_out_time = datetime.now()
        self.save()    



class Income(models.Model):
    INCOME_CATEGORIES = [
        ('maintenance', 'Maintenance Payment'),
        ('event', 'Event Fee'),
        ('facility', 'Facility Booking'),
        ('other', 'Other'),
    ]

    category = models.CharField(max_length=20, choices=INCOME_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    received_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_received = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.get_category_display()} - ₹{self.amount} on {self.date_received}"


class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('maintenance', 'Maintenance Costs'),
        ('salary', 'Staff Salaries'),
        ('utilities', 'Utility Bills'),
        ('repairs', 'Repairs & Renovation'),
        ('other', 'Other'),
    ]

    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_to = models.CharField(max_length=255)  # Who received the payment
    description = models.TextField(null=True, blank=True)
    date_paid = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.get_category_display()} - ₹{self.amount} on {self.date_paid}"
    

class Facility(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="facilities/", blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price per day

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    start_date = models.DateField() 
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_proof = models.ImageField(upload_to="payments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.facility.name} ({self.start_date} to {self.end_date})"


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('security', 'Security'),
        ('billing', 'Billing'),
        ('noise', 'Noise Disturbance'),
        ('other', 'Other'),
    ]

    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Link to Room table
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    admin_remarks = models.TextField(null=True, blank=True) 

    def resolve(self, remarks=""):
        self.status = 'resolved'
        self.resolved_at = datetime.now()
        self.admin_remarks = remarks
        self.save()

    def __str__(self):
        return f"{self.resident.username} - {self.room.room_number} - {self.category} - {self.status}"
    

class MaintenancePayment(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    year = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resident', 'month', 'year')
    def __str__(self):
        return f"{self.resident.username} - {self.get_month_display()} {self.year} - {'Paid' if self.is_paid else 'Pending'}"
    


class Maintenance(models.Model):
    MONTH_CHOICES = [
        (1, "January"), (2, "February"), (3, "March"), (4, "April"),
        (5, "May"), (6, "June"), (7, "July"), (8, "August"),
        (9, "September"), (10, "October"), (11, "November"), (12, "December"),
    ]

    STATUS = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maintenance_payments")
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField(default=date.today().year)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10,choices=STATUS, default="pending")
    payment_proof = models.ImageField(upload_to="maintenance_payments/", blank=True, null=True)
    date_paid = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "month", "year") 
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"{self.user.username} - {self.get_month_display()} {self.year} - ₹{self.amount} ({self.status})"


class MaintenanceForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Maintenance Amount", min_value=0
    )