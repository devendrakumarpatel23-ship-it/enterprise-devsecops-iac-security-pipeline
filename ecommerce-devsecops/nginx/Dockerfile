FROM nginx:1.25-alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy SSL certificates (should be mounted or added)
# COPY certs/ /etc/nginx/certs/

# Create log directory
RUN mkdir -p /var/log/nginx && \
    touch /var/log/nginx/access.log && \
    touch /var/log/nginx/error.log

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Run as non-root
RUN addgroup -g 1000 nginx && \
    adduser -D -u 1000 -G nginx nginx && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx

USER nginx

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
