!include common/acronyms.yaml

# SCOPE

## Identification

- Name: Flask Web Application
- Version: 1.0.0
- Deployment Environment: Containerized Linux environment (e.g., Docker)
- Interface: REST API accessible over +https

## System Overview

!include common/system_overview.md

## Document Overview

This document details the software's version, components, and configuration, following MIL-STD-498 guidance. It specifies modified components, dependencies, deployment configuration, and instructions for this release.

# REFERENCE DOCUMENTS

::: {#refs}
:::

:::{#reference_table}

| References  |
|-------------|
| placeholder |
: Reference Documents {#tbl:reference_documents}

:::

# VERSION DESCRIPTION

[@idd-XXXX] provides details of the software design.
[@str-XXXX] provides details of testing outcomes. 

## Inventory of Materials Released

The version comprises the following files, directories, and artifacts:

- **Source Code Repository**: [Git Repository URL]
    - Branch/Commit: [Branch Name] / [Commit SHA]
- **Build Scripts**:
    - `Dockerfile` - for containerized deployment
    - `requirements.txt` - for Python dependencies
- **Entrypoint**: `gunicorn` serving the Flask app located at `application.py`.
- Docker Service Configuration (e.g., YAML):
- Executables:
    - `app.py`: Flask entry script
    - `gunicorn` worker service

## Inventory of Software Contents

## Adaptation data

###  Configuration Identification

**Hardware**:

- Architecture: x86_64 (Linux)
- Memory Recommended: 4GB Min

**Software**:

- Gunicorn Version: 20.1.0
- Python Version: 3.12+
- Flask Version: 2.3.2
- Docker Version: 23.0.1

**Dependencies**: Defined in `requirements.txt` as:

``` 
   Flask==2.3.2
   gunicorn==20.1.0
   some-other-dependency==1.2.3
```

## Related Documents

@tbl:related_documents lists the documents associated with the release of the software identified in this +vdd.

| Identifier | Revision | Title                     | Date       | Reference |
|------------|:--------:|---------------------------|------------|:---------:|
| IDD-XXXX   |    1     | Interface Design Document | yyyy-mm-dd | @idd-XXXX |
| STD-XXXX   |    2     | Software Test Description | yyyy-mm-dd | @std-XXXX |
| STR-XXXX   |    3     | Software Test Report      | yyyy-mm-dd | @str-XXXX |
| SUM-XXXX   |    1     | Software User Manual      | yyyy-mm-dd | @sum-XXXX |

: Related documents {#tbl:related_documents}


## Modules and Files

- `app.py`: Defines Flask routing
- `settings.py`: Configuration for Flask application
- `static/` and `templates/`: HTML and CSS files for rendering views
- `Dockerfile`: Containerization setup
- `run.sh`: Startup script for initializing Gunicorn

## Changes in This Release

- Added endpoints:
    - `/api/resource`: Handles API GET/POST requests

- Optimized static file handling.
- Increased Gunicorn worker count from 2 to 4 to improve performance.

# Installation Instructions

**Installation via Docker**:
1. Clone the repository:
``` bash
      git clone [repository-url]
      cd [repository-directory]
```
1. Build Docker image:

``` bash
      docker-compose up --build
```

1. Access application at `http://localhost:5000`.

**Standalone Installation (non-docker)**:

``` bash
   pip install -r requirements.txt
   gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

# Notes

## Acronyms

## Terminology

| Term                    | Definition                                                                                                                                           |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Gunicorn**            | A Python WSGI HTTP server that handles HTTP requests and distributes them to Flask workers for processing.                                           |
| **Flask**               | A Python-based micro-web framework used to develop web applications and RESTful APIs.                                                                |
| **WSGI**                | Web Server Gateway Interface, a standard for Python web applications to communicate with web servers (e.g., Gunicorn).                               |
| **Static Files**        | Front-end resources such as CSS (Cascading Style Sheets), JavaScript files, and images required for rendering the application's user interface (UI). |
| **API Handlers**        | Functions or classes in Flask that define the endpoints (routes) of the application and handle incoming HTTP requests.                               |
| **External APIs**       | Third-party services or APIs that the application interacts with to fetch or process additional data (e.g., payment services or external databases). |
| **Database**            | A persistent storage system used for saving and retrieving structured data (e.g., MySQL, PostgreSQL, or SQLite).                                     |
| **Response**            | The HTTP response sent by the Flask application (via Gunicorn) to the client in the form of JSON, HTML, or other content types.                      |
| **Docker**              | A platform used to deploy, run, and package applications in containers, ensuring consistency across environments.                                    |
| **Request**             | An HTTP request sent by the client to the server. It can be a GET, POST, PUT, or DELETE request, depending on the action required.                   |
| **Entrypoint**          | The starting point or execution command for the software. In this case, Gunicorn serves as the entry point for the Flask application.                |
| **Static File Handler** | A Flask or Gunicorn component responsible for serving static files such as images, CSS, and JavaScript to the end-user.                              |
| **Route**               | A URL path defined in Flask that maps HTTP requests to specific functions or logic in the application.                                               |
| **REST API**            | A type of API built using Representational State Transfer principles, allowing stateless communication between the client and server over HTTP.      |

: Terminology Table {#tbl:terminology}

::: landscape

# Appendix A. Interface and Deployment Matrix

The following table provides a consolidated reference for key application interfaces, deployment settings, runtime dependencies, configuration inputs, operational assumptions, and verification considerations.

| Category             | Item                   | Description                                                               | Source / Location                | Required Value or Example              | Configuration Method                             | Runtime Impact                                                   | Verification Method                                               |
|----------------------|------------------------|---------------------------------------------------------------------------|----------------------------------|----------------------------------------|--------------------------------------------------|------------------------------------------------------------------|-------------------------------------------------------------------|
| Application Identity | Application Name       | Identifies the released software application.                             | Release documentation            | Flask Web Application                  | Documented release metadata                      | Used for traceability across deployment and support artifacts.   | Confirm name matches release package and repository metadata.     |
| Application Identity | Version                | Defines the specific released version of the software.                    | Release documentation            | 1.0.0                                  | Documented release metadata                      | Supports baseline tracking and rollback decisions.               | Compare release tag, package label, and deployment notes.         |
| Deployment           | Container Platform     | Describes the expected containerized runtime environment.                 | Docker runtime                   | Docker 23.0.1 or compatible            | Docker engine installation                       | Determines container build and execution compatibility.          | Run container build and startup validation.                       |
| Deployment           | Operating System       | Defines the target host operating system family.                          | Host environment                 | Linux x86_64                           | Host provisioning                                | Affects package compatibility, file paths, and runtime behavior. | Confirm host architecture and operating system before deployment. |
| Deployment           | Application Port       | Network port exposed by the application service.                          | Service configuration            | 5000                                   | Docker Compose or runtime command                | Determines how clients reach the REST API.                       | Access `http://localhost:5000` or configured endpoint.            |
| Runtime              | WSGI Server            | Production server used to run the Flask application.                      | Startup command                  | Gunicorn                               | `gunicorn -w 4 -b 0.0.0.0:5000 app:app`          | Manages worker processes and request handling.                   | Confirm Gunicorn process starts without errors.                   |
| Runtime              | Worker Count           | Number of Gunicorn worker processes.                                      | Startup command                  | 4                                      | Gunicorn command-line option                     | Affects request throughput and resource usage.                   | Inspect startup logs or process list.                             |
| Runtime              | Python Version         | Python interpreter version required by the application.                   | Runtime image or host            | Python 3.12+                           | Docker image or host installation                | Determines language and dependency compatibility.                | Run `python --version` in the target environment.                 |
| Dependency           | Flask                  | Web framework used to implement the REST API.                             | `requirements.txt`               | Flask 2.3.2                            | Python package installation                      | Provides routing, request handling, and response generation.     | Run dependency inspection or application smoke test.              |
| Dependency           | Gunicorn               | WSGI server dependency used to host the Flask app.                        | `requirements.txt`               | Gunicorn 20.1.0                        | Python package installation                      | Provides production-grade process management.                    | Run `gunicorn --version`.                                         |
| Configuration        | Environment Mode       | Indicates whether the application runs in development or production mode. | Environment variables            | `APP_ENV=production`                   | Runtime environment variable                     | May affect logging, debugging, and security behavior.            | Inspect container or host environment variables.                  |
| Configuration        | Debug Flag             | Controls debug behavior.                                                  | Environment variables            | `DEBUG=False`                          | Runtime environment variable                     | Should remain disabled in production deployments.                | Confirm debug mode is disabled during deployment validation.      |
| Configuration        | External Configuration | Optional dynamic configuration source.                                    | `settings.py` or `config.json`   | Environment-specific settings          | Configuration file or loader                     | Allows deployment-specific values without source changes.        | Confirm configuration is loaded during startup.                   |
| Interface            | REST API Base Access   | Primary client interface over HTTP or HTTPS.                              | Application routes               | `http://localhost:5000`                | Network and service configuration                | Enables client access to application functions.                  | Submit a test HTTP request and validate response.                 |
| Interface            | Resource Endpoint      | Endpoint supporting resource operations.                                  | Flask routes                     | `/api/resource`                        | Application routing                              | Provides GET and POST API behavior.                              | Test GET and POST requests with expected payloads.                |
| Operations           | Static File Handling   | Method used to serve front-end assets.                                    | Application/static configuration | Optimized static handling              | Flask configuration or web server setup          | Affects page rendering and asset load performance.               | Load UI pages and verify CSS, JavaScript, and images.             |
| Operations           | Logging                | Runtime event and error reporting.                                        | Application and Gunicorn logs    | Standard output / container logs       | Runtime logging configuration                    | Supports troubleshooting and operational monitoring.             | Review logs after startup and request execution.                  |
| Operations           | Health Validation      | Basic verification that the service is available.                         | Deployment procedure             | Successful HTTP response               | Manual or automated smoke test                   | Confirms application is running and reachable.                   | Execute endpoint request and confirm expected status code.        |
| Security             | Public Exposure        | Determines whether the service is exposed externally.                     | Network configuration            | Internal or controlled external access | Firewall, reverse proxy, or container networking | Impacts attack surface and access control requirements.          | Review network bindings and ingress rules.                        |
| Security             | Secrets Handling       | Method for providing sensitive values.                                    | Runtime environment              | Environment variables or secret store  | Deployment platform configuration                | Prevents secrets from being hardcoded in source files.           | Confirm sensitive values are not committed to repository.         |

: Interface and Deployment Matrix Table {#tbl:interface-deployment-matrix}

:::
