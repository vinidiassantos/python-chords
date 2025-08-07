from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'cifras'
db = SQLAlchemy(app)

# Modelo de música
class Musica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    arquivo = db.Column(db.String(100), nullable=False)

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Página inicial com busca
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        termo = request.form["busca"]
        musicas = Musica.query.filter(
            (Musica.titulo.contains(termo)) | (Musica.artista.contains(termo))
        ).all()
    else:
        musicas = Musica.query.all()
    return render_template("index.html", musicas=musicas)

# Página de upload de cifras
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        titulo = request.form["titulo"]
        artista = request.form["artista"]
        arquivo = request.files["arquivo"]

        # Salvar o arquivo na pasta 'cifras'
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
        arquivo.save(caminho)

        # Salvar os dados no banco
        nova_musica = Musica(titulo=titulo, artista=artista, arquivo=arquivo.filename)
        db.session.add(nova_musica)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("upload.html")

# Página para exibir a cifra
@app.route("/cifra/<nome_arquivo>")
def cifra(nome_arquivo):
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    return render_template("cifra.html", cifra=conteudo)

# Executar localmente (ignorado no Render)
if __name__ == "__main__":
    app.run(debug=True)
