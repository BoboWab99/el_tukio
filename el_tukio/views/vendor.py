from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404

from el_tukio.forms import VendorRegForm, BusinessProfileForm, VendorImageUploadForm
from el_tukio.models import User, Vendor, VendorImageUpload
from el_tukio.utils.decorators import vendor_required
from el_tukio.utils.main import print_form_values


class Register(CreateView):
    model = User
    form_class = VendorRegForm
    template_name = 'main/register/register.html'
    extra_context = {'title': 'Vendor Registration'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Login successful!')
        return redirect('vendor-dashboard')


@vendor_required
def dashboard(request):
    return render(request, 'vendor/dashboard.html')


@vendor_required
def profile(request):
    return render(request, 'vendor/profile.html')


@method_decorator(vendor_required, name='dispatch')
class BusinessProfileUpdate(UpdateView):
    form_class = BusinessProfileForm
    template_name = 'vendor/profile-update.html'

    def get_object(self):
        return get_object_or_404(Vendor, pk=self.request.user.pk)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Business profile updated!')
        return redirect('vendor-profile')


@method_decorator(vendor_required, name='dispatch')
class BusinessGallery(CreateView):
    form_class = VendorImageUploadForm
    template_name = 'vendor/business-gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gallery"] = VendorImageUpload.objects.filter(vendor_id=self.request.user.id)
        return context

    # def get(self, request):
        
    #     pass

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        print(form)

        if form.is_valid():
            # file = VendorImageUpload(
            #     vendor_id=self.request.user.pk,
            #     image=form.cleaned_data['image'],
            #     caption=form.cleaned_data['caption']
            # )
            # file.save()
            messages.success(self.request, 'Form valid!')
        # return render(request, self.template_name, {'form': form})


@vendor_required
def business_gallery(request):
    context = {
        'gallery': VendorImageUpload.objects.filter(vendor_id=request.user.pk),
        'form': VendorImageUploadForm
    }
    return render(request, 'vendor/business-gallery.html', context)


@vendor_required
def upload_business_image(request):
    form = VendorImageUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, form.errors.as_text())
        return redirect('business-gallery')

    image = form.cleaned_data['image']
    caption = form.cleaned_data['caption']
    img = VendorImageUpload(
        vendor_id = request.user.id,
        image=image,
        caption=caption,
    )
    img.save()
    messages.success(request, 'New image uploaded!')
    return redirect('business-gallery')