"""
Test Runner for AS2 Unit Tests
Runs all unit tests and generates a report
"""
import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from test_as2_send import TestAS2Send, TestAS2SendAPI, TestAS2MessageValidation
from test_as2_receive import TestAS2Receive, TestAS2ReceiveAPI, TestAS2MDN, TestAS2MessageParsing


def run_all_tests(verbosity=2):
    """
    Run all AS2 unit tests
    
    Args:
        verbosity: Level of detail in test output (0-2)
    
    Returns:
        TestResult object
    """
    print("=" * 70)
    print("AS2 Unit Test Suite")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add Send tests
    print("Loading Send tests...")
    suite.addTests(loader.loadTestsFromTestCase(TestAS2Send))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2SendAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MessageValidation))
    
    # Add Receive tests
    print("Loading Receive tests...")
    suite.addTests(loader.loadTestsFromTestCase(TestAS2Receive))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2ReceiveAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MDN))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MessageParsing))
    
    print(f"Total tests loaded: {suite.countTestCases()}")
    print()
    print("=" * 70)
    print("Running tests...")
    print("=" * 70)
    print()
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print()
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    print()
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    return result


def run_send_tests_only(verbosity=2):
    """Run only Send tests"""
    print("Running Send tests only...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAS2Send))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2SendAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MessageValidation))
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def run_receive_tests_only(verbosity=2):
    """Run only Receive tests"""
    print("Running Receive tests only...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestAS2Receive))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2ReceiveAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MDN))
    suite.addTests(loader.loadTestsFromTestCase(TestAS2MessageParsing))
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run AS2 unit tests')
    parser.add_argument('--send', action='store_true', help='Run only send tests')
    parser.add_argument('--receive', action='store_true', help='Run only receive tests')
    parser.add_argument('--verbose', '-v', action='count', default=2, help='Increase verbosity')
    
    args = parser.parse_args()
    
    if args.send:
        result = run_send_tests_only(args.verbose)
    elif args.receive:
        result = run_receive_tests_only(args.verbose)
    else:
        result = run_all_tests(args.verbose)
    
    sys.exit(0 if result.wasSuccessful() else 1)
