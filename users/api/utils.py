from django.core.mail import send_mail


def send_activation_mail(email, activation_code):
    subject = 'Активация аккаунта'
    message = f"""
                Здравствуйте, уважаемый пользователь! Спасибо за регистрацию на нашем сайте!
                Для активации Вашего аккаунта пройдите по ссылке: 
                http://127.0.0.1:8000/account/activate/{activation_code}

    """

    from_ = 'test@project.com'
    emails = [email, ]
    print(emails)

    send_mail(subject, message, from_, emails)
