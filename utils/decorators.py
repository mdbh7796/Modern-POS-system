def require_admin(func):
    def wrapper(self, *args, **kwargs):
        if getattr(self, 'role', None) != 'admin':
            raise PermissionError("Admin access required")
        return func(self, *args, **kwargs)
    return wrapper
