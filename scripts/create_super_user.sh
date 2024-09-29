#!/bin/bash

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
