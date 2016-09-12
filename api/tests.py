from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()

def main():
    """
    """

    user = User.objects.get(username='auto_test')
    pass

# Create your tests here.
if __name__ == '__main__':
    main()
