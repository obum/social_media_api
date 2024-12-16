Steps to Setup a token based authentication 

1. install restframework (pip install djangorestframework)

2. include the rest_framework into the INSTALLED APPS in the settings.py file

3. include the rest_framework.authtoken to INSTALLED_APPS

4. run python manage.py migrate to create a table to store authentication tokens.

5. Configure Default Authentication in settings.py
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
            ],
        }

6. create the token endpoint in the urls.py
    NB: Django REST Framework provides a built-in view for obtaining tokens. You can use this or create your own custom view.

    from django.urls import path
    from rest_framework.authtoken.views import obtain_auth_token

    urlpatterns = [
        ...
        path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    ]
7. Test with the token using POSTMAN
        Access the protected endpoint using the token as a Header input on POSTMAN : for example
        Authorization : Token 56565645@###$$dtvgbhjnjnc

 ------------------------------------------------------------------
-----------------USER AUTHENTICATION WORKFLOW----------------------
--------------------------------------------------------------------
8. Create the app to haandle the user authentication.
    python manage.py startapp accounts

9. register the app in the projects installed apps
    INSTALLED_APPS = [
        'accounts.apps.AccountsConfig',
    ]
10. include the accounts.urls in the project urls.py file
    urlpartterns = [
        path('accounts', include('accounts.urls'))
    ]

11. create a urls.py file for the accounts app. 
    Add the login/register/profile/logout urls to the accounts.urls file

    urlpartterns = [
        path('register/', include('accounts.urls')),
        path('login/', include('accounts.urls')),
        path('logout/', include('accounts.urls')),
    ]
    Use routers & Viewset to handle profile endpoints

    router = DefaultRouter()
    router.register('profile/', profileViewSet)

    Add the router to the urlpatterns

    urlpatterns += router.urls

12. Define the serializers which helps to handle all 
    data transformatiion process (custom user creation logic, updation login ) & Validation.

    class ModelnameSerializer(serializer.ModelSerializer):
        model = ModelName
        fields = [takes in all the fields to be serializeed]

    class RegisterSerializer(serializers.ModelSerializer):
         class Meta:
             model = User
             fields = ['username', 'password', 'email', 'bio', 'profile_picture']
             extra_kwargs = {'password': {'write_only': True}}

         def create(self, validated_data):
             user = User.objects.create_user(
                 username=validated_data['username'],
                 email=validated_data.get('email', ''),
                 bio=validated_data.get('bio', ''),
                 profile_picture=validated_data.get('profile_picture', ''),
                 password=validated_data['password']
             )
             return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']
        read_only_fields = ['followers']

    def update(self, instance, validated_data):
        # Update the fields based on validated_data
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)

        # Update the password only if provided (hashing automatically handled)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance


13. Define the views that consume take the serializers / permisions and
    determine  the business logic for the json response.

    