#!/bin/bash

# Database Restore Script
# Restores MongoDB from backup

set -e

# Configuration
MONGODB_URI="${MONGODB_URI:-mongodb://admin:admin123@localhost:27017/ecommerce}"
BACKUP_FILE="${1:-.}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}====================================${NC}"
echo -e "${BLUE}MongoDB Database Restore${NC}"
echo -e "${BLUE}====================================${NC}\n"

# Check if backup file is provided
if [ "$BACKUP_FILE" == "." ]; then
    echo -e "${RED}Error: Backup file not specified${NC}"
    echo "Usage: $0 <backup-file>"
    echo "Example: $0 ./backups/ecommerce_20240515_100000.gz"
    exit 1
fi

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

echo -e "${YELLOW}⚠ WARNING: This will overwrite the database!${NC}"
echo "Backup file: $BACKUP_FILE"
read -p "Continue? (y/n) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Restore cancelled${NC}"
    exit 0
fi

echo -e "\n${BLUE}Starting restore...${NC}"

# Restore backup
if mongorestore --uri="$MONGODB_URI" --archive="$BACKUP_FILE" --gzip --drop; then
    echo -e "\n${GREEN}✓ Restore completed successfully${NC}"
else
    echo -e "\n${RED}✗ Restore failed${NC}"
    exit 1
fi

echo -e "\n${GREEN}====================================${NC}"
echo -e "${GREEN}Database restored!${NC}"
echo -e "${GREEN}====================================${NC}\n"
