from flask import Flask, render_template

app = Flask(__name__)

# Lista de músicas com cifras (exemplo)
musicas = [
    {"titulo": "Asa Branca", "artista": "Luiz Gonzaga", "arquivo": "asa_branca"},
    {"titulo": "Tocando em Frente", "artista": "Almir Sater", "arquivo": "tocando_em_frente"},
]

@app.route("/")
def index():
    return render_template("index.html", musicas=musicas)

@app.route("/cifra/<nome>")
def cifra(nome):
    try:
        with open(f"cifras/{nome}.txt", "r", encoding="utf-8") as f:
            conteudo = f.read()
        return render_template("cifra.html", titulo=nome.replace("_", " ").title(), cifra=conteudo)
    except FileNotFoundError:
        return "Cifra não encontrada", 404

if __name__ == "__main__":
    app.run(debug=True)
