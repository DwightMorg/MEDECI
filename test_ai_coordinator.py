import pytest
from ai_coordinator import AICoordinator
import os  # Add this line

class MockModule:
    def handle_message(self, message, context):
        return f"MockModule processed: {message['content']}"

def test_module_registration():
    coordinator = AICoordinator()
    mock_module = MockModule()
    coordinator.register_module("mock", mock_module)
    assert "mock" in coordinator.modules
    assert coordinator.modules["mock"] == mock_module

def test_route_message_success():
    coordinator = AICoordinator()
    mock_module = MockModule()
    coordinator.register_module("mock", mock_module)
    message = {"target_module": "mock", "content": "test message"}
    response = coordinator.route_message(message)
    assert response == "MockModule processed: test message"

def test_route_message_module_not_found():
    coordinator = AICoordinator()
    message = {"target_module": "nonexistent", "content": "test message"}
    response = coordinator.route_message(message)
    assert response is None

def test_route_message_module_exception():
    coordinator = AICoordinator()
    class ExceptionModule:
        def handle_message(self, message, context):
            raise ValueError("Test exception")
    exception_module = ExceptionModule()
    coordinator.register_module("exception", exception_module)
    message = {"target_module": "exception", "content": "test message"}
    response = coordinator.route_message(message)
    assert response is None

def test_set_get_context():
    coordinator = AICoordinator()
    coordinator.set_context("test_key", "test_value")
    assert coordinator.get_context("test_key") == "test_value"
    assert coordinator.get_context("nonexistent_key", "default") == "default"

def test_load_config():
    coordinator = AICoordinator()
    os.environ["TEST_CONFIG"] = "config_value"
    config_value = coordinator.load_config("TEST_CONFIG")
    assert config_value == "config_value"
    assert coordinator.load_config("NON_EXISTENT") == None
    assert coordinator.load_config("NON_EXISTENT", "default") == "default"