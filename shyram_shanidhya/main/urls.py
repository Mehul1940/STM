from django.urls import path, include

from .views import *


urlpatterns = [

    path('', dashboard, name="dashboard"),

    # ROOMS

    path("rooms/", RoomListView.as_view(), name="room_list"),
    path("rooms/new", RoomCreateView.as_view(), name="add_room"),
    path('rooms/<int:pk>/', RoomUpdateDeleteView.as_view(), name='view_room'),


    # NOTICE

    path("notices/", NoticeListView.as_view(), name="notice_list"),
    path("notices/new", NoticeCreateView.as_view(), name="add_notice"),
    path('notices/<int:pk>/', NoticeUpdateDeleteView.as_view(), name='view_notice'),


    # EVENT
    path("events/", EventListView.as_view(), name="event_list"),
    path("events/new", EventCreateView.as_view(), name="add_event"),
    path('events/<int:pk>/', EventUpdateDeleteView.as_view(), name='view_event'),

    # USERS
    path("users/", user_list_view, name="user_list"),
    path("users/new", UserCreateView.as_view(), name="add_user"),
    path("users/<int:pk>/", UserUpdateDeleteView.as_view(), name="view_user"),

    # FACILITY
    path("facility/", FacilityListView.as_view(), name="facility_list"),
    path("facility/new", FacilityCreateView.as_view(), name="add_facility"),
    path("facility/<int:pk>/", FacilityUpdateDeleteView.as_view(), name="view_facility"),

    # BOOKING

    path("bookings/", AdminBookingsListView.as_view(), name="booking_list"),
    path("bookings/<int:pk>/", booking_detail, name="booking_detail"),

    # CONTRIBUTION

    path("contributions/", AdminContributionsListView.as_view(), name="contribution_list"),
    path("contributions/<int:pk>/", contribution_detail, name="contribution_detail"),


    # COMPLAINT
    path("complaints/", ComplaintListView.as_view(), name="complaint_list"),
    path("complaints/<int:pk>/", complaint_detail, name="view_complaint"),

    # FINANCE

    path('finance/', finance_overview, name='finance_overview'),
    path('finance/income/add/', IncomeCreateView.as_view(), name='add_income'),
    path('finance/expense/add/', ExpenseCreateView.as_view(), name='add_expense'),

    # MAINTANCE OVERVIEW

    path("maintenance/", maintenance_overview, name="maintenance_overview"),
    path("maintenance/<int:pk>/", maintenance_detail, name="maintenance_detail"),


    # VISITORS

    path("visitors/", VisitorListView.as_view(), name="visitor_list"),
    path('visitors/<int:visitor_id>/mark-out/', mark_out, name='mark_out'),
    path("visitors/new", CreateVisitorView.as_view(), name="add_visitor"),


    # RESIDENT
    path("resident/events/", event_list ,name="resident_event"),
    path('resident/events/<int:event_id>/', event_detail, name='resident_event_detail'),
    path("resident/events/<int:event_id>/contribute/", contribute_to_event, name="resident_event_contribute"),

    path("my-bookings/", my_bookings, name="my_bookings"),
    path("resident/booking/", book_facility_page, name="resident_book_facility"),
    path("resident/booking/payment/<int:booking_id>", facility_payment_page, name="resident_facility_payment"),


    path("resident/complaints/", resident_complaints, name="resident_complaints"),
    path("resident/complaints/submit/", submit_complaint, name="resident_submit_complaint"),
    path("resident/maintenance/<int:pk>/", maintenance_payment_page, name="resident_maintenance"),
]


