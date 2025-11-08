"""Tiny runner to demonstrate PowerSource and verify imports/workflow."""

from powerSources import PowerSource


def main():
	ps = PowerSource(
		name="PSU-1",
		description="Test power source",
		type="Battery",
		pieceNumber="PN-001",
		parameters={"chemistry": "Li-ion"},
		dimensions={"length": 10, "width": 5, "height": 2},
		voltage=12.0,
		current=2.5,
	)

	info = ps.get_power_info()
	print("PowerSource info:")
	for k, v in info.items():
		print(f"{k}: {v}")


if __name__ == "__main__":
	main()
