from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        if request.user.is_authenticated:
            return obj.owner == request.user

        anon_id = request.session.get("anon_id")
        return anon_id and str(obj.anonymous_id) == anon_id


# class ReadPerm(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS and request.user and request.user.is_staff:
#             return True
#         return request.user and request.user.is_authenticated
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS and request.user and request.user.is_staff:
#             return True
#         return obj.owner == request.user


class ReadPerm(BasePermission):
    def has_permission(self, request, view):
        # Authenticated users can always POST (create)
        if request.method == "POST":
            return bool(request.user and request.user.is_authenticated)

        # For all other methods, must at least be authenticated
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Staff can read/write/delete everything
        if request.user.is_staff:
            return True

        # Normal users:
        if request.method in SAFE_METHODS:
            # Can only read their own object
            return obj.owner == request.user

        if request.method in ("PUT", "PATCH", "DELETE"):
            # Can only modify their own object
            return obj.owner == request.user

        return False
