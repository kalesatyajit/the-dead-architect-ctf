import os
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, send_file, session, url_for
from werkzeug.security import check_password_hash

from database import get_db, init_db


app = Flask(__name__)
app.config["SECRET_KEY"] = "local-development-key"
app.config["DATABASE_PATH"] = os.environ.get(
    "DATABASE_PATH", str(Path(app.root_path) / "dead_architect.db")
)
app.config["ARTIFACTS_PATH"] = os.environ.get(
    "ARTIFACTS_PATH", str(Path(app.root_path).parents[1] / "artifacts")
)


@app.before_request
def ensure_database() -> None:
    init_db(app.config["DATABASE_PATH"])


@app.route("/")
def index():
    db = get_db(app.config["DATABASE_PATH"])
    featured = db.execute(
        "SELECT * FROM projects WHERE featured = 1 AND status = 'public' ORDER BY year DESC"
    ).fetchall()
    return render_template("index.html", featured=featured)


@app.route("/project/<slug>")
def project(slug: str):
    db = get_db(app.config["DATABASE_PATH"])
    item = db.execute(
        "SELECT * FROM projects WHERE slug = ? AND status = 'public'", (slug,)
    ).fetchone()
    if item is None:
        return render_template("error.html", message="Project not found."), 404
    return render_template("projects.html", project=item)


@app.route("/projects")
def projects():
    db = get_db(app.config["DATABASE_PATH"])
    items = db.execute(
        "SELECT * FROM projects WHERE status = 'public' ORDER BY year DESC"
    ).fetchall()
    return render_template("projects.html", projects=items)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        db = get_db(app.config["DATABASE_PATH"])
        user = db.execute(
            "SELECT username, password FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            return redirect(url_for("index"))
        error = "Those credentials did not match the studio log."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/api/projects")
def api_projects():
    db = get_db(app.config["DATABASE_PATH"])
    items = db.execute(
        "SELECT id, slug, title, artist, year, genre, cover_color "
        "FROM projects WHERE status = 'public' ORDER BY year DESC"
    ).fetchall()
    return jsonify([dict(item) for item in items])


@app.route("/api/projects/<int:project_id>")
def api_project_detail(project_id: int):
    db = get_db(app.config["DATABASE_PATH"])
    item = db.execute(
        "SELECT id, slug, title, artist, year, genre, description, cover_color, "
        "featured, status, studio_note FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()
    if item is None:
        return jsonify(error="Project not found", id=project_id), 404
    return jsonify(dict(item))


@app.route("/archive/architect-notes.git")
def archive_download():
    archive_path = Path(app.config["ARTIFACTS_PATH"]) / "architect-notes.git.tar.gz"
    if not archive_path.is_file():
        return render_template("error.html", message="Archive unavailable."), 404
    return send_file(archive_path, as_attachment=True, download_name=archive_path.name)


@app.route("/media/<path:artifact_name>")
def media_download(artifact_name: str):
    allowed = {"vault.enc", "final_mix.wav", "architect_node"}
    if artifact_name not in allowed:
        return render_template("error.html", message="Media not found."), 404
    artifact_path = Path(app.config["ARTIFACTS_PATH"]) / artifact_name
    if not artifact_path.is_file():
        return render_template("error.html", message="Media unavailable."), 404
    return send_file(artifact_path, as_attachment=True, download_name=artifact_name)


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    init_db(app.config["DATABASE_PATH"])
    app.run(host="0.0.0.0", port=5000)
