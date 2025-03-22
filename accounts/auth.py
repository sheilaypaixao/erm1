from rest_framework.exceptions import AuthenticationFailed, APIException

from django.contrib.auth.hashers import check_password, make_password

from accounts.models import User
from companies.models import Enterprise
from companies.models import Employee

class Authentication:
    def signin(self, email=None, password=None):
        exception_auth = AuthenticationFailed("Usuário ou email não encontrados")

        user_not_exist = User.objects.filter(email=email).exists()

        if not user_not_exist:
            raise exception_auth
        
        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise exception_auth

        return user
    
    def signup(self, name, email, password, type_account='owner', company_id=False, company_name=None):
        if not name or name == '':
            raise AuthenticationFailed("O nome não deve ser nulo")
        
        if not email or email == '':
            raise AuthenticationFailed("O email não deve ser nulo")
        
        if not password or password == '':
            raise AuthenticationFailed("A senha não deve ser nula")

        user = User.objects.filter(email=email).exists()
        if user:
            raise AuthenticationFailed("Esse email já existe")

        password_rashed = make_password(password)

        created_user = User.objects.create(
            name=name,
            email=email,
            password=password_rashed,
            is_owner=0 if type_account == 'employee' else 1
        )

        if type_account=='owner' and company_name and company_name!='':
            company = Enterprise.objects.create(
                name=company_name,
                owner_id=created_user.id
            )

        if (company_id and company_id!='') or (company):
            Employee.objects.create(
                user_id=created_user.id,
                enterprise_id=company_id or company.id
            )

        return created_user