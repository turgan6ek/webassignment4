from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions are only allowed to the author of the post
        return obj.author == request.user.username
