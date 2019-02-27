rm -rf ./game_store/migrations/
rm -rf ./db.sqlite3
mkdir ./game_store/migrations/
touch ./game_store/migrations/__init__.py
python manage.py makemigrations
python manage.py migrate
echo "from game_store.models import StoreUser; StoreUser.objects.create_superuser('late', 'late@late.late', 'latelate')" | python manage.py shell