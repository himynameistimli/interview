from django.urls import path

from emart_mgmt import views

app_name = 'emart_mgmt'
urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', views.AddProductView.as_view(), name='add_product'),
    path('product/edit/<int:product_id>', views.EditProductView.as_view(), name='edit_product'),
    path('product/delete/<int:product_id>', views.DeleteProductView.as_view(), name='delete_product'),
    path('products/recommended/', views.RecommendedProductView.as_view(), name='recommended_products'),
]
