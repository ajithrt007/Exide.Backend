from django.utils.text import slugify

def custom_slugify(value, max_length=30):
    slug = slugify(value)
    if len(slug) > max_length:
        return slug[:max_length]
    return slug