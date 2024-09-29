#!/bin/bash

# Function to ask for confirmation
wait_for_confirmation() {
    while true; do
        echo "This script has been tested on Linux and it is experimental on Mac"
        echo "It also requires you to have some basic things installed already on your system"
        echo "Please check this prior to continue"
        read -p "Do you have pip, virtualenv, python3 and docker installed? (yes/no): " response
        case $response in
            [Yy]* )
                echo "You chose yes. Proceeding..."
                return 0
                ;;
            [Nn]* )
                echo "You chose no. Exiting."
                return 1
                ;;
            * )
                echo "Please answer yes or no."
                ;;
        esac
    done
}

# Call the function
if wait_for_confirmation; then
    echo "Continuing setup..."
else
    # Add your code here that should run if the user declines
    echo "Please install the prerequisites to proceed."
    exit 1
fi

# Function to check if Docker is installed
check_docker() {
    if command -v docker &> /dev/null; then
        echo "Docker is installed."
        docker --version
    else
        echo "Docker is not installed. Please install Docker to proceed."
        exit 1
    fi
}

# Check the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Operating System: Linux"
    check_docker
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Operating System: macOS"
    check_docker
else
    echo "Unsupported Operating System: $OSTYPE, this script is only for Linux or Mac"
    exit 1
fi

# Get the name of the virtual environment from the user
read -p "Enter the name for the virtual environment: " venv_name

# Check if the virtual environment already exists
if [ -d "$venv_name" ]; then
    echo "Virtual environment '$venv_name' already exists."
else
    # Create the virtual environment
    python3 -m venv "$venv_name"
    echo "Virtual environment '$venv_name' created successfully."
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source "$venv_name/bin/activate"
echo "You are now in the virtual environment '$venv_name'."

# Check for requirements.txt file
if [[ ! -f requirements.txt ]]; then
    echo "requirements.txt not found!"
    exit 1
fi

# Install the required Python packages
echo "Installing requirements..."
pip install -r requirements.txt

wait

docker compose up -d

# Check if Docker Compose is up
if ! docker compose ps | grep -q 'Up'; then
    echo "Docker Compose services are not running."
    exit 1
fi

CONTAINER_NAME="moxiechallenge-db-1"

# Function to check if the container is running
is_container_running() {
    docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null
}

# Wait until the container is running
echo "Waiting for container $CONTAINER_NAME to be up..."
while [ "$(is_container_running)" != "true" ]; do
    sleep 2
done
sleep 40
echo "Container $CONTAINER_NAME is now running!"

wait
echo "PostgreSQL is ready to use."

wait
# Run migrations
echo "Applying migrations..."
python manage.py migrate
wait

sleep 2
# Start the server
echo "Starting the server..."
echo "Now we will create a default admin superuser"
python manage.py runserver

DJANGO_MANAGE="./manage.py"  # Path to manage.py
SUPERUSER_NAME="admin"
SUPERUSER_EMAIL="admin@admin.com"
SUPERUSER_PASSWORD="admin"

# Check if the superuser already exists
if python $DJANGO_MANAGE shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(username='$SUPERUSER_NAME').exists())" | grep -q "True"; then
    echo "Superuser '$SUPERUSER_NAME' already exists."
else
    # Create the superuser
    echo "Creating superuser '$SUPERUSER_NAME'..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python $DJANGO_MANAGE shell
    echo "Superuser '$SUPERUSER_NAME' created successfully."
fi



