# CometReverseApi
Serves user data from Comet platform with reverse engineering

A simple REST Api to fetch and serve data like user profile info, skils and experiences from the platform 'Comet'

Tech Stack:
  - FastApi: Lightweight rest api framework for Python. Have a good documentation, easy to implement and OpenApi documentation is integrated.
  - Pydantic: Data validation, JSON serialization/deserialization library for Python, works well with FastApi. Preferred to create strict dtos and validate them. 
  Also enforces type hints at runtime and provides user friendly errors when data is invalid.
  - SQLAlchemy: Choosed as ORM. Well documented.
  - SQLite: Integrated easily with Python. A real relational or nosql database server is not needed at this phase.
  
Logging handled with 'logging' module of Python.
Intercepter added as FastApi's @middleware to log incoming requests to this app.
  
Dockerfile and docker-compose.yml are ready to use.
To run this application as a container, run 'docker-compose up' command. Then you can reach the app from 8000 port.


OpenApi documentation: http://localhost:8000/docs
