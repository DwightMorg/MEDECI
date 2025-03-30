# test_memory_manager.py
import pytest
import json
import os
from memory_manager import MemoryManager
from google.cloud import aiplatform

# Mock Vertex AI Matching Engine components
class MockMatchingEngineIndexEndpoint:
    def __init__(self, index_endpoint_name):
        pass

    def deploy_index(self, deployed_index_id):
        pass

    def upsert_datapoints(self, datapoints):
        pass

# Mock Vertex AI TextEmbeddingModel
class MockTextEmbeddingModel:
    def __init__(self, model_name):
        pass

    def get_embeddings(self, texts):
        # Return a fixed vector for testing
        return [aiplatform.TextEmbeddingModel.Embedding(values=[0.1, 0.2, 0.3])]

@pytest.fixture
def memory_manager(tmp_path, monkeypatch):
    # Mock aiplatform.MatchingEngineIndexEndpoint and aiplatform.TextEmbeddingModel
    monkeypatch.setattr(aiplatform, "MatchingEngineIndexEndpoint", MockMatchingEngineIndexEndpoint)
    monkeypatch.setattr(aiplatform, "TextEmbeddingModel", MockTextEmbeddingModel)

    base_dir = str(tmp_path)
    return MemoryManager(base_dir=base_dir, project="test-project", location="test-location", index_endpoint_name="test-endpoint")

def test_save_conversation_entry(memory_manager):
    user_id = "user1"
    session_id = "session1"
    entry_id = "1"
    content = "Test message"
    role = "user"

    memory_manager.save_conversation_entry(user_id, session_id, entry_id, content, role)

    path = memory_manager._get_conversation_path(user_id, session_id)
    with open(path, "r") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["content"] == content
        assert data[0]["role"] == role

def test_load_conversation(memory_manager):
    user_id = "user1"
    session_id = "session1"
    entry_id = "1"
    content = "Test message"
    role = "user"

    memory_manager.save_conversation_entry(user_id, session_id, entry_id, content, role)
    loaded_conversation = memory_manager.load_conversation(user_id, session_id)

    assert len(loaded_conversation) == 1
    assert loaded_conversation[0]["content"] == content
    assert loaded_conversation[0]["role"] == role

def test_save_summary(memory_manager):
    user_id = "user1"
    session_id = "session1"
    summary_id = "1"
    summary = "Test summary"

    memory_manager.save_summary(user_id, session_id, summary_id, summary)

    path = memory_manager._get_summary_path(user_id, session_id, summary_id)
    with open(path, "r") as f:
        data = json.load(f)
        assert data["summary"] == summary

def test_load_summary(memory_manager):
    user_id = "user1"
    session_id = "session1"
    summary_id = "1"
    summary = "Test summary"

    memory_manager.save_summary(user_id, session_id, summary_id, summary)
    loaded_summary = memory_manager.load_summary(user_id, session_id, summary_id)

    assert loaded_summary["summary"] == summary