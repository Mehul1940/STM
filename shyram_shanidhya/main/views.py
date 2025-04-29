from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import View, ListView , CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.timezone import now

from .models import *
from .forms import *

# Create your views here.


@login_required
def dashboard(request):
    user = request.user

    current_month = datetime.now().month
    current_year = datetime.now().year

    if user.is_superuser:

        context = {
            "visitors": Visitor.objects.filter(check_out_time__isnull=True),
            "total_residents": User.objects.filter(is_staff=False).count(),
            "total_staff": User.objects.filter(is_staff=True).count(),
            "pending_maintenance": Maintenance.objects.filter(status="pending").count(),
            "upcoming_events": Notice.objects.filter().count(),
        }

        return render(request, 'main/admin_dashboard.html', context=context)
    elif user.is_staff:
        context = {
            "visitors": Visitor.objects.filter(check_out_time__isnull=True)
        }
        return render(request, 'main/staff_dashboard.html', context=context)
    else:
        maintenance = Maintenance.objects.filter(
            user=user, month=current_month, year=current_year
        ).first()

        context = {
            "notices": Notice.objects.all(),
            "maintenance": maintenance,
        }

        return render(request, "main/resident/resident_dashboard.html", context)


class AddExtraContextMixin:
    extra_context = {
        
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra"] = self.extra_context
        return context
    


# ROOMS

class RoomListView(AddExtraContextMixin, ListView):
    model = Room
    template_name = "main/list_view.html" 
    paginate_by = 5

    extra_context = {
        "title": "Rooms",
        "headers": ["Room No.", "Block", "Type", "Status", "Resident",],
        "fields": ["room_number", "block", "room_type", "status", "resident"]

    }

class RoomCreateView(AddExtraContextMixin, CreateView):
    model = Room
    template_name = "main/insert_view.html"
    fields = "__all__"
    success_url = reverse_lazy("room_list")

    extra_context = {
        "title": "Room"
    }


class RoomUpdateDeleteView(View):
    template_name = "main/detail_view.html"

    extra_context = {
        "title": "Room"
    }

    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        form = RoomForm(instance=room)
        return render(request, self.template_name, {'form': form, 'room': room, "extra": self.extra_context})

    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)

        if "delete" in request.POST:
            room.delete()
            return redirect("room_list")

        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("room_list")

        return render(request, self.template_name, {'form': form, 'room': room, "extra": self.extra_context})
    


# NOTICE

class NoticeListView(AddExtraContextMixin, ListView):
    model = Notice
    template_name = "main/list_view.html" 
    paginate_by = 5

    extra_context = {
        "title": "Notices",
        "headers": ["Title", "Description", "Notice Type", "Expire Date", "Is Active"],
        "fields": ["title", "description", "notice_type", "expiry_date", "is_active"]

    }

class NoticeCreateView(AddExtraContextMixin, CreateView):
    model = Notice
    template_name = "main/insert_view.html"
    form_class = NoticeForm
    success_url = reverse_lazy("notice_list")

    extra_context = {
        "title": "Notice"
    }


class NoticeUpdateDeleteView(View):
    template_name = "main/detail_view.html"

    extra_context = {
        "title": "Notice"
    }

    def get(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)
        form = NoticeForm(instance=notice)
        return render(request, self.template_name, {'form': form, 'notice': notice, "extra": self.extra_context})

    def post(self, request, pk):
        notice = get_object_or_404(Notice, pk=pk)

        if "delete" in request.POST:
            notice.delete()
            return redirect("notice_list")

        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect("notice_list")

        return render(request, self.template_name, {'form': form, 'notice': notice, "extra": self.extra_context})
    


# EVENTS

class EventListView(AddExtraContextMixin, ListView):
    model = Event
    template_name = "main/list_view.html" 
    paginate_by = 5

    extra_context = {
        "title": "Events",
        "headers": ["Image", "Name", "Description", "Event Date", "Fund Needed", "Fund Collected"],
        "fields": ["image", "name", "description", "event_date", "total_fund_needed", "total_fund_collected"]

    }

