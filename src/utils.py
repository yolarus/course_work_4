from django.core.exceptions import ValidationError


def check_photo(photo):
    """
    Проверка веса и формата загружаемой фотографии
    """
    max_size = 5 * 1024 ** 2
    if photo:
        if photo.size > max_size:
            raise ValidationError("Размер изображения не должен превышать 5 Мб")
        elif photo.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
            raise ValidationError("Можно загрузить файлы только форматов JPEG, JPG, PNG")
        return photo
    else:
        return False
