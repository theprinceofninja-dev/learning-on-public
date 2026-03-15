import json
import os
import sqlite3

# Connect to database
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "gig_reviews.db"))
cursor = conn.cursor()

# Create simple tables
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS gigs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gig_id INTEGER,
    client_id INTEGER,
    rating INTEGER,
    comment TEXT,
    reply TEXT,
    FOREIGN KEY (gig_id) REFERENCES gigs(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
)
"""
)

conn.commit()

# Insert sample data
# Add a gig
cursor.execute("INSERT INTO gigs (title) VALUES (?)", ("Logo Design Service",))
gig_id = cursor.lastrowid

# Add multiple clients
clients = [("John Smith",), ("Sarah Johnson",), ("Mike Wilson",), ("Emily Davis",)]
cursor.executemany("INSERT INTO clients (name) VALUES (?)", clients)

# Get client IDs
cursor.execute("SELECT id, name FROM clients")
clients_data = cursor.fetchall()
client_ids = {name: id for id, name in clients_data}

# Multiple clients add reviews to the same gig
reviews = [
    (
        gig_id,
        client_ids["John Smith"],
        5,
        "Excellent work! Very professional.",
        "Thanks John!",
    ),
    (
        gig_id,
        client_ids["Sarah Johnson"],
        4,
        "Good quality, but delivery was late.",
        "Sorry about that, we'll improve!",
    ),
    (
        gig_id,
        client_ids["Mike Wilson"],
        5,
        "Perfect! Will hire again.",
        "Thank you Mike!",
    ),
    (
        gig_id,
        client_ids["Emily Davis"],
        3,
        "Average work. Could be better.",
        "We appreciate your feedback.",
    ),
]

cursor.executemany(
    """
INSERT INTO reviews (gig_id, client_id, rating, comment, reply) 
VALUES (?, ?, ?, ?, ?)
""",
    reviews,
)

conn.commit()

# Query: Get all reviews for a gig
print("=== ALL REVIEWS FOR GIG ===")
cursor.execute(
    """
SELECT 
    c.name as client_name,
    r.rating,
    r.comment,
    r.reply
FROM reviews r
JOIN clients c ON r.client_id = c.id
WHERE r.gig_id = ?
ORDER BY r.rating DESC
""",
    (gig_id,),
)

for row in cursor.fetchall():
    print(f"Client: {row[0]}")
    print(f"Rating: {row[1]}/5")
    print(f"Comment: {row[2]}")
    print(f"Reply: {row[3]}")
    print("-" * 40)

# Query: Get average rating
cursor.execute(
    """
SELECT 
    g.title,
    AVG(r.rating) as avg_rating,
    COUNT(r.id) as review_count
FROM gigs g
LEFT JOIN reviews r ON g.id = r.gig_id
WHERE g.id = ?
GROUP BY g.id
""",
    (gig_id,),
)

result = cursor.fetchone()
print(f"\n=== GIG SUMMARY ===")
print(f"Gig: {result[0]}")
print(f"Average Rating: {result[1]:.1f}/5 from {result[2]} clients")

# Query: Get a specific client's reviews
client_name = "Sarah Johnson"
print(f"\n=== {client_name}'S REVIEW ===")
cursor.execute(
    """
SELECT 
    g.title,
    r.rating,
    r.comment,
    r.reply
FROM reviews r
JOIN clients c ON r.client_id = c.id
JOIN gigs g ON r.gig_id = g.id
WHERE c.name = ?
""",
    (client_name,),
)

for row in cursor.fetchall():
    print(f"Gig: {row[0]}")
    print(f"Rating: {row[1]}/5")
    print(f"Comment: {row[2]}")
    print(f"Reply: {row[3]}")

# Add another review from existing client
print("\n=== ADDING NEW REVIEW ===")
cursor.execute(
    """
INSERT INTO reviews (gig_id, client_id, rating, comment) 
VALUES (?, ?, ?, ?)
""",
    (gig_id, client_ids["John Smith"], 5, "Second order! Still amazing."),
)

conn.commit()

# Show all reviews including the new one
print("\n=== UPDATED REVIEW LIST ===")
cursor.execute(
    """
SELECT 
    c.name as client_name,
    r.rating,
    r.comment,
    r.reply
FROM reviews r
JOIN clients c ON r.client_id = c.id
WHERE r.gig_id = ?
ORDER BY r.rating DESC
""",
    (gig_id,),
)

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}/5 - '{row[2]}'")

conn.close()
