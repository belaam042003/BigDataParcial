import requests
import boto3
from datetime import datetime


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'fzappa-q6y33fmy5'

    for page_number in range(1, 6):
        if page_number == 1:
            url = 'https://casas.mitula.com.co/casas/pereira/'
        else:
            url = 'https://casas.mitula.com.co/casas/pereira/{page_number}'
        response = requests.get(url)

        if response.status_code == 200:
            current_date = datetime.now().strftime('%Y-%m-%d')
            file_key = 'casas/contenido-pag-{page_number}-'.format(
                page_number=page_number
            ) + '{current_date}.html'.format(current_date=current_date)

            s3.put_object(
                Body=response.content,
                Bucket=bucket_name,
                Key=file_key)

    return {
        'statusCode': 200,
        'body': 'Páginas descargadas y guardadas en S3 correctamente.'
    }
