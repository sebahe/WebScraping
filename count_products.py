from main import get_grouped_products

grouped = get_grouped_products()
total = 0
for cat in grouped:
    for sub in grouped[cat]:
        total += len(grouped[cat][sub])

print(f"Total products: {total}")
