import random
import string
import psycopg2
import click
import os
from os.path import isfile, join
import yadisk
import tarfile
import boto3


def get_random_filename(format="png", length=16):
    """Generate random filename"""

    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    filename = f"{''.join(random.choice(letters) for i in range(length))}.{format}"
    return filename


def get_files_from_dir(path):
    """Return list of all files in directory"""

    files = [file for file in os.listdir(path) if isfile(join(path, file))]
    return files


@click.command()
@click.argument('from_dir')
@click.option('--yandex/--no-yandex', required=True)
@click.option('--url', required=True)
@click.option('--token', required=True)
@click.option('--save_dir', required=True)
@click.option('--database', '-db', required=True, help='Postgresql database to upload')
@click.option('--user', '-u', required=True, help='User with access to database')
@click.option('--password', '-p', required=True, help='Password of user with access to database')
@click.option('--host', '-h', default="127.0.0.1")
@click.option('--port', default="5432")
@click.option('--table', required=True, help='Name of table with photos')
@click.option('--aws/--no-aws', required=True)
@click.option('--img_type', required=True)
def main(yandex, url, token, save_dir, from_dir, database, user, password, host, port, table, aws, img_type):
    # # Соединяемся с базой данных
    # con = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    # cur = con.cursor()

    # Вводим данные хранилища если необходимо
    if aws:
        session = boto3.session.Session()
        client = session.client(
            's3',
            region_name=input('Enter region name\n> '),
            endpoint_url=input('Enter endpoint url\n> '),
            aws_access_key_id=input('Enter "AWS ACCESS KEY ID"\n> '),
            aws_secret_access_key=input('Enter "AWS SECRET ACCESS KEY"\n> ')
        )
        space_name = input('Enter space name\n> ')
        dir_to_load = input('Enter directory where the images will be uploaded\n> ')

    if yandex:
        y = yadisk.YaDisk(token)
        print(f'Downloading files from {url}')
        y.download_public(
            public_key=url,
            file_or_path="from_disk.tar.gz"
        )
        archive = tarfile.open('from_disk.tar.gz')
        print(f'Extracting files to {save_dir}')
        archive.extractall(f"{save_dir}")
        archive.close()

    files = [('/'.join([os.path.abspath(os.getcwd()), from_dir]), image_path) for image_path in get_files_from_dir(from_dir)]
    print(files)

    # for path, image_filename in files:
    #     filename = get_random_filename()
    #     os.rename(f"{path}/{image_filename}", f"{path}/{filename}")
    #     # Добавляем фото в БД
    #     cur.execute(
    #         f"INSERT INTO {table} (is_real,type,photo_url) VALUES (true, '{img_type}', '{filename}')"
    #     )
    #
    #     con.commit()
    #     # Загружаем в хранилище при необходимости
    #     if aws:
    #         client.upload_file(
    #             f"{path}/{filename}",
    #             space_name,
    #             f"{dir_to_load}/{filename}",
    #             ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'}
    #         )

    con.close()


if __name__ == '__main__':
    main()
