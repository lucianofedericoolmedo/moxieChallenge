#!/bin/bash

# List of service types
service_types=(
    "Neuromodulator"
    "HA Dermal Filler"
    "Calcium Hydroxyapatite"
    "Hyaluronidase"
    "Polymethyl methacrylate (PMMA)"
    "Poly-L Lactic Acid"
    "Chemical Peel"
    "Deoxycholic Acid"
    "Sclerotherapy"
    "PDO Threads"
    "GLP-1 Antagonists"
    "IV Therapy"
    "Vitamin Injections"
    "Peptide Therapy"
    "Ultrasound"
    "Hydrafacial"
    "SilkPeel"
    "Diamond Glow"
    "Other facial"
    "Massage"
    "Microblading"
    "Microdermabrasion"
    "Dermaplaning"
    "Teeth Whitening"
    "Waxing"
    "Other Non Medical Service"
    "Consultation"
    "Follow up"
    "Other"
)

# Loop through service types and create ServiceType instances
for service in "${service_types[@]}"; do
    python manage.py shell -c "from api.models import ServiceType; ServiceType.objects.create(name='$service')"
done
