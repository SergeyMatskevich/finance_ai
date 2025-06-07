#!/bin/bash

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
DATABASE_URL=postgresql://postgres:postgres@localhost/family_finance
APP_ENV=development
DEBUG=True
SECRET_KEY=secret
EOL
    echo ".env file created!"
fi

# Start the database using Docker Compose
echo "Starting PostgreSQL database..."
docker-compose up -d db

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 5

# Create the database
echo "Creating database..."
docker-compose exec db psql -U postgres -c "CREATE DATABASE family_finance;" || true

# Initialize the database
echo "Initializing database schema..."
python -m app.db.manage init

echo "Database setup complete! You can now run your tests."
echo "To stop the database, run: docker-compose down" 