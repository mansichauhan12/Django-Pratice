


from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
   
    name=serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=200
    )
    status=serializers.ChoiceField(
        choices=["active","inactive"]
    )

    class Meta:
        model=Product
        fields='__all__'

    def validate_price(self,value):

        if value<0:
            raise serializers.ValidationError(
                "Price cannot be negative"
            )
        return value

    
    def validate(self,data):
        status=data.get("status")
        price=data.get("price")

        if status =="inactive" and price>50000:
            raise serializers.ValidationError(
                "Inactive product cannot have price greater then 50000."
            )
        return data
            




# Important interview concept

# This:

# def validate_price(self, value):

# is called field-level validation.

# The naming convention is:

# validate_<field_name>

# So later:

# validate_name()
# validate_status()
# validate_category()

# can validate individual fields.

# Object-level validation using validate()

# This is used when validation depends on multiple fields together, not just one field.

# For example, suppose we don't allow a product to have:

# status = "inactive"
# AND
# price > 50000

# Here we need both status and price, so validate_price() alone isn't enough.

# validate_price(value)
#        ↓
# One field
#        ↓
# Field-level validation


# validate(data)
#        ↓
# Multiple fields
#        ↓
# Object-level validation

# 1. validate_price(value)
#        ↓
#    Field-level custom validation

# 2. validate(data)
#        ↓
#    Object-level validation

# 3. ChoiceField
#        ↓
#    Restrict allowed values

# 4. required=True
#        ↓
#    Field must be provided

# 5. allow_blank=False
#        ↓
#    Empty string not allowed

# 6. max_length
#        ↓
#    Limit string length