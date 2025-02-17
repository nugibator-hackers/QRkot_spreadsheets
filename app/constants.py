MIN_PASSWORD_LENGTH = 3
SHORT_PASSWORD = (
    'Пароль должен содержать не менее {} символов.'
).format(MIN_PASSWORD_LENGTH)
EMAIL_IN_PASSWORD = 'Пароль не должен содержать e-mail.'
USER_REGISTERED = 'Пользователь {} зарегистрирован.'
MAX_CHARITY_PROJECT_NAME_LENGTH = 100
MAX_DESCRIPTION_PREVIEW_LENGTH = 10

NAME_DUPLICATE = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_IS_CLOSED = 'Проект закрыт и недоступен для редактирования!'
PROJECT_HAS_DONATIONS = 'В проект были внесены средства, не подлежит удалению!'
FULL_AMOUNT_LESS_INVESTED_AMOUNT = (
    'Нельзя установить значение full_amount '
    'меньше уже вложенной суммы.'
)