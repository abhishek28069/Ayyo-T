FROM debian:latest

# Install HAProxy
RUN apt-get update && apt-get install -y haproxy

# Copy HAProxy configuration file
COPY haproxy.cfg /etc/haproxy/haproxy.cfg

# Expose the HAProxy port
EXPOSE 80

# Run HAProxy
CMD ["haproxy", "-f", "/etc/haproxy/haproxy.cfg"]
