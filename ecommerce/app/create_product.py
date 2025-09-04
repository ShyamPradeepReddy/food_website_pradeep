from .models import Product

# Create a new Product instance
product = Product.objects.create(
    title="Buffalo Ghee",
    selling_price=500.00,
    discounted_price=450.00,
    description="Clarified butter made from buffalo milk.",
    composition="Buffalo milk cream",
    prodapp="Used in traditional dishes and remedies.",
    category="Dairy",
    product_image="path/to/buffalo_ghee.jpg"  # Ensure the image path is correct
)