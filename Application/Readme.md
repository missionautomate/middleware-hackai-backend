| Language | Framework | Platform | Author |
| -------- | -------- |--------|--------|
| Python | Django | Azure Web App, Virtual Machine| |


# Python Django web application

Sample Python Django web application built using Visual Studio 2017.

# APPLICATION SETUP
0. Install requirements
    0.0. If necessary, run `pip install python3-venv`; Create a new virtualenv using `python -m venv venv`
    0.1. Activate the new virtualenv: Run `source venv/bin/activate` (Linux); Run `venv\Scripts\activate.bat` (Windows)
    0.2. Run `which python` and `which pip` to ensure you are using the right interpreter & Python module manager
    0.3. Run `pip install -r requirements.txt`
1. Obtain the Azure connection string
    1.1. If needed, create a new Microsoft Azure account
    1.2. Create a new Storage Account via the [Azure Web UI](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.Storage%2FStorageAccounts)
    1.3. Access the settings page of the new Storage Account
    1.4. Left side > Networking > Firewalls and virtual networks > Checkmark "Add your client IP"
    1.5. Left side > Access keys > Connection String > Show & copy
2. Use the connection string in `backend/Application/mwbackend/views.py`
3. Create a superuser: `python manage.py createsuperuser`
4. Run the Django dev server: `python manage.py runserver`

## License:

See [LICENSE](LICENSE).

## Contributing

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

