import boto3
import pandas as pd

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    sqs = boto3.client("sqs")
    queue_url = "https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/TESTE_SQS"

    # Download the file from S3
    s3.download_file("TESTE_S3", "PASTA123/arquivo_para_ser_usado.csv", "/tmp/arquivo_para_ser_usado.csv")

    # Load the data from the CSV file
    df = pd.read_csv("/tmp/arquivo_para_ser_usado.csv")

    for index, row in df.iterrows():
        if pd.isnull(row["nome"]) or pd.isnull(row["telefone"]) or pd.isnull(row["endereco"]):
            print(f"Linha {index} com campos null")
            continue
        message = {"nome": row["nome"], "telefone": row["telefone"], "endereco": row["endereco"]}
        try:
            sqs.send_message(QueueUrl=queue_url, MessageBody=str(message))
        except:
            print("Erro ao enviar a mensagem para a fila")
