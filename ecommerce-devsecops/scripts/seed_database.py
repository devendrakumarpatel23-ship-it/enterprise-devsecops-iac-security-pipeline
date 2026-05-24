#!/usr/bin/env python3
"""
Database seed script for ecommerce application.
Populates MongoDB with initial data.
"""

import pymongo
from datetime import datetime
import os

# Connection settings
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://admin:admin123@localhost:27017/ecommerce')
DB_NAME = 'ecommerce'

def connect_db():
    """Connect to MongoDB"""
    client = pymongo.MongoClient(MONGODB_URI)
    return client[DB_NAME]

def seed_users(db):
    """Seed users collection"""
    users_collection = db['users']
    
    users = [
        {
            'email': 'admin@example.com',
            'password_hash': 'hashed_password_here',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'email': 'user@example.com',
            'password_hash': 'hashed_password_here',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'user',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'email': 'user2@example.com',
            'password_hash': 'hashed_password_here',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'user',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
    ]
    
    users_collection.insert_many(users)
    print(f"✓ Inserted {len(users)} users")

def seed_products(db):
    """Seed products collection"""
    products_collection = db['products']
    
    products = [
        {
            'name': 'Laptop Pro',
            'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
            'category': 'electronics',
            'price': 1299.99,
            'stock': 50,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'name': 'Wireless Mouse',
            'description': 'Ergonomic wireless mouse with 2.4GHz connection',
            'category': 'accessories',
            'price': 29.99,
            'stock': 200,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'name': 'USB-C Hub',
            'description': 'Multi-port USB-C hub with 4K display support',
            'category': 'accessories',
            'price': 79.99,
            'stock': 150,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'name': 'Mechanical Keyboard',
            'description': 'RGB mechanical keyboard with Cherry MX switches',
            'category': 'accessories',
            'price': 149.99,
            'stock': 100,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'name': '4K Monitor',
            'description': '27-inch 4K IPS monitor with USB-C and HDR support',
            'category': 'electronics',
            'price': 599.99,
            'stock': 30,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
    ]
    
    products_collection.insert_many(products)
    print(f"✓ Inserted {len(products)} products")

def create_indexes(db):
    """Create database indexes"""
    # Users indexes
    db['users'].create_index('email', unique=True)
    db['users'].create_index('role')
    
    # Products indexes
    db['products'].create_index('category')
    db['products'].create_index('price')
    db['products'].create_index('created_at', background=True)
    
    # Orders indexes
    db['orders'].create_index('user_id')
    db['orders'].create_index('status')
    db['orders'].create_index([('created_at', -1)], background=True)
    
    print("✓ Created database indexes")

def main():
    """Main function to run all seeds"""
    print("Starting database seed...")
    
    try:
        db = connect_db()
        
        # Clear existing data (optional)
        print("\nClearing existing data...")
        db['users'].delete_many({})
        db['products'].delete_many({})
        db['orders'].delete_many({})
        
        # Seed data
        print("\nSeeding data...")
        seed_users(db)
        seed_products(db)
        
        # Create indexes
        print("\nCreating indexes...")
        create_indexes(db)
        
        print("\n✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        raise

if __name__ == '__main__':
    main()
