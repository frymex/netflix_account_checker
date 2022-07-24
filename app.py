from system.checker import start, Settings, Checker

# первый вариант использывания (дефолт)


def x1():
    start(username='username', password='password') # автоматическая проверка на потоках
    while True:
        if Settings.COMPLETED:
            print(Settings.RESULTS[0].json)
            break


# или в ручную

def x2():
    checker = Checker() # иницилазция чекера
    checker.set_login_and_password('username', 'password') # добавление кредитов в процесор
    checker.login_into_page() # загрузка страницы входа
    checker.try_login() # ввод кредитов и попытка авторизации
    result = checker.get_status() # получение результата возращает Response
    print(result.json) # выводим всю информацию в json
    print(result.cookies) # выводим только куки
    print(result.status) # выводим только статус (Valid - валид, Doesnt exists - не существует,
    # Invalid - данные не верны)






