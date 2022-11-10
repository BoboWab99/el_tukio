from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models import CheckConstraint, Q, F
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed

from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image


class User(AbstractUser):
    """Model representing a general system user"""
    class UserType(models.IntegerChoices):
        ORGANIZER = 0, _('Organizer')
        PLANNER = 1, _('Planner')
        VENDOR = 3, _('Vendor')

        __empty__ = _('(Unkown)')

    user_type = models.SmallIntegerField(blank=True, null=True, choices=UserType.choices)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    profile = models.ImageField(default='default.png', upload_to='profile_pics')

    @property
    def is_organizer(self):
        return self.user_type == self.UserType.ORGANIZER

    @property
    def is_planner(self):
        return self.user_type == self.UserType.PLANNER
    
    @property
    def is_vendor(self):
        return self.user_type == self.UserType.VENDOR

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """Return the url to access a particular user"""
        return reverse('user-details', args=[str(self.id)])

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # resize big images using 'Pillow'
        # 'django-cleanup' deletes old version of the image once it is changed!
        img = Image.open(self.profile.path)
        if img.height > 300 or img.width > 300:
            img_size = (300, 300)
            img.thumbnail(img_size)
            img.save(self.profile.path)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    comment = models.CharField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)


class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    file = models.FileField(upload_to='uploads/')
    date_uploaded = models.DateTimeField(auto_now_add=True)


class ChatRoom(models.Model):
    class Type(models.IntegerChoices):
        PERSONAL = 0, _('Personal')
        GROUP = 1, _('Group')

    name = models.CharField(max_length=50, blank=True, null=True)
    type = models.SmallIntegerField(choices=Type.choices)
    members = models.ManyToManyField(User, blank=True, related_name='chatroom')

    # def clean(self, *args, **kwargs):
    #     if self.members.count() == 2:
    #         raise ValidationError(_("Personal chat can't have more than 2 people!"))
    #     super(ChatRoom, self).clean(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.type == self.Type.PERSONAL and self.members.count() == 2:
    #         raise ValidationError(_("Personal chat can't have more than 2 people!"))
    #     else:
    #         super().save(*args, **kwargs)


# limit members in personal chat
def chat_members_changed(sender, **kwargs):
    chatroom = kwargs['instance']
    if chatroom.type == ChatRoom.Type.PERSONAL and chatroom.members.count() > 2:
        raise ValidationError(_("Personal chat can't have more than 2 people!"))

m2m_changed.connect(chat_members_changed, sender=ChatRoom.members.through)


class ChatMessage(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=CASCADE)
    message = models.CharField(max_length=5000, help_text='Enter message...')
    sender = models.ForeignKey(User, on_delete=CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    reply_to = models.BigIntegerField(blank=True, null=True)

    @property
    def reference(self):
        return ChatMessage.objects.get(id=self.reply_to)

    class Meta:
        ordering = ['date_sent']


# class ChatMessageReply(ChatMessage):
#     reference = models.ForeignKey(ChatMessage, on_delete=CASCADE, related_name='chat_reply_message')

#     class Meta:
#         verbose_name = 'Chat Message Reply'
#         verbose_name_plural = 'Chat Message Replies'


class VendorCategory(models.Model):
    """Model representing a wedding vendor category. 
    Vendor categories are added by the Admin in the database. """
    name = models.CharField( max_length=200, help_text='Select a category (EG: Venues)')

    class Meta:
        verbose_name = 'Vendor Category'
        verbose_name_plural = 'Vendor Categories'

    def __str__(self):
        return self.name


class Organizer(models.Model):
    """Model representing a system user who's an organizer of an event"""
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    bookmarks = models.ManyToManyField(User, related_name='organizer_bookmarks')

    def __str__(self):
        return f'{self.user} (organizer)'


class Planner(models.Model):
    """Model representing a system user who's a professional planner of events"""
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    description = models.TextField(max_length=5000, help_text='Brief description of your business')
    services_offered = models.TextField(max_length=5000, help_text='List the particular services your business offers')
    city = models.CharField(max_length=100, help_text='Primary (Current) city of residence')
    location = models.CharField(max_length=200, help_text='EG: Ole Sangale Rd, Madaraka')  # street code
    up_for_business = models.BooleanField(default=True, help_text='Ready to take business at the moment?')
    bookmarks = models.ManyToManyField(User, related_name='planner_bookmarks')

    def __str__(self):
        return f'{self.user} (planner)'


class Vendor(models.Model):
    """Model representing a system user who's a vendor"""
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    business_name = models.CharField(max_length=100)
    category = models.ForeignKey(VendorCategory, on_delete=SET_NULL, null=True, blank=True, help_text='Select a category for your business.')
    description = models.TextField(max_length=5000, help_text='Brief description of your business')
    services_offered = models.TextField(max_length=5000, help_text='List the particular services your business offers')
    city = models.CharField(max_length=100, help_text='City in which your business is located')
    location = models.CharField(max_length=200, help_text='EG: Ole Sangale Rd, Madaraka')  # street code
    open_hours = models.CharField(max_length=500, default='24/7', help_text='Business service (working) times')
    up_for_business = models.BooleanField(default=True, help_text='Ready to take business at the moment?')

    def get_absolute_url(self):
        """Return the url to access a particular vendor"""
        return reverse('vendor-details', args=[str(self.id)])

    def __str__(self):
        return f'{self.business_name} ({self.category})'


class VendorImageUpload(models.Model):
    """Model representing a vendor's image upload"""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vendor_img_uploads')
    caption = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.vendor.business_name}'s image"


