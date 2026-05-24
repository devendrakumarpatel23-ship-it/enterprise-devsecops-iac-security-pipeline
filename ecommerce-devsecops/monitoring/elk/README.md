# ELK Stack Configuration

This directory contains the Elasticsearch, Logstash, and Kibana (ELK) stack configuration for centralized logging.

## 📊 Components

### Elasticsearch
- **Port:** 9200
- **Purpose:** Log storage and indexing
- **Configuration:** `elasticsearch/elasticsearch.yml`

### Kibana
- **Port:** 5601
- **Purpose:** Log visualization and analysis
- **URL:** http://localhost:5601
- **Configuration:** `kibana/kibana.yml`

### Logstash
- **Port:** 5000
- **Purpose:** Log processing and forwarding
- **Configuration:** `logstash/pipeline/logstash.conf`

## 🚀 Quick Start

### Start ELK Stack

```bash
# Using Docker Compose (recommended)
cd monitoring/elk
docker-compose up -d

# Or use main docker-compose
cd ../../
docker-compose up -d elasticsearch kibana logstash
```

### Access Kibana

1. Open http://localhost:5601
2. Create index pattern: `*-logs-*`
3. Start exploring logs

## 📝 Log Types

Logstash is configured to handle:

1. **Application Logs** (type: `application_logs`)
   - Index: `application-logs-YYYY.MM.dd`
   - Sources: Backend application logs

2. **Security Logs** (type: `security_logs`)
   - Index: `security-logs-YYYY.MM.dd`
   - Sources: Failed logins, unauthorized access

3. **Audit Logs** (type: `audit_logs`)
   - Index: `audit-logs-YYYY.MM.dd`
   - Sources: User actions, changes

## 🔧 Configuration

### Sending Logs to Logstash

```python
import logging
import json
import socket

# Configure Python logging to send to Logstash
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(json.dumps({
    'timestamp': '%(asctime)s',
    'level': '%(levelname)s',
    'message': '%(message)s',
    'type': 'application_logs'
})))

logger = logging.getLogger()
logger.addHandler(handler)
```

### Modifying Logstash Pipeline

Edit `logstash/pipeline/logstash.conf` to:
- Add new input sources
- Modify filters
- Change output destinations

After editing, restart Logstash:
```bash
docker-compose restart logstash
```

## 💾 Data Retention

- **Default:** 7 days
- **Configure:** Edit `monitoring/elk/logstash/pipeline/logstash.conf`

```conf
delete {
  where => '[%{+YYYY.MM.dd}]' < '[{{retention_days}}]'
}
```

## 🔍 Common Queries

### Find Failed Logins
```
type: "security_logs" AND message: "failed"
```

### High Error Rate
```
type: "application_logs" AND level: "ERROR"
```

### API Performance
```
type: "application_logs" AND endpoint: "/api/*"
```

## 🚨 Troubleshooting

### Elasticsearch Won't Start

```bash
# Check logs
docker-compose logs elasticsearch

# Increase max_map_count (Linux)
sysctl -w vm.max_map_count=262144
```

### No Logs in Kibana

1. Verify Logstash is running: `docker-compose ps`
2. Check Logstash logs: `docker-compose logs logstash`
3. Verify index pattern in Kibana settings
4. Check logs are being sent to port 5000

### High Memory Usage

Edit `elasticsearch/elasticsearch.yml`:
```yaml
ES_JAVA_OPTS=-Xms256m -Xmx256m
```

## 📚 Documentation

- [Elasticsearch Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Kibana Docs](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Logstash Docs](https://www.elastic.co/guide/en/logstash/current/index.html)

## 🔐 Security Notes

This configuration has security disabled (`xpack.security.enabled=false`) for development. For production:

1. Enable X-Pack security
2. Set strong passwords
3. Use SSL/TLS
4. Restrict network access
5. Regular backups

## 📊 Monitoring ELK Stack

Check cluster health:
```bash
curl http://localhost:9200/_cluster/health?pretty
```

List indices:
```bash
curl http://localhost:9200/_cat/indices?v
```

Get Logstash stats:
```bash
curl http://localhost:9600/_stats
```

---

**Last Updated:** May 2024