class EventCreateView(AddExtraContextMixin, CreateView):
    model = Event
    template_name = "main/insert_view.html"
    form_class = EventForm
    success_url = reverse_lazy("event_list")

    extra_context = {
        "title": "Event"
    }


class EventUpdateDeleteView(View):
    template_name = "main/detail_view.html"

    extra_context = {
        "title": "Event"
    }

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = EventForm(instance=event)
        return render(request, self.template_name, {'form': form, 'event': event, "extra": self.extra_context})

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        if "delete" in request.POST:
            event.delete()
            return redirect("event_list")

        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_list")

        return render(request, self.template_name, {'form': form, 'event': event, "extra": self.extra_context})
    


# USERS
def user_list_view(request):
    users = User.objects.filter(is_superuser=False).select_related("profile").annotate(
        full_name=F("profile__full_name"),
        contact_number=F("profile__contact_number"),
    )

    context = {
        "object_list": users,
        "extra": {
            "title": "Users",
            "headers": ["Username", "Full Name", "Contact Number", "Email", "Is Staff"],
            "fields": ["username", "email", "full_name", "contact_number", "is_staff"],  # No "profile."
        }
    }

    return render(request, "main/list_view.html", context=context)

class UserCreateView(AddExtraContextMixin, CreateView):
    model = User
    template_name = "main/insert_view.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("user_list")

    extra_context = {
        "title": "User"
    }


class UserUpdateDeleteView(View):
    template_name = "main/detail_view.html"

    extra_context = {
        "title": "User"
    }

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(UserProfile, user=user)

        form = CustomUserForm(instance=user, initial={
            "full_name": profile.full_name,
            "contact_number": profile.contact_number
        })
        
        return render(request, self.template_name, {'form': form, 'user': user, "extra": self.extra_context})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(UserProfile, user=user)

        if "delete" in request.POST:
            user.delete()
            return redirect("user_list")

        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.full_name = form.cleaned_data["full_name"]
            profile.contact_number = form.cleaned_data["contact_number"]
            profile.save()
            return redirect("user_list")

        return render(request, self.template_name, {'form': form, 'user': user, "extra": self.extra_context})

# COMPLAINTS

class ComplaintListView(AddExtraContextMixin, ListView):
    model = Complaint
    template_name = "main/list_view.html"
    paginate_by = 10

    extra_context = {
        "title": "Complaints",
        "disable_create": True,
        "headers": ["Resident", "Room", "Category", "Description", "Status"],
        "fields": ["resident", "room", "category", "description", "status"],
    }


def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, id=pk)

    if request.method == "POST":
        form = ComplaintResolutionForm(request.POST, instance=complaint)
        if form.is_valid():
            remark = form.cleaned_data['admin_remarks']
            complaint.resolve(remarks=remark)
            return redirect('complaint_list')
    else:
        form = ComplaintResolutionForm(instance=complaint)

    return render(request, 'main/complaint_detail.html', {'complaint': complaint, 'form': form})



# FINANCE

def finance_overview(request):
    incomes = Income.objects.all().order_by('-date_received')
    expenses = Expense.objects.all().order_by('-date_paid')

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    net_balance = total_income - total_expense

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
    }
    return render(request, 'main/finance_overview.html', context)


class IncomeCreateView(AddExtraContextMixin, CreateView):
    model = Income
    template_name = "main/insert_view.html"
    form_class = IncomeForm
    success_url = reverse_lazy("finance_overview")

    extra_context = {
        "title": "Income"
    }

class ExpenseCreateView(AddExtraContextMixin, CreateView):
    model = Expense
    template_name = "main/insert_view.html"
    form_class = ExpenseForm
    success_url = reverse_lazy("finance_overview")

    extra_context = {
        "title": "Expense"
    }


# FACILITY


class FacilityListView(AddExtraContextMixin, ListView):
    model = Facility
    template_name = "main/list_view.html"
    paginate_by = 10

    extra_context = {
        "title": "Facilities",
        "headers": ["Name", "Description", "Image", "Price Per Day"],
        "fields": ["name", "description", "image", "price_per_day",],
    }

class FacilityCreateView(AddExtraContextMixin, CreateView):
    model = Facility
    template_name = "main/insert_view.html"
    form_class = FacilityForm 
    success_url = reverse_lazy("facility_list")

    extra_context = {
        "title": "Facility"
    }


