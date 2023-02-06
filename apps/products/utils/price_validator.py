from datetime import timedelta


class PriceValidator:
    def __init__(self, serializer, queryset):
        self.serializer = serializer
        self.validated_data = serializer.validated_data
        self.queryset = queryset

    def get_existing_price_query(self, process_date):
        """Get already existing prices for submitted dates."""
        prices = self.queryset.filter(
            start_date__lt=process_date,
            end_date__gt=process_date).first()
        return prices

    def update_date_intervals(self, start_date_query, end_date_query):
        """Update date intervals for dates that persist within current dates."""
        if start_date_query:
            start_date_query.end_date = self.validated_data.get('start_date') - timedelta(days=1)
            start_date_query.save()
        if end_date_query:
            end_date_query.start_date = self.validated_data.get('end_date') + timedelta(days=1)
            end_date_query.save()

    def clear_existing_range(self):
        """Clears outdated prices within submitted dates."""
        self.queryset.filter(
            start_date__gte=self.validated_data.get('start_date'),
            end_date__lte=self.validated_data.get('end_date')
        ).delete()

    def validate_save_data(self):
        if self.queryset:
            self.update_date_intervals(
                start_date_query=self.get_existing_price_query(self.validated_data.get('start_date')),
                end_date_query=self.get_existing_price_query(self.validated_data.get('end_date'))
            )
        self.serializer.save()

    def insert_price(self):
        self.queryset = self.queryset.filter(product=self.validated_data.get('product')).order_by('start_date')
        if not self.queryset:
            self.serializer.save()
        else:
            self.clear_existing_range()
            self.validate_save_data()
