import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_CASES_FILE = PROJECT_ROOT / "data" / "test_cases.json"


def load_test_cases():
    """
    Load LLM security test cases from the JSON test definition file.
    """

    if not TEST_CASES_FILE.exists():
        raise FileNotFoundError(
            f"Test case file was not found: {TEST_CASES_FILE}"
        )

    with TEST_CASES_FILE.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    if not isinstance(test_cases, list):
        raise ValueError(
            "Test case file must contain a JSON list."
        )

    return test_cases


if __name__ == "__main__":
    tests = load_test_cases()

    print("\nAI LLM Red-Team Test Loader")
    print("=" * 50)
    print(f"Loaded {len(tests)} test case(s).\n")

    for test in tests:
        print(f"ID:       {test.get('id')}")
        print(f"Category: {test.get('category')}")
        print(f"Name:     {test.get('name')}")
        print(f"Severity: {test.get('severity')}")
        print("-" * 50)
