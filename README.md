# Stock-A-Mock

A mock stock-market web app used as the platform for a DevOps CI/CD pipeline with **GitHub, Jenkins, and Selenium**.

Team: Jeffin Solomon Asir J S (2023103501), Viswa S (2023103564), Ganesh S (2023103582)

## What this project demonstrates

Every push or Pull Request to GitHub can trigger Jenkins. Jenkins checks out the code, builds the application, runs Selenium browser tests, and deploys only when those tests pass.

```
Developer  →  GitHub (branch / PR)  →  Jenkins
                                      ├─ Checkout
                                      ├─ Build (Docker)
                                      ├─ Selenium tests
                                      └─ Deploy to Docker (main only)
```

## Application

| Area | Stack |
| --- | --- |
| Frontend | React + Vite |
| Backend | Node.js + Express + Oracle DB |
| Tests | Python, pytest, Selenium WebDriver (headless Chrome) |
| CI/CD | Jenkins declarative pipeline (`Jenkinsfile`) |
| Deploy | Docker Compose on port `3000` |

Local development (without Docker):

```bash
# Frontend
cd Frontend && npm install && npm run dev

# Backend (needs Oracle and Backend/.env)
cd Backend && npm install && npm run dev
```

Frontend: http://localhost:5173  
Backend: http://localhost:5001

## Run the CI pipeline locally (same as Jenkins)

Requires Docker Desktop.

```bash
mkdir -p reports
docker compose -p stock-ci -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from selenium-tests
docker compose -p stock-ci -f docker-compose.test.yml down -v
```

Selenium covers:

- Home page load
- Navigation (home → login / signup)
- Login and signup form interactions
- Stock list retrieval and symbol search

Failed tests stop the pipeline. Jenkins will not deploy.

## Deploy (Continuous Deployment)

After tests pass on `main` / `master`, Jenkins runs:

```bash
docker compose -p stock-cd -f docker-compose.yml up -d --build
```

Open http://localhost:3000

The deployed app uses the Express backend on port `5001` and the existing Oracle database at `localhost:1521/XEPDB1`. The frontend on port `3000` is configured to call that backend. The database container and its persistent volume are not part of test cleanup.

## Jenkins setup

1. Use the Jenkins already running at **http://localhost:8080**. Jenkins itself does not need to run in Docker.
2. Install plugins if missing: **Git**, **GitHub**, **GitHub Branch Source**, **Pipeline**, **JUnit**.
3. The pipeline uses `docker compose` to build, test, and deploy the app, so the OS user that runs Jenkins must be able to run `docker` (on macOS, Docker Desktop running is enough for a typical local Jenkins).
4. Create a **Multibranch Pipeline** job pointing at this GitHub repository. Jenkins will pick up the root `Jenkinsfile`.
5. GitHub webhooks cannot reach a laptop `localhost`. In the Multibranch Pipeline job, enable **Scan Multibranch Pipeline Triggers → Periodically if not otherwise run** and set the interval to **5 minutes**. This discovers branch changes without requiring a public Jenkins endpoint. Pull request discovery and merge protection are controlled by Jenkins and GitHub settings.
6. Use feature branches and Pull Requests. Deployment runs on `main` / `master` only. The live app is **http://localhost:3000**.

Pipeline stages:

| Stage | Purpose |
| --- | --- |
| Checkout | Pull the latest commit from GitHub |
| Build | Build frontend, mock API, and Selenium images |
| Selenium Tests | Headless Chrome tests; publish JUnit XML |
| Deploy | `docker compose up` on `main` / `master` after tests pass |

## API URL

The production UI uses `http://localhost:5001` for the Oracle-backed Express API. The isolated Selenium stack uses the mock API on its internal Docker network and publishes test-only ports `5002` (API) and `3001` (frontend). Jenkins tears this stack down after tests pass or fail; production ports and the Oracle data volume are separate.
