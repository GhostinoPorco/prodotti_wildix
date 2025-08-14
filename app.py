from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)
CSV_FILE = "products.csv"

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

# Endpoint per ottenere tutti i prodotti
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

# Endpoint per cercare prodotti per keyword parziale
@app.route("/search_products", methods=["GET"])
def search_products():
    try:
        keyword = request.args.get("q", "").lower()  # Prende la query dall'URL
        if not keyword:
            return jsonify({"error": "Devi fornire una keyword con ?q=keyword"}), 400

        if not os.path.exists(CSV_FILE):
            return jsonify({"error": "File CSV non trovato"}), 404

        results = []
        with open(CSV_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if keyword in row["name"].lower():
                    results.append({
                        "name": row["name"],
                        "price": row["price"],
                        "description": row["description"]
                    })

        if not results:
            return jsonify({"message": "Nessun prodotto trovato."}), 404

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": f"Errore nel server: {str(e)}"}), 500

if __name__ == "__main__":
    # Porta 10000 compatibile con Render
    app.run(host="0.0.0.0", port=10000)