class Event(models.Model):
    """Model representing an event"""
    organizer = models.ForeignKey(Organizer, on_delete=CASCADE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField(help_text='When will this event be held?')
    event_budget = models.FloatField(help_text='What  is the budget for this event?')
    event_location = models.CharField(max_length=100, null=True, blank=True)
    guest_size = models.IntegerField(help_text='Expected number of guests at the event?')
    event_team = models.ManyToManyField(User, related_name='event_team_members')
    chatroom = models.OneToOneField(ChatRoom, on_delete=SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.event_name
    

class Review(models.Model):
    """Model representing an event organizer's rating of a planner or vendor"""
    organizer = models.ForeignKey(Organizer, on_delete=CASCADE)
    rated_user = models.ForeignKey(User, on_delete=CASCADE, related_name='rated_planner_or_vendor', editable=False)
    comment = models.CharField(max_length=500, help_text='Your comment on the business services')
    stars = models.SmallIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for {self.rated_user}'


class QuoteRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=CASCADE, related_name='receiver')
    comment = models.CharField(max_length=1000)


class Contract(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, _('Pending')
        ACCEPTED = 1, _('Accepted')
        DECLINED = 2, _('Declined')

    event = models.ForeignKey(Event, on_delete=CASCADE)
    contractor = models.ForeignKey(User, on_delete=CASCADE, related_name='contractor', help_text='Event Organizer|Planner giving the contract.')
    contractee = models.ForeignKey(User, on_delete=CASCADE, related_name='contractee', help_text='Planner|Vendor receiving the contract')
    terms = models.CharField(max_length=5000, help_text='Contract terms of agreement')
    status = models.SmallIntegerField(choices=Status.choices, default=Status.PENDING)
    date_sent = models.DateTimeField(auto_now_add=True, help_text='Time a contract is sent to the contractee')
    date_signed = models.DateTimeField(help_text='Time the contractee signs the contract', blank=True, null=True)

    @property
    def is_pending(self):
        return self.status == self.Status.PENDING

    @property
    def is_accepted(self):
        return self.status == self.Status.ACCEPTED

    @property
    def is_declined(self):
        return self.status == self.Status.DECLINED

    def __str__(self):
        return f'contract: evt|{self.event}, by {self.contractor}, to {self.contractee}'


class TaskGroup(models.Model):
    event = models.ForeignKey(Event, on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(max_length=500)
    
    def __str__(self) :
        return self.name


class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=CASCADE)
    task = models.TextField(max_length=5000)
    task_group = models.ForeignKey(TaskGroup, on_delete=SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True, help_text='When would you like to have this done?')
    created_by = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True, related_name='created_by')
    assigned_to = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True, related_name='assigned_to') 
    completed = models.BooleanField(default=False, help_text='Mark this task as completed')
    date_completed = models.DateField(blank=True, null=True)
    completed_by = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True, related_name='completed_by')
    comments = models.ManyToManyField(Comment, related_name='task_comments')
    files = models.ManyToManyField(FileUpload, related_name='task_files')
    deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.event}: {self.task}'


class ExpenseCategory(models.Model):
    """Model representing an expense category.
    Some general expense categories are pre-defined by the admin in the System.
    Users can add more categories of their own"""
    event = models.ForeignKey(Event, on_delete=CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, help_text='Categorize your expenses for proper budgeting.')

    class Meta:
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    """Model representing an budget item or expense"""
    event = models.ForeignKey(Event, on_delete=CASCADE)
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=SET_NULL, blank=True, null=True)
    description = models.TextField(max_length=5000)
    total_cost = models.FloatField(help_text='Estimated taotal cost of this budget item')
    total_paid = models.FloatField( default=0, help_text='Total amount already paid for this budget item')
    budgeted_by = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)
    date_budgeted = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, related_name='expense_comments')
    files = models.ManyToManyField(FileUpload, related_name='expense_files')
    deleted = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(blank=True, null=True)

    @property
    def balance_cleared(self):
        return self.total_paid and self.total_cost == self.total_paid

    class Meta:
        constraints = [
            CheckConstraint(check=Q(total_cost__gte=F('total_paid')), name='check_total_cost_vs_paid')
        ]

    def clean(self):
        super().clean()
        if self.total_paid > self.total_cost:
            raise ValidationError(_('Invalid. Total paid greater than total cost!'))

    def __str__(self):
        return self.description