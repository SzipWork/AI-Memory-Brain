from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def save_memory(user_id: str, memory):
    with driver.session() as session:
        session.run(
            """
            MERGE (u:User {id: $uid})
            CREATE (m:Memory {
                content: $content,
                confidence: $confidence,
                importance: $importance,
                created_at: datetime($created),
                last_accessed: datetime($accessed)
            })
            MERGE (u)-[:HAS_MEMORY]->(m)
            """,
            uid=user_id,
            content=memory.content,
            confidence=memory.confidence,
            importance=memory.importance,
            created=memory.created_at.isoformat(),
            accessed=memory.last_accessed.isoformat()
        )

def get_memories(user_id: str):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $uid})-[:HAS_MEMORY]->(m:Memory)
            RETURN m.content AS content
            ORDER BY m.created_at ASC
            """,
            uid=user_id
        )
        return [r["content"] for r in result]
