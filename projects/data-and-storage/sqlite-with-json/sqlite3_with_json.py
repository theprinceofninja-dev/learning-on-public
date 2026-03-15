import json
import os
import sqlite3


# Simple version without classes
def setup_simple_db():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "simple_gigs.db"))
    cursor = conn.cursor()

    # Create table with JSON column
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS gig_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gig_title TEXT NOT NULL,
            review_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Insert sample review with JSON
    review_data = {
        "client": "Alice Johnson",
        "rating": 5,
        "comment": "Excellent service!",
        "provider_reply": "Thank you Alice!",
    }

    cursor.execute(
        """
        INSERT INTO gig_reviews (gig_title, review_json)
        VALUES (?, ?)
    """,
        ("Web Development Service", json.dumps(review_data)),
    )

    conn.commit()

    # Query and parse JSON
    cursor.execute("SELECT gig_title, review_json FROM gig_reviews")
    for row in cursor.fetchall():
        title, review_json = row
        review = json.loads(review_json)
        print(f"Gig: {title}")
        print(f"Client: {review['client']}")
        print(f"Rating: {review['rating']}/5")
        print(f"Comment: {review['comment']}")
        print(f"Reply: {review['provider_reply']}")

    conn.close()


# Run the simple version
setup_simple_db()