class FacilityUpdateDeleteView(View):
    template_name = "main/detail_view.html"

    extra_context = {
        "title": "Facility"
    }

    def get(self, request, pk):
        facility = get_object_or_404(Facility, pk=pk)
        form = FacilityForm(instance=facility)
        return render(request, self.template_name, {'form': form, 'facility': facility, "extra": self.extra_context})

    def post(self, request, pk):
        facility = get_object_or_404(Facility, pk=pk)

        if "delete" in request.POST:
            facility.delete()
            return redirect("facility_list")

        form = FacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            return redirect("facility_list")

        return render(request, self.template_name, {'form': form, 'facility': facility, "extra": self.extra_context})



# BOOKING
class AdminBookingsListView(AddExtraContextMixin, ListView):
    model = Booking
    template_name = "main/list_view.html"
    paginate_by = 10

    extra_context = {
        "title": "Bookings",
        "disable_create": True,
        "headers": ["Resident", "Facility", "Start Date", "End Date", "Total Price", "Status"],
        "fields": ["user", "facility", "start_date", "end_date", 'total_price', "status"],
    }



def booking_detail(request, pk):
    booking = get_object_or_404(Booking, id=pk)

    if request.method == "POST":
        form = BookingApprovalForm(request.POST, instance=booking)
        if form.is_valid():
            status = form.cleaned_data["status"]
            form.save()
            
            if status == "approved":
                Income.objects.create(
                    category="facility",
                    amount=booking.total_price,
                    received_from=booking.user,
                    description=f"Facility booking for {booking.facility.name} from {booking.start_date} to {booking.end_date}",
                    date_received=date.today(),
                )
            return redirect("booking_list")

    else:
        form = BookingApprovalForm(instance=booking)

    return render(request, "main/booking_detail.html", {"booking": booking, "form": form})


# CONTRIBUTION


class AdminContributionsListView(AddExtraContextMixin, ListView):
    model = Contribution
    template_name = "main/list_view.html"
    paginate_by = 10

    extra_context = {
        "title": "Contributions",
        "disable_create": True,
        "headers": ["User", "Event", "Amount", "Status", "Date"],
        "fields": ["user", "event", "amount", "status", "contributed_at"],
    }


def contribution_detail(request, pk):
    contribution = get_object_or_404(Contribution, id=pk)

    if request.method == "POST":
        form = ContributionApprovalForm(request.POST, instance=contribution)
        if form.is_valid():
            status = form.cleaned_data["status"]
            form.save()

            if status == "verified":
                Income.objects.create(
                    category="Donation",
                    amount=contribution.amount,
                    received_from=contribution.user,
                    description=f"Contribution for {contribution.event.name}",
                    date_received=date.today(),
                )

                contribution.event.total_fund_collected = F("total_fund_collected") + contribution.amount
                contribution.event.save(update_fields=["total_fund_collected"])
            return redirect("contribution_list")

    else:
        form = ContributionApprovalForm(instance=contribution)

    return render(request, "main/contribution_detail.html", {"contribution": contribution, "form": form})



# MAINTANCE

def maintenance_overview(request):
    selected_month = int(request.GET.get("month", now().month))
    selected_year = int(request.GET.get("year", now().year))

    maintenance_records = Maintenance.objects.filter(month=selected_month, year=selected_year)
    records_exist = maintenance_records.exists()

    months = [
        (i, datetime(2000, i, 1).strftime("%B")) for i in range(1, 13)
    ]
    years = [year for year in range(2023, now().year + 1)]

    if request.method == "POST" and not records_exist:
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            residents = User.objects.filter(is_staff=False, is_superuser=False)

            # Create maintenance record for each resident
            for resident in residents:
                Maintenance.objects.create(user=resident, month=selected_month, year=selected_year, amount=amount)

            return redirect("maintenance_overview")

    else:
        form = MaintenanceForm()

    return render(
        request,
        "main/maintenance_overview.html",
        {
            "maintenance_records": maintenance_records,
            "selected_month": selected_month,
            "selected_year": selected_year,
            "months": months,
            "years": years,
            "records_exist": records_exist,
            "form": form,
        },
    )


def maintenance_detail(request, pk):
    maintenance = get_object_or_404(Maintenance, id=pk)

    if request.method == "POST":
        form = MaintenanceApprovalForm(request.POST, instance=maintenance)
        if form.is_valid():
            status = form.cleaned_data["status"]
            form.save()
        

            if status == "verified":
                Income.objects.create(
                    category="Maintenance Payment",
                    amount=maintenance.amount,
                    received_from=maintenance.user,
                    description=f"Maintenance payment by {maintenance.user.profile.full_name}",
                    date_received=date.today(),
                )

            return redirect("maintenance_overview") 

    else:
        form = MaintenanceApprovalForm(instance=maintenance)

    return render(request, "main/maintenance_detail.html", {"maintenance": maintenance, "form": form})

class UserListView(AddExtraContextMixin, ListView):
    model = Complaint
    template_name = "main/list_view.html"
    paginate_by = 10

    extra_context = {
        "title": "Users",
        "headers": ["Username", "Fullname", "Contact Number" "Email", "Is Staff"],
        "fields": ["username", "email", "fullname", "contact_number" "is_staff"],
    }



# VISITORS

class VisitorListView(ListView):
    model = Visitor
    template_name = "main/visitor_logs.html"
    paginate_by = 5

    def get_queryset(self):
        return Visitor.objects.filter(check_out_time__isnull=False)


class CreateVisitorView(CreateView):
    form_class = VisitorForm
    template_name = "main/visitor_entry.html"
    models = Visitor
    success_url = reverse_lazy("dashboard")


def mark_out(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id)
    visitor.check_out()
    
    return redirect(reverse_lazy('dashboard'))



# EVENTS

def event_list(request):
    events = Event.objects.all().order_by('-event_date')
    return render(request, 'main/resident/events.html', {"events": events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    contribution = event.contributions.filter(user=request.user).first()

    return render(request, 'main/resident/event_detail.html', {'event': event, "contribution": contribution})


@login_required
def contribute_to_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = ContributionForm(request.POST, request.FILES)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.user = request.user
            contribution.event = event 
            contribution.save()
            return redirect("resident_event_detail", event_id=event.id)

    else:
        form = ContributionForm()

    return render(request, "main/resident/contribute.html", {"event": event, "form": form})





# BOOKINGS

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "main/resident/booking_list.html", {"bookings": bookings})

@login_required
def book_facility_page(request):
    total_price = None
    booking = None

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            facility = form.cleaned_data["facility"]
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            days_booked = (end_date - start_date).days
            total_price = days_booked * facility.price_per_day

            booking = form.save(commit=False)
            booking.user = request.user
            booking.total_price = total_price
            booking.save()

            return redirect("resident_facility_payment", booking.id)
    else:
        form = BookingForm()

    return render(request, "main/resident/booking.html", {
        "form": form,
        "total_price": total_price,
        "booking": booking
    })

def facility_payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        payment_screenshot = request.FILES.get("payment_screenshot")

        if payment_screenshot:
            booking.payment_proof = payment_screenshot
            booking.status = "processing"
            booking.save()

            return redirect("my_bookings")

    return render(request, "main/resident/booking_payment.html", {
        "booking": booking,
    })


def maintenance_payment_page(request, pk):
    maintenance = get_object_or_404(Maintenance, id=pk)

    if request.method == "POST":
        payment_screenshot = request.FILES.get("payment_screenshot")

        if payment_screenshot:
            maintenance.payment_proof = payment_screenshot
            maintenance.status = "processing" 
            maintenance.save()
            return redirect("dashboard")

    return render(request, "main/resident/pay_maintenance.html", {
        "maintenance": maintenance,
    })


# COMPLAIN

@login_required
def resident_complaints(request):
    complaints = Complaint.objects.filter(resident=request.user).order_by("-submitted_at")
    return render(request, "main/resident/complaints.html", {"complaints": complaints})


@login_required
def submit_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.resident = request.user 
            complaint.save()
            return redirect("resident_complaints")

    else:
        form = ComplaintForm()

    return render(request, "main/resident/submit_complaint.html", {"form": form})