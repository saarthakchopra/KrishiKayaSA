from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from main.models import CustomUser, Inventory
from main.form import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import logout as logouts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json

from django.urls import reverse_lazy
# Create your views here.

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'main/signup.html'

class UserLoginPageView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

def logoutUser(request):
    if request.method=='GET':
        logouts(request)
        return redirect('login')

class StockList(LoginRequiredMixin,ListView):
    model = Inventory
    template_name = 'main/dashboard.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = context['items'].filter(user=self.request.user)
        context['count'] = context['items'].count() 
        #context['market_count'] = context['items'].filter(sale_status='on_sale')
        return context

class ItemDetail(LoginRequiredMixin,DetailView):
    model = Inventory
    template_name = 'main/item_detail.html'
    context_object_name = 'item'

class CreateItem(LoginRequiredMixin, CreateView):
    model = Inventory
    template_name = 'main/create_item_form.html'
    fields = ['name', 'item_type', 'cost_per_item', 'quantity_in_stock', 'quantity_sold', 'sale_status', 'item_image']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Set last_sales_date if quantity_sold is provided
        quantity_sold = form.cleaned_data['quantity_sold']
        if quantity_sold is not None:
            form.instance.last_sales_date = timezone.now().date()

            # Calculate sales
            cost_per_item = form.cleaned_data['cost_per_item']
            form.instance.sales = quantity_sold * cost_per_item

        return super().form_valid(form)

class UpdateItem(LoginRequiredMixin,UpdateView):
    model = Inventory
    fields = ['name', 'item_type', 'cost_per_item', 'quantity_in_stock', 'quantity_sold','sale_status','item_image']
    template_name = 'main/create_item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Get the instance of the object being updated
        instance = form.instance
        
        # Check if quantity_sold has changed
        if form.cleaned_data['quantity_sold'] != instance.quantity_sold:
            # If quantity_sold has changed, update last_sales_date to current date
            instance.last_sales_date = timezone.now()

        # Calculate sales if quantity_sold is updated
        quantity_sold = form.cleaned_data['quantity_sold']
        cost_per_item = instance.cost_per_item  # Use instance's current cost_per_item
        if quantity_sold is not None:
            instance.sales = quantity_sold * cost_per_item

        return super().form_valid(form)

class DeleteItem(LoginRequiredMixin,DeleteView):
    model = Inventory
    context_object_name = 'item'
    template_name = 'main/item_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

@login_required
def analytics(request):
    inventories = Inventory.objects.filter(user=request.user)
    df = read_frame(inventories)

    sales_graph_df = df.groupby(by='last_sales_date', as_index=False,sort=False)['sales'].sum()
    # sales_graph = px.line(sales_graph_df, x = sales_graph_df.last_sales_date, y = sales_graph_df.sales, title='Sales Trend')
    sales_graph = px.line(sales_graph_df, x='last_sales_date', y='sales', title='Sales Trend')
    sales_graph = json.dumps(sales_graph,cls=plotly.utils.PlotlyJSONEncoder)

    best_performing_product_df = df.groupby(by='name').sum().sort_values(by="quantity_sold")
    # best_performing_product = px.bar(best_performing_product_df,
    #                                     x = best_performing_product_df.index,
    #                                     y = best_performing_product_df.quantity_sold,
    #                                     title = "Best Performing Product")
    best_performing_product = px.bar(best_performing_product_df,
                                  x=best_performing_product_df.index,
                                  y='quantity_sold',  # Change this line
                                  title="Best Performing Product")

    best_performing_product_df = json.dumps(best_performing_product,cls=plotly.utils.PlotlyJSONEncoder)

    most_product_in_stock_df = df.groupby(by='name').sum().sort_values(by='quantity_in_stock')
    most_product_in_stock = px.pie(
        most_product_in_stock_df,
        names = most_product_in_stock_df.index,
        values = most_product_in_stock_df.quantity_in_stock,
        title = "Most Product in Stock"
    )
    most_product_in_stock = json.dumps(most_product_in_stock,cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "sales_graph": sales_graph,
        "best_performing_product": best_performing_product_df,
        "most_product_in_stock": most_product_in_stock
    }
    
    return render(request, 'main/analytics.html',context = context)

class marketPlace(ListView):
    model = Inventory
    template_name = 'main/marketPlace.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset()
        state_filter = self.request.GET.get('state')
        type_filter = self.request.GET.get('type')

        if state_filter:
            queryset = queryset.filter(user__state=state_filter)
        if type_filter:
            queryset = queryset.filter(item_type=type_filter)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['states'] = Inventory.objects.values_list('user__state', flat=True).distinct()
        context['item_types'] = Inventory.objects.values_list('item_type', flat=True).distinct()
        return context