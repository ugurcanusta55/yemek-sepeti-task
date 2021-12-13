echo "yedek yükleniyor..."
PGPASSWORD=postgres gunzip -c backup.sql.gz | psql -U postgres -d test_db
echo "yedek bitti..."