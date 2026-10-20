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
| Deploy | Docker Compose on port `8080` |

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

Open http://localhost:8080

This deploy uses a mock stock API on port `5001` so the demo works without Oracle. To start the real backend as well (Oracle required):

```bash
docker compose --profile oracle up -d --build
```

## Jenkins setup

1. Install Jenkins and the plugins: **Git**, **GitHub**, **Pipeline**, **JUnit**.
2. Give the Jenkins user permission to run Docker (`docker` group, or mount `/var/run/docker.sock` if Jenkins is in a container).
3. Create a **Multibranch Pipeline** job pointing at this GitHub repository. Jenkins will pick up the root `Jenkinsfile`.
4. Add a GitHub webhook: `http://<jenkins-host>:8080/github-webhook/` with events **push** and **pull request**.
5. Use feature branches and Pull Requests. Jenkins validates the PR. Merge to `main` only after the build is green. Deployment runs on `main` / `master` only.

Pipeline stages:

| Stage | Purpose |
| --- | --- |
| Checkout | Pull the latest commit from GitHub |
| Build | Build frontend, mock API, and Selenium images |
| Selenium Tests | Headless Chrome tests; publish JUnit XML |
| Deploy | `docker compose up` on `main` / `master` after tests pass |

## API URL

The UI uses `VITE_API_URL` (see `Frontend/src/config.js`). Defaults to `http://localhost:5001`. CI builds the frontend with `http://mock-api:5001` so Selenium inside Docker can reach the mock API.
