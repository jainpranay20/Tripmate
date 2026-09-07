from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore


checkpointer = InMemorySaver()
travel_store = InMemoryStore()