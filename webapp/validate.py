def article_validator(article):
    errors = {}
    if not article.title:
        errors['title'] = "Название обязательное поле"
    elif len(article.title) > 50:
        errors['title'] = "Длина поля не может быть больше чем 50"

    if not article.content:
        errors['content'] = "Контент обязательное поле"

    if not article.author:
        errors['author'] = "Автор обязательное поле"
    elif len(article.author) > 50:
        errors['author'] = "Длина поля не может быть больше чем 50"
    return errors