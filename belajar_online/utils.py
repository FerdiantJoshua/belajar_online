from belajar_online import settings
from django.urls import reverse_lazy

def set_fields_css_class(fields):
    for key in fields:
        placeholder = ' '.join(list(map(lambda x: x[0].upper() + x[1:], key.split('_'))))
        fields[key].widget.attrs.update({'class': 'input', 'placeholder': placeholder})


def add_invalid_css_class_to_form(func):
    def wrapper(*args, **kwargs):
        form = args[1]
        objects = form.fields if form.non_field_errors() else form.errors
        for key in objects:
            field = form.fields.get(key)
            field.widget.attrs.update({'class': field.widget.attrs['class'] + ' is-danger'})
        return func(*args, **kwargs)
    return wrapper


def context_processors(request):
    context = {'is_dev_mode': settings.DEV_MODE}

    if request.build_absolute_uri('?').split(request.get_host(), 1)[1] in list(map(reverse_lazy, settings.HIDE_NAV)):
        context['hide_nav'] = True

    if request.build_absolute_uri('?').split(request.get_host(), 1)[1] in list(map(reverse_lazy, settings.HIDE_FOOTER)):
        context['hide_footer'] = True
        
    if request.build_absolute_uri('?').split(request.get_host(), 1)[1] in list(map(reverse_lazy, settings.HIDE_SCROLLBAR)):
        context['hide_scrollbar'] = True
        
    return context