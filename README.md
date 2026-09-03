# The Dead Architect

The Dead Architect is a fictional producer portfolio website and an intentionally vulnerable local CTF challenge. It contains no real secrets, credential theft features, persistence mechanisms, or destructive behavior.

## Requirements

- Docker Desktop with Docker Compose

## Start the challenge

From this directory, build and start the container:

```text
docker compose up --build
```

Open [http://localhost:5000](http://localhost:5000) in a browser. The container includes a health check at `/health`.

To run in the background:

```text
docker compose up --build -d
```

## Stop the challenge

```text
docker compose down
```

To also remove the persisted SQLite volume and reset the sample data:

```text
docker compose down -v
```

## Project locations

- Flask application: `challenge/app/app.py`
- SQLite setup and queries: `challenge/app/database.py`
- HTML templates: `challenge/app/templates/`
- CSS and JavaScript: `challenge/app/static/`
- Future challenge artifacts: `organizer/`

The SQLite database is initialized automatically when the web container starts and is stored in the `challenge-data` Docker volume.

The generated player artifacts are served only through their application routes: the encrypted archive is at `/media/vault.enc`, the audio is at `/media/final_mix.wav`, the native analysis target is at `/media/architect_node`, and the Git archive is at `/archive/architect-notes.git`. Organizer scripts regenerate these during the Docker build.

For organizer validation outside Docker, run `python organizer/verify_challenge.py` after installing the test dependencies and a C compiler. The automated tests are in `tests/`.

## Sample login

The foundation includes a deliberately non-sensitive sample account for demonstrating the login flow:

- Username: `architect`
- Password: `demo-only`

Replace or remove this sample account as the challenge develops. Do not use real credentials or secrets in this local challenge.
