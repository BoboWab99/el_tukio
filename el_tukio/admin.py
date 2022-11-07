from django.contrib import admin
from .models import User, Organizer, Planner, Vendor, VendorCategory, VendorImageUpload, Event, Review, Expense, ExpenseCategory, Task, TaskGroup


# Register your models here.
admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Planner)
admin.site.register(Vendor)
admin.site.register(VendorCategory)
admin.site.register(VendorImageUpload)
admin.site.register(Event)
admin.site.register(Review)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(Task)
admin.site.register(TaskGroup)