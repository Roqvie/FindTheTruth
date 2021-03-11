import requests
import random
import string
import psycopg2
import click
import boto3


def get_random_filename(media_src="img", format="png", length=16):
    """Generate random filename"""

    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    filename = f"{media_src}/{''.join(random.choice(letters) for i in range(length))}.{format}"
    return filename


@click.command()
@click.argument('num_of_photos', type=int)
@click.option('--database', '-db', required=True, help='Postgresql database to upload')
@click.option('--user', '-u', required=True, help='User with access to database')
@click.option('--password', '-p', required=True, help='Password of user with access to database')
@click.option('--host', '-h', default="127.0.0.1")
@click.option('--port', default="5432")
@click.option('--table', required=True, help='Name of table with photos')
@click.option('--aws/--no-aws', required=True)
@click.option('--img_type', required=True)
def main(num_of_photos, database, user, password, host, port, table, aws, img_type):

    # Соединяемся с базой данных
    con = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cur = con.cursor()

    if img_type == "PS":
        URL = "https://thispersondoesnotexist.com/image"
    elif img_type == "CA":
        URL = "https://thiscatdoesnotexist.com/"

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

    i = 0
    while i < num_of_photos:
        r = requests.get(URL)
        filename = get_random_filename()
        # Сохраняем фото
        print(f'Getting {i + 1}/{num_of_photos} photo... [ "{filename}" ]')
        with open(f"media/{filename}", "wb") as photo:
            photo.write(r.content)
            i += 1
        # Добавляем фото в БД
        cur.execute(
            f"INSERT INTO {table} (is_real,type,photo_url) VALUES (false, '{img_type}', '{filename}')"
        )
        con.commit()
        # Загружаем в хранилище при необходимости
        if aws:
            client.upload_file(
                f"media/{filename}",
                space_name,
                f"{dir_to_load}/{filename}",
                ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'}
            )

    con.close()


if __name__ == '__main__':
    main()
