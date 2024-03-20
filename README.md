## About
This is a small backend application written while learning [DRF](https://github.com/encode/django-rest-framework) from [this](https://github.com/ilyachch/django-rest-framework-rusdoc) translation of the official documentation.

## Launch
To launch this application:
1. clone this repository
2. optionally populate a .env file based on the .env.template file, or set the appropriate environment variables
3. run within docker
```
git clone https://github.com/TheArtur128/DRF-practice.git
docker compose --project-directory ./DRF-practice up
```

Go to http://localhost/api/root (or whatever host or protocol you choose) to get almost all endponits (the rest are in http://localhost/api/other).
