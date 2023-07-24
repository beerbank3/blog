from functools import wraps
from django.shortcuts import get_object_or_404
from .models import Log, Post

def log_action(action):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            post_id = kwargs.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            log_data = {
                'user' : 'guest',
                'post' : post,
                'action': action,
                'ip_address': request.META['REMOTE_ADDR'],
                'user_agent': request.META.get('HTTP_USER_AGENT'),
                'referrer': request.META.get('HTTP_REFERER'),
            }

            # 로그인된 사용자인 경우에만 유저 정보 추가
            if request.user.is_authenticated:
                log_data['user'] = request.user

            Log.objects.create(**log_data)

            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator