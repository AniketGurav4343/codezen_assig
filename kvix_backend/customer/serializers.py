from rest_framework import serializers
from customer.models import *
from common import messages

class CustomerGlobalSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerGlobal
        fields = ('first_name','last_name','gender','address_line_1','address_line_2','city','state','pincode','mobile_number','alternate_mobile_number','email')

class CustomerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUser
        fields = ('customer_global','first_name','last_name','gender','address_line_1','address_line_2','city','state','pincode','mobile_number','alternate_mobile_number','email')
          

class CustomerProfilePictureSerializer(serializers.Serializer):
   
    customer_id = serializers.IntegerField(required=True)
    profile_image = serializers.FileField(required=True)

    def validate_customer_id(self,customer_id):
        if customer_id is not None:
            application = CustomerUser.objects.filter(id=customer_id,is_deleted=False).order_by('-created_at')

            if application.exists():
                return customer_id
            else:
                raise serializers.ValidationError(messages.INVALID_CUSTOMER_ID)
        else:
            raise serializers.ValidationError(messages.INVALID_CUSTOMER_ID)


    def validate_profile_image(self,profile_image):
        if profile_image.size > 0:
            return profile_image
        else:
            raise serializers.ValidationError(messages.EMPTY_DOCUMENT)
    
    def create(self, validated_data):
        return CustomerProfilePicture.objects.create(**validated_data)