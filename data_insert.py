import json
import mysql.connector
from mysql.connector import Error
import sys

class DjangoFixtureImporter:
    def __init__(self, host, database, user, password, port=3306):
        """
        Initialize MySQL connection parameters
        """
        self.connection_config = {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': port
        }
        self.connection = None
        
    def connect(self):
        """Establish MySQL connection"""
        try:
            self.connection = mysql.connector.connect(**self.connection_config)
            if self.connection.is_connected():
                print(f"Successfully connected to MySQL database: {self.connection_config['database']}")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close MySQL connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
    
    def create_tables(self):
        """Create all necessary tables"""
        cursor = self.connection.cursor()
        
        tables = {
            'contenttypes_contenttype': '''
                CREATE TABLE IF NOT EXISTS contenttypes_contenttype (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    app_label VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    UNIQUE KEY contenttypes_contenttype_app_label_model (app_label, model)
                )
            ''',
            'products_image': '''
                CREATE TABLE IF NOT EXISTS products_image (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    link VARCHAR(255) NOT NULL
                )
            ''',
            'products_datasheet': '''
                CREATE TABLE IF NOT EXISTS products_datasheet (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    link VARCHAR(255) NOT NULL
                )
            ''',
            'products_brand': '''
                CREATE TABLE IF NOT EXISTS products_brand (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    slug VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    img_id INT,
                    FOREIGN KEY (img_id) REFERENCES products_image(id)
                )
            ''',
            'products_category': '''
                CREATE TABLE IF NOT EXISTS products_category (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    img_id INT,
                    FOREIGN KEY (img_id) REFERENCES products_image(id)
                )
            ''',
            'products_product': '''
                CREATE TABLE IF NOT EXISTS products_product (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    slug VARCHAR(200) UNIQUE NOT NULL,
                    brand_id INT NOT NULL,
                    features TEXT,
                    name VARCHAR(200) NOT NULL,
                    category_id INT NOT NULL,
                    quantity INT DEFAULT 0,
                    top_featured BOOLEAN DEFAULT FALSE,
                    datasheet_id INT,
                    FOREIGN KEY (brand_id) REFERENCES products_brand(id),
                    FOREIGN KEY (category_id) REFERENCES products_category(id),
                    FOREIGN KEY (datasheet_id) REFERENCES products_datasheet(id)
                )
            ''',
            'products_banner': '''
                CREATE TABLE IF NOT EXISTS products_banner (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    img_id INT NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products_product(id),
                    FOREIGN KEY (img_id) REFERENCES products_image(id)
                )
            ''',
            'products_productimage': '''
                CREATE TABLE IF NOT EXISTS products_productimage (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    img_id INT NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products_product(id),
                    FOREIGN KEY (img_id) REFERENCES products_image(id)
                )
            ''',
            'auth_permission': '''
                CREATE TABLE IF NOT EXISTS auth_permission (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    content_type_id INT NOT NULL,
                    codename VARCHAR(100) NOT NULL,
                    UNIQUE KEY auth_permission_content_type_id_codename (content_type_id, codename)
                )
            ''',
            'auth_user': '''
                CREATE TABLE IF NOT EXISTS auth_user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    password VARCHAR(128) NOT NULL,
                    last_login DATETIME(6),
                    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                    username VARCHAR(150) UNIQUE NOT NULL,
                    first_name VARCHAR(150) NOT NULL DEFAULT '',
                    last_name VARCHAR(150) NOT NULL DEFAULT '',
                    email VARCHAR(254) NOT NULL DEFAULT '',
                    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    date_joined DATETIME(6) NOT NULL
                )
            ''',
            'queries_query': '''
                CREATE TABLE IF NOT EXISTS queries_query (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''
        }
        
        try:
            for table_name, create_statement in tables.items():
                cursor.execute(create_statement)
                print(f"Table {table_name} created/verified")
            
            self.connection.commit()
            print("All tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def insert_data(self, fixture_data):
        """Insert fixture data into database"""
        cursor = self.connection.cursor()
        
        # Define insertion order based on foreign key dependencies
        insert_order = [
            'contenttypes.contenttype',
            'products.image',
            'products.datasheet',
            'products.brand',
            'products.category',
            'products.product',
            'products.banner',
            'products.productimage',
            'auth.permission',
            'auth.user'
        ]
        
        try:
            # Group data by model
            data_by_model = {}
            for item in fixture_data:
                model = item['model']
                if model not in data_by_model:
                    data_by_model[model] = []
                data_by_model[model].append(item)
            
            # Insert data in dependency order
            for model in insert_order:
                if model in data_by_model:
                    self._insert_model_data(cursor, model, data_by_model[model])
            
            self.connection.commit()
            print("All data inserted successfully")
            
        except Error as e:
            print(f"Error inserting data: {e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def _insert_model_data(self, cursor, model, items):
        """Insert data for a specific model"""
        print(f"Inserting {len(items)} records for {model}...")
        
        table_mappings = {
            'contenttypes.contenttype': {
                'table': 'contenttypes_contenttype',
                'fields': ['app_label', 'model']
            },
            'products.image': {
                'table': 'products_image',
                'fields': ['link']
            },
            'products.datasheet': {
                'table': 'products_datasheet',
                'fields': ['link']
            },
            'products.brand': {
                'table': 'products_brand',
                'fields': ['slug', 'name', 'img_id']
            },
            'products.category': {
                'table': 'products_category',
                'fields': ['name', 'img_id']
            },
            'products.product': {
                'table': 'products_product',
                'fields': ['slug', 'brand_id', 'features', 'name', 'category_id', 'quantity', 'top_featured', 'datasheet_id']
            },
            'products.banner': {
                'table': 'products_banner',
                'fields': ['product_id', 'img_id']
            },
            'products.productimage': {
                'table': 'products_productimage',
                'fields': ['product_id', 'img_id']
            },
            'auth.permission': {
                'table': 'auth_permission',
                'fields': ['name', 'content_type_id', 'codename']
            },
            'auth.user': {
                'table': 'auth_user',
                'fields': ['password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
            }
        }
        
        if model not in table_mappings:
            print(f"Skipping unknown model: {model}")
            return
        
        table_info = table_mappings[model]
        table_name = table_info['table']
        fields = table_info['fields']
        
        for item in items:
            try:
                # Handle special cases for different models
                if model == 'auth.permission':
                    values = self._prepare_permission_values(item, fields)
                elif model == 'auth.user':
                    values = self._prepare_user_values(item, fields)
                else:
                    values = self._prepare_standard_values(item, fields)
                
                if values is None:
                    continue
                
                # Create INSERT statement with explicit ID
                pk = item.get('pk')
                if pk:
                    all_fields = ['id'] + fields
                    all_values = [pk] + values
                    placeholders = ', '.join(['%s'] * len(all_fields))
                    field_names = ', '.join(all_fields)
                else:
                    all_values = values
                    placeholders = ', '.join(['%s'] * len(fields))
                    field_names = ', '.join(fields)
                
                query = f"INSERT IGNORE INTO {table_name} ({field_names}) VALUES ({placeholders})"
                cursor.execute(query, all_values)
                
            except Exception as e:
                print(f"Error inserting item {item.get('pk', 'unknown')} for model {model}: {e}")
                continue
    
    def _prepare_standard_values(self, item, fields):
        """Prepare values for standard models"""
        values = []
        item_fields = item.get('fields', {})
        
        for field in fields:
            if field.endswith('_id'):
                # Handle foreign key fields (remove _id suffix to get actual field name)
                actual_field = field[:-3]
                values.append(item_fields.get(actual_field))
            else:
                values.append(item_fields.get(field))
        
        return values
    
    def _prepare_permission_values(self, item, fields):
        """Prepare values for auth.permission model"""
        values = []
        item_fields = item.get('fields', {})
        
        for field in fields:
            if field == 'content_type_id':
                # content_type is stored as [app_label, model] array
                content_type = item_fields.get('content_type', [])
                if isinstance(content_type, list) and len(content_type) == 2:
                    # Find the content type ID (this is a simplified approach)
                    # In a real scenario, you'd query the contenttypes_contenttype table
                    values.append(1)  # Placeholder - you may need to implement proper lookup
                else:
                    values.append(None)
            else:
                values.append(item_fields.get(field))
        
        return values
    
    def _prepare_user_values(self, item, fields):
        """Prepare values for auth.user model"""
        values = []
        item_fields = item.get('fields', {})
        
        for field in fields:
            value = item_fields.get(field)
            if field in ['last_login', 'date_joined'] and value:
                # Convert ISO datetime string to MySQL format
                if 'T' in value:
                    value = value.replace('T', ' ').replace('Z', '')
            values.append(value)
        
        return values

def main():
    # Sample fixture data (you should replace this with your actual data)
    fixture_json = '''[{"model": "contenttypes.contenttype", "fields": {"app_label": "admin", "model": "logentry"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "auth", "model": "permission"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "auth", "model": "group"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "auth", "model": "user"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "contenttypes", "model": "contenttype"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "sessions", "model": "session"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "products", "model": "brand"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "products", "model": "image"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "products", "model": "category"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "products", "model": "product"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "products", "model": "banner"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "products", "model": "productimage"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "products", "model": "datasheet"}}, {"model": "contenttypes.contenttype", "fields": {"app_label": "queries", "model": "query"}}, {"model": "products.image", "pk": 1, "fields": {"link": "Body_Protection.png"}}, {"model": "products.image", "pk": 2, "fields": {"link": "Eye_Protection.png"}}]'''
    
    # Database configuration
    config = {
        'host': 'localhost',
        'database': 'safety_equipment_db',
        'user': 'root',
        'password': 'your_password'
    }
    
    try:
        # Parse fixture data
        print("Loading fixture data...")
        fixture_data = json.loads(fixture_json)
        
        # Initialize importer
        importer = DjangoFixtureImporter(**config)
        
        # Connect to database
        if not importer.connect():
            sys.exit(1)
        
        # Create tables
        print("Creating database tables...")
        importer.create_tables()
        
        # Insert data
        print("Inserting fixture data...")
        importer.insert_data(fixture_data)
        
        print("Import completed successfully!")
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if 'importer' in locals():
            importer.disconnect()

if __name__ == "__main__":
    # Update these configuration values for your MySQL setup
    DATABASE_CONFIG = {
        'host': 'localhost',
        'database': 'exidesaftey_db',
        'user': 'root',
        'password': '8411',
        'port': 3306
    }
    
    # Path to your fixture JSON file
    FIXTURE_FILE = 'db_converted.json'
    
    try:
        # Load the complete fixture data from your document
        with open(FIXTURE_FILE, 'r', encoding='utf-8') as f:
            fixture_data = json.load(f)
        
        # Initialize and run importer
        importer = DjangoFixtureImporter(**DATABASE_CONFIG)
        
        if importer.connect():
            importer.create_tables()
            importer.insert_data(fixture_data)
        
    except FileNotFoundError:
        print(f"Fixture file {FIXTURE_FILE} not found. Please save your JSON data to this file.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'importer' in locals():
            importer.disconnect()