import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime  # Importar datetime

from Casas import lambda_handler


@pytest.mark.parametrize("page_number, url", [
    (1, "https://casas.mitula.com.co/casas/pereira/"),
])
@patch('Casas.requests.get')
@patch('Casas.boto3.client')
def test_lambda_handler(
        mock_boto3_client,
        mock_requests_get,
        page_number,
        url):
    # Configurar el comportamiento simulado de requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'<!DOCTYPE html><html><body>' + \
        b'<h1>Test</h1></body></html>'
    mock_requests_get.return_value = mock_response

    mock_s3_client = MagicMock()
    mock_boto3_client.return_value = mock_s3_client

    event = {}
    context = MagicMock()

    # Llamar a la función lambda_handler
    lambda_handler(event, context)

    # Verificar que se llamó a requests.get con la URL correcta
    mock_requests_get.assert_called_once_with(url)

    # Verificar que se llamó a s3.put_object con los parámetros correctos
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_key = f'casas/contenido-pag-{page_number}-{current_date}.html'
    mock_s3_client.put_object.assert_called_once_with(
        Body=mock_response.content, Bucket='zappa-q6y33fmy5', Key=file_key)

    # Verificar que se devuelve un diccionario con statusCode 200 y body
    # 'Páginas descargadas y guardadas en S3 correctamente.'
    expected_response = {
        'statusCode': 200,
        'body': 'Páginas descargadas y guardadas en S3 correctamente.'}
    assert lambda_handler(event, context) == expected_response
