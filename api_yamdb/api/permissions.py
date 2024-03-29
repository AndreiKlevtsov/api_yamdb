from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Полные права на управление всем контентом проекта.
    Может создавать и удалять произведения, категории и жанры.
    Может назначать роли пользователям.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Полные права на управление всем контентом проекта только у администратора.
    Незарегистрированным пользователям доступно чтение.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin)
                )


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Права на изменение у администратора/модератора/юзера.
    Незарегистрированным пользователям доступно чтение.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
