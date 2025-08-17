"""
Base Views and Common Functionality
====================================

This module contains base view classes and common functionality
that can be shared across different view modules.
"""

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


class BaseListView(generics.ListAPIView):
    """
    Base list view with common functionality.
    """
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Override to add common filtering logic.
        """
        queryset = super().get_queryset()
        
        # Add pagination info to response
        if hasattr(self, 'paginate_queryset'):
            return queryset
        
        return queryset


class BaseCreateView(generics.CreateAPIView):
    """
    Base create view with common functionality.
    """
    permission_classes = [IsAdminUser]
    
    def create(self, request, *args, **kwargs):
        """
        Override to add custom response formatting.
        """
        response = super().create(request, *args, **kwargs)
        
        # Add success message
        if response.status_code == status.HTTP_201_CREATED:
            response.data['message'] = f'{self.serializer_class.Meta.model.__name__} created successfully'
        
        return response


class BaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Base detail view with common functionality.
    """
    permission_classes = [IsAdminUser]


class BaseUpdateView(generics.UpdateAPIView):
    """
    Base update view with common functionality.
    """
    permission_classes = [IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        """
        Override to add custom response formatting.
        """
        response = super().update(request, *args, **kwargs)
        
        # Add success message
        if response.status_code == status.HTTP_200_OK:
            response.data['message'] = f'{self.serializer_class.Meta.model.__name__} updated successfully'
        
        return response


class BaseDeleteView(generics.DestroyAPIView):
    """
    Base delete view with common functionality.
    """
    permission_classes = [IsAdminUser]
    
    def destroy(self, request, *args, **kwargs):
        """
        Override to add custom response formatting.
        """
        instance = self.get_object()
        model_name = instance.__class__.__name__
        
        response = super().destroy(request, *args, **kwargs)
        
        # Add success message
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {'message': f'{model_name} deleted successfully'},
                status=status.HTTP_200_OK
            )
        
        return response


# Mixins for common functionality
class FilterMixin:
    """
    Mixin to add common filtering functionality.
    """
    
    def filter_by_ids(self, queryset, param_name, field_name=None):
        """
        Filter queryset by list of IDs.
        
        Args:
            queryset: Django queryset to filter
            param_name: URL parameter name (e.g., 'teacher')
            field_name: Model field name (defaults to param_name + '_id')
        """
        if field_name is None:
            field_name = f"{param_name}_id"
        
        ids = self.request.query_params.getlist(param_name)
        if ids:
            filter_kwargs = {f"{field_name}__in": ids}
            queryset = queryset.filter(**filter_kwargs)
        
        return queryset
    
    def filter_by_boolean(self, queryset, param_name, field_name=None):
        """
        Filter queryset by boolean parameter.
        
        Args:
            queryset: Django queryset to filter
            param_name: URL parameter name
            field_name: Model field name (defaults to param_name)
        """
        if field_name is None:
            field_name = param_name
        
        value = self.request.query_params.get(param_name, None)
        if value is not None:
            bool_value = value.lower() == 'true'
            filter_kwargs = {field_name: bool_value}
            queryset = queryset.filter(**filter_kwargs)
        
        return queryset
    
    def filter_by_search(self, queryset, param_name='search', field_names=None):
        """
        Filter queryset by text search across multiple fields.
        
        Args:
            queryset: Django queryset to filter
            param_name: URL parameter name (defaults to 'search')
            field_names: List of field names to search (defaults to ['title', 'name'])
        """
        if field_names is None:
            field_names = ['title', 'name']
        
        search_term = self.request.query_params.get(param_name, None)
        if search_term:
            from django.db.models import Q
            
            query = Q()
            for field_name in field_names:
                try:
                    # Check if field exists on the model
                    queryset.model._meta.get_field(field_name)
                    query |= Q(**{f"{field_name}__icontains": search_term})
                except:
                    # Skip field if it doesn't exist
                    continue
            
            if query:
                queryset = queryset.filter(query)
        
        return queryset
