# Use Nginx as base image
FROM nginx:alpine

# Remove the default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy your frontend files (HTML, CSS, etc.)
COPY . /usr/share/nginx/html

# Expose port 80 (for the web browser)
EXPOSE 80
