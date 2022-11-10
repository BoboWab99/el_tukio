from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from el_tukio.views import main, organizer, planner, vendor


urlpatterns = [
    path('', main.index, name='home'),
    path('login/', main.user_login, name='login'),
    path('logout/', main.user_logout, name='logout'),
    path('vendors/', main.vendors, name='vendors'),
    path('planners/', main.planners, name='planners'),
    path('vendors/<int:vendor_id>/details/', main.vendor_details, name='vendor-details'),
    path('planners/<int:planner_id>/details/', main.planner_details, name='planner-details'),
    path('<str:user_type>/bookmarks/', main.bookmarks, name='bookmarks'),
    path('users/<int:user_id>/bookmark/', main.bookmark, name='bookmark'),
    path('users/<int:user_id>/bookmark/remove/', main.remove_bookmark, name='remove-bookmark'),
    path('users/<int:user_id>/hire/', main.hire_seller, name='hire-seller'),
    path('my/deals/', main.current_deals, name='current-deals'),
    path('my/deals/<str:status>/', main.current_deals, name='current-deals'),
    path('my/deals/sign/<int:deal_id>/<str:action>/', main.sign_contract, name='sign-deal'),
    path('events/<int:event_id>/chatroom/', main.event_chatroom, name='event-chatroom'),
    path('events/<int:event_id>/chatroom/chat-with/<int:chat_with>/', main.event_chatroom, name='event-chatroom'),
    path('my/calendar/', main.calendar, name='calendar'),
    path('my/calendar/<int:yy>/<int:mm>/', main.calendar, name='calendar'),
    path('my/calendar/<int:yy>/<int:mm>/<int:dd>/', main.calendar, name='calendar'),
    # path('csrf-token/', main.get_csrf)
]

urlpatterns += [
    path('register/', include([
        path('', main.register, name='register'),
        path('organizer/', organizer.Register.as_view(), name='register-organizer'),
        path('planner/', planner.Register.as_view(), name='register-planner'),
        path('vendor/', vendor.Register.as_view(), name='register-vendor')
    ]))
]

urlpatterns += [
    path('user-account/', include([
        path('', main.user_account, name='user-account'),
        path('update/username/', main.UsernameUpdate.as_view(), name='change-username'),
        path('update/names/', main.NameUpdate.as_view(), name='change-name'),
        path('update/email/', main.EmailUpdate.as_view(), name='change-email'),
        path('update/password/', main.PasswordUpdate.as_view(), name='change-password'),
    ]))
]

urlpatterns += [
    path('organizer/', include([
        path('dashboard/', organizer.dashboard, name='organizer-dashboard'),
        path('events/', organizer.Events.as_view(), name='organizer-events'),
        path('events/<int:event_id>/details/', organizer.event_details, name='organizer-event-details'),
        path('events/<int:event_id>/update/', organizer.event_update, name='organizer-event-update'),
        path('events/<int:event_id>/team/', organizer.event_team, name='organizer-event-team'),

        path('events/<int:event_id>/tasks/', organizer.tasks, name='organizer-event-tasks'),
        path('events/<int:event_id>/tasks/group=<int:group_id>/', organizer.tasks, name='organizer-event-tasks'),
        path('events/<int:event_id>/tasks/group=<int:group_id>/delete/', organizer.delete_task_group, name='delete-task-group'),
        path('events/<int:event_id>/tasks/group=<int:group_id>/delete/tasks-included=<str:tasks_included>/',
             organizer.delete_task_group, name='delete-task-group'),
        path('tasks/<int:task_id>/details/', organizer.task_details, name='task-details'),
        path('tasks/<int:task_id>/complete/', organizer.complete_task, name='complete-task'),
        path('tasks/<int:task_id>/delete/', organizer.delete_task, name='delete-task'),
        path('tasks/<int:task_id>/assign/<int:member_id>/', organizer.assign_to, name='assign-to'),
        path('tasks/<int:task_id>/assign/remove/', organizer.assign_to_remove, name='assign-to-remove'),

        path('events/<int:event_id>/expenses/', organizer.budget_tracker, name='organizer-event-expenses'),
        path('expenses/<int:exp_id>/details/', organizer.expense_details, name='organizer-exp-details'),
        path('expenses/<int:id>/delete/', organizer.delete_expense, name='delete-expense'),
    ]))
]

urlpatterns += [
    path('planner/', include([
        path('dashboard/', planner.dashboard, name='planner-dashboard'),
    ]))
]

urlpatterns += [
    path('vendor/', include([
        path('dashboard/', vendor.dashboard, name='vendor-dashboard'),
        path('business-profile/', vendor.profile, name='vendor-profile'),
        path('business-profile/update/', vendor.BusinessProfileUpdate.as_view(), name='vendor-profile-update'),
        path('business-gallery/', vendor.business_gallery, name='business-gallery'),
        path('business-gallery/upload', vendor.upload_business_image, name='business-gallery-upload'),
    ]))
]


# Handle media files
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
