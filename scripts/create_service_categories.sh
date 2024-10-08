#!/bin/bash

# List of service categories
categories=(
    "Injectables"
    "Peels"
    "Fat Dissolving"
    "Sclerotherapy"
    "Threads"
    "Weightloss"
    "IV Therapy"
    "Vitamin Injections"
    "Peptide Therapy"
    "Ultrasound"
    "Facials"
    "Other Non Medical"
    "Consultation"
    "Follow up"
    "Other"
)

# Loop through categories and create ServiceCategory instances
for category in "${categories[@]}"; do
    python manage.py shell -c "from api.models import ServiceCategory; ServiceCategory.objects.create(name='$category')"
done
