# Synchronisation S3

Auteure : Anna-Rose Lescure

## Prérequis
Version de python utilisée : Python 3.8

Au besoin, installer **boto3** avec : `pip install boto3`

## Tester le script

Afin de tester le script, on prendra soin de déployer un serveur S3 tel que Minio, selon les suggestions de l'énoncé, ie :

`docker run -it -e MINIO_ACCESS_KEY=minio -e MINIO_SECRET_KEY=miniokey minio/minio server /data`

Le serveur est disponible à l'adresse **http://172.17.0.2:9000**, qui est spécifiée dans le script. Au besoin, la changer à la ligne 72 de `main.py`.

Ensuite, créer un dossier de test, `test`, et y copier un dossier ayant des sous-dossiers (par exemple, des notes de cours). Enfin, pour tester le script de synchronisation, on utilisera :

`python main.py test test`

On peut notamment utiliser l'interface graphique à l'adresse du server Minio pour vérifier qu'un bucket `test` est bien créé et le contenu du dossier local y est ajouté, qu'en supprimant un fichier du dossier local `test`, la synchronisation le supprime du bucket, et qu'on ne met à jour un objet du bucket que si sa version locale a été modifiée depuis la dernière synchronisation.