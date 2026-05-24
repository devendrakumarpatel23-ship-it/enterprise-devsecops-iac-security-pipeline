#!/bin/bash

# Database Backup Script
# Creates MongoDB backup with timestamp and compression

set -e

# Configuration
MONGODB_URI="${MONGODB_URI:-mongodb://admin:admin123@localhost:27017/ecommerce}"
DB_NAME="ecommerce"
BACKUP_DIR="${BACKUP_DIR:-.}/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/ecommerce_$TIMESTAMP.gz"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}MongoDB Database Backup${NC}"
echo -e "${BLUE}====================================${NC}\n"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo -e "${BLUE}Creating backup...${NC}"
echo "Database: $DB_NAME"
echo "Output: $BACKUP_FILE"

# Create backup
if mongodump --uri="$MONGODB_URI" --archive="$BACKUP_FILE" --gzip; then
    echo -e "\n${GREEN}✓ Backup created successfully${NC}"
    
    # Get file size
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "File size: $SIZE"
    
    # List recent backups
    echo -e "\n${BLUE}Recent backups:${NC}"
    ls -lhS "$BACKUP_DIR" | head -10
    
    # Cleanup old backups (keep last 30 days)
    echo -e "\n${BLUE}Cleaning up old backups (older than 30 days)...${NC}"
    find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete
    echo -e "${GREEN}✓ Cleanup completed${NC}"
    
else
    echo -e "\n${RED}✗ Backup failed${NC}"
    exit 1
fi

echo -e "\n${GREEN}====================================${NC}"
echo -e "${GREEN}Backup completed successfully!${NC}"
echo -e "${GREEN}====================================${NC}\n"
