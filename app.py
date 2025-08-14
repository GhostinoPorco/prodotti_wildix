from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

CSV_FILE = "prodotti.csv"

# Funzione per caricare il CSV
def load_data():
    return pd.read_csv(CSV_FILE)

@app.route("/get_product", methods=["POST"])
def get_product():
    try:
        data = request.json
        product_name = data.get("name")
        if not product_name:
            return jsonify({"error": "Parametro 'name' mancante"}), 400

        df = load_data()

        # Cerca il prodotto ignorando maiuscole/minuscole
        match = df[df["Nome"].str.lower() == product_name.lower()]

        if match.empty:
            return jsonify({"error": "Prodotto non trovato"}), 404

        prodotto = match.iloc[0].to_dict()
        return jsonify(prodotto)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)