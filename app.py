from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
CSV_FILE = "prodotti.csv"

# Endpoint per aggiungere un prodotto
@app.route("/add_product", methods=["POST"])
def add_product():
    try:
        data = request.get_json(force=True)
        if not data or not all(k in data for k in ("name", "description", "price")):
            return jsonify({"error": "JSON non valido. Richiesti: name, description, price"}), 400

        # Scrive sul CSV
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([data["name"], data["description"], data["price"]])

        return jsonify({"message": "Prodotto aggiunto con successo!"})

    except Exception as e:
        return jsonify({"error": f"Errore nel server: {str(e)}"}), 500

# Endpoint per ottenere i prodotti
@app.route("/get_products", methods=["GET"])
def get_products():
    try:
        products = []
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    products.append(row)
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": f"Errore nel server: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
