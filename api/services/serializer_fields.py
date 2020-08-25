from rest_framework import serializers


class MinimalContentField(serializers.Field):
    def to_representation(self, value):
        if len(value) < 100:
            return value
        return '%s...' % (value[:100])

    def to_internal_value(self, data):
        return data
