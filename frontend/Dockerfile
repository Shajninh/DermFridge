# Use Nginx as the base image
FROM nginx:alpine

# Remove the default Nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy your frontend files into Nginx’s default directory
COPY homepage.html /usr/share/nginx/html/index.html
COPY homepage.css /usr/share/nginx/html/homepage.css

# Expose port 80 to access via localhost
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
