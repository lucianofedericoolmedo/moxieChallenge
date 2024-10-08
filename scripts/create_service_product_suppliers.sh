#!/bin/bash

service_products_suppliers=(
    "Allergan"
    "Revance"
    "Galderma"
    "Evolus"
    "Merz"
    "Prollenium"
    "Suneva"
    "WiQo"
    "VI"
    "Zo Skin Health"
    "Bella Medical Products"
    "Asclera"
    "Mint"
    "Miracu"
    "PDO Max"
    "V Soft Lift"
    "Viola Threads"
    "NovaThreads"
    "EuroThreads"
    "Other"
)


# Loop through service products and create ServiceProductSupplier instances
for product in "${service_products_suppliers[@]}"; do
    python manage.py shell -c "from api.models import ServiceProductSupplier; ServiceProductSupplier.objects.create(name='$product')"
done
