import csv
import psycopg2
from dotenv import load_dotenv
import os

def import_postal_areas(csv_file_path):
    try:
        load_dotenv()

        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                region_code = row['Maakunta']
                region_name = row['Maakunnan nimi']
                municipality_code = row['Kunta']
                municipality_name = row['Kunnan nimi']
                postal_code = row['Postinumeroalue']
                postal_area_name = row['Postinumeroalueen nimi']
                
                cur.execute("""
                    INSERT INTO regions (code, name) VALUES (%s, %s)
                    ON CONFLICT (code) DO NOTHING
                """, (region_code, region_name))

                cur.execute("""
                    INSERT INTO municipalities (code, name, region_id) VALUES (%s, %s, (SELECT id FROM regions WHERE code = %s))
                    ON CONFLICT (code) DO NOTHING
                """, (municipality_code, municipality_name, region_code))

                cur.execute("""
                    INSERT INTO postal_areas (postal_code, name, municipality_code) VALUES (%s, %s, %s)
                    ON CONFLICT (postal_code) DO NOTHING
                """, (postal_code, postal_area_name, municipality_code))

        conn.commit()
        cur.close()
        conn.close()

        print("Location data imported successfully.")
        return True
    except Exception as e:
        print(f"Error importing data: {e}")
        return False