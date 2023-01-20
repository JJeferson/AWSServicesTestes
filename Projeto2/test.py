import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
import lambda_function

class TestLambdaFunction(unittest.TestCase):
    @patch('lambda_function.boto3')
    def test_lambda_handler(self, mock_boto3):
        # Test the case where there are no rows with null values
        mock_s3_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_boto3.client.side_effect = [mock_s3_client, mock_sqs_client]
        mock_s3_client.download_file.return_value = None
        mock_sqs_client.send_message.return_value = None

        event = {}
        context = {}
        csv_file = "nome,telefone,endereco\nJohn,1234567890,NYC\nMike,0987654321,LA\n"
        with patch('builtins.open', mock_open(read_data=csv_file)):
            lambda_function.lambda_handler(event, context)

        mock_s3_client.download_file.assert_called_once_with("TESTE_S3", "PASTA123/arquivo_para_ser_usado.csv", "/tmp/arquivo_para_ser_usado.csv")
        mock_sqs_client.send_message.assert_has_calls([call(QueueUrl='https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/TESTE_SQS', MessageBody='{"nome": "John", "telefone": "1234567890", "endereco": "NYC"}'),
                                                       call(QueueUrl='https://sqs.us-east-1.amazonaws.com/<ACCOUNT_ID>/TESTE_SQS', MessageBody='{"nome": "Mike", "telefone": "0987654321", "endereco": "LA"}')])
        self.assertEqual(mock_sqs_client.send_message.call_count, 2)

        # Test the case where there are rows with null values
        mock_s3_client = MagicMock()
        mock_sqs_client = MagicMock()
        mock_boto3.client.side_effect = [mock_s3_client, mock_sqs_client]
        mock_s3_client.download_file.return_value = None
