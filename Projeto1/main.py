from flask import Flask, request, jsonify
from boto3 import resource

app = Flask(__name__)
dynamodb = resource('dynamodb')

@app.route("/nome", methods=["POST", "GET"])
def nome():
    if request.method == "POST":
        # Get the name from the request body
        name = request.json.get("nome")
        if not name:
            return "É preciso informar um nome para gravar", 500
        # Generate a unique ID
        item_id = # generate unique id
        # Store the name and ID in DynamoDB
        table = dynamodb.Table("BANCO_NOME")
        table.put_item(Item={'id': item_id, 'nome': name})
        return "Gravado com sucesso", 200
    elif request.method == "GET":
        # Retrieve all names and IDs from DynamoDB
        table = dynamodb.Table("BANCO_NOME")
        items = table.scan()
        if not items:
            return "nenhum nome gravado", 404
        # Return the names and IDs as a JSON array
        return jsonify([{'id': item['id'], 'nome': item['nome']} for item in items['Items']])

if __name__ == "__main__":
    app.run()
