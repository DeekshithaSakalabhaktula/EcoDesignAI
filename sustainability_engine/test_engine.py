from filter_engine import filter_materials

# Test Case 1
print("Low Budget + Eco Priority")
results = filter_materials(budget="low", eco_priority=True)

for r in results:
    print(r)

print("\nMedium Budget without Eco Priority")
results = filter_materials(budget="medium", eco_priority=False)

for r in results:
    print(r)
