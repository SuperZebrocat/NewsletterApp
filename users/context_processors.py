def is_manager(request):
    return {
        'is_manager': request.user.groups.filter(name='managers').exists()
    }
