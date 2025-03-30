import json
import os
from datetime import datetime
from google.cloud import aiplatform

class MemoryManager:
    def __init__(self, base_dir="local_storage", project="your-gcp-project", location="your-gcp-location", index_endpoint_name="YOUR_INDEX_ENDPOINT_NAME"):
        self.base_dir = base_dir
        self.conversations_dir = os.path.join(base_dir, "conversations")
        self.summaries_dir = os.path.join(base_dir, "summaries")
        os.makedirs(self.conversations_dir, exist_ok=True)
        os.makedirs(self.summaries_dir, exist_ok=True)
        self.project = project
        self.location = location
        aiplatform.init(project=self.project, location=self.location)
        self.index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name)

    def _get_conversation_path(self, user_id, session_id):
        return os.path.join(self.conversations_dir, f"user_{user_id}_session_{session_id}.json")

    def _get_summary_path(self, user_id, session_id, summary_id):
        return os.path.join(self.summaries_dir, f"user_{user_id}_session_{session_id}_summary_{summary_id}.json")

    def generate_embeddings(self, text):
        model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@001") # or textembedding-gecko@002
        embeddings = model.get_embeddings([text])
        return embeddings[0].values

    def save_conversation_entry(self, user_id, session_id, entry_id, content, role):
        path = self._get_conversation_path(user_id, session_id)
        content_vector = self.generate_embeddings(content)  # Generate embeddings
        entry = {
            "id": entry_id,
            "userId": user_id,
            "sessionId": session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "content": content,
            "contentVector": content_vector,
            "role": role,
        }
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []
        data.append(entry)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        # Matching Engine integration
        self.index_endpoint.deploy_index(deployed_index_id="conversation_vectors")
        self.index_endpoint.upsert_datapoints(
            datapoints=[
                aiplatform.MatchingEngineIndexEndpoint.UpsertDatapointsSpec(
                    datapoint_id=f"user_{user_id}_session_{session_id}_entry_{entry_id}",
                    feature_vector=content_vector,
                )
            ]
        )

    def load_conversation(self, user_id, session_id):
        path = self._get_conversation_path(user_id, session_id)
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_summary(self, user_id, session_id, summary_id, summary):
        path = self._get_summary_path(user_id, session_id, summary_id)
        summary_data = {
            "userId": user_id,
            "sessionId": session_id,
            "summaryId": summary_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": summary,
        }
        with open(path, "w") as f:
            json.dump(summary_data, f, indent=2)

    def load_summary(self, user_id, session_id, summary_id):
        path = self._get_summary_path(user_id, session_id, summary_id)
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None