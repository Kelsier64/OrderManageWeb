from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import TemplateView, ListView,DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from base.models import ExtendedUser,Product,Order,Announcement
from django.shortcuts import get_object_or_404
from .forms import ProductForm,RegistrationForm,UserEditForm,EditProductForm
from django.contrib.auth.decorators import login_required

class OpRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        extended_user = ExtendedUser.objects.get(user=request.user)
        if extended_user.user_class != 'op':
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

class RegistView(LoginRequiredMixin, OpRequiredMixin, TemplateView):
    template_name = 'regist.html'
    
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/op/userManage/?page=1")
        return render(request, self.template_name, {'form': form})

class HomeView(LoginRequiredMixin, OpRequiredMixin, ListView):
    template_name = 'opHome.html'
    model = Announcement
    context_object_name = 'notes'


class UserEditView(LoginRequiredMixin, OpRequiredMixin, TemplateView):
    template_name = 'userEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userId = self.request.GET.get('userId')
        user = ExtendedUser.objects.get(user__id=userId)
        initial_data = {
            'userId': user.user.id,
            'userName': user.user.username,
            'user_class': user.user_class,
            'name': user.name,
        }
        form = UserEditForm(initial=initial_data)
        context['form'] = form
        return context
    
    def post(self, request):
        form = UserEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/op/userManage/?page=1")
        return render(request, self.template_name, {'form': form})
    

class UserDelView(LoginRequiredMixin, View, OpRequiredMixin):
    def get(self, request):
        userId = request.GET['userId']
        try:
            user = User.objects.get(id=userId)
            user.delete()
            return redirect("/op/userManage/?page=1")
        except:
            return redirect("/op/userManage/?page=1")
        
class OrderDelView(LoginRequiredMixin, View, OpRequiredMixin):
    def get(self, request):
        id = request.GET['id']
        try:
            order = Order.objects.get(id=id)
            order.delete()
            return redirect("/op/check/")
        except:
            return redirect("/op/check/")
        
class ProductDelView(LoginRequiredMixin, View, OpRequiredMixin):
    def get(self, request):
        id = request.GET['id']
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return redirect("/op/productManage/")
        except:
            return redirect("/op/productManage/")

class UserManageView(LoginRequiredMixin, OpRequiredMixin, ListView):
    model = ExtendedUser
    template_name = 'userManage.html'
    context_object_name = 'users'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        pages = {
            "pre": page_obj.previous_page_number() if page_obj.has_previous() else 1,
            "next": page_obj.next_page_number() if page_obj.has_next() else paginator.num_pages,
            "max": paginator.num_pages,
            "now": page_obj.number,
        }
        context['page'] = pages

        return context
    
class CheckView(LoginRequiredMixin, TemplateView, OpRequiredMixin):
    template_name = 'opCheck.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()
        products = Product.objects.all()
            
        context['orders'] = orders
        return context


class ProductView(LoginRequiredMixin, TemplateView, OpRequiredMixin):
    template_name = 'products.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        platforms = Product.objects.values_list('platform', flat=True).distinct()
        products = Product.objects.all()
        
        context['platforms'] = platforms
        context['products'] = products
        return context



class CreateProductView(LoginRequiredMixin, OpRequiredMixin, TemplateView):
    template_name = 'create.html'
    
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/op/productManage/")
        return render(request, self.template_name, {'form': form})
    
    
class EditProductView(LoginRequiredMixin, OpRequiredMixin, TemplateView):
    template_name = 'editProduct.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.GET.get('id')
        product = Product.objects.get(id=id)

        initial_data = {
            "id":product.id,
            'release_date': product.release_date,
            'platform': product.platform,
            'product_name': product.product_name,
            'suggested_price': product.suggested_price,
            'notes': product.notes,
        }
        form = EditProductForm(initial=initial_data)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = EditProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/op/productManage/")
        return render(request, self.template_name, {'form': form})
    