import sqlite3

# Super simple version
conn = sqlite3.connect("simple_gigs.db")
cursor = conn.cursor()

# Just one table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gig_title TEXT,
    client_name TEXT,
    rating INTEGER,
    comment TEXT,
    reply TEXT
)
"""
)

# Add multiple reviews from different clients for the same gig
reviews = [
    ("Logo Design", "Alice", 5, "Great work!", "Thank you!"),
    ("Logo Design", "Bob", 4, "Good but slow", "Sorry, we'll improve"),
    ("Logo Design", "Charlie", 5, "Perfect!", "Thanks Charlie!"),
    ("Logo Design", "Diana", 3, "It's okay", "We appreciate feedback"),
    ("Web Development", "Alice", 4, "Nice website", "Glad you liked it!"),
]

cursor.executemany(
    """
INSERT INTO reviews (gig_title, client_name, rating, comment, reply)
VALUES (?, ?, ?, ?, ?)
""",
    reviews,
)

conn.commit()

# Show all reviews for "Logo Design"
print("=== ALL REVIEWS FOR LOGO DESIGN ===")
cursor.execute(
    """
SELECT client_name, rating, comment, reply 
FROM reviews 
WHERE gig_title = 'Logo Design'
ORDER BY rating DESC
"""
)

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}/5 stars")
    print(f"Comment: {row[2]}")
    if row[3]:
        print(f"Reply: {row[3]}")
    print()

# Show average rating
cursor.execute(
    """
SELECT gig_title, AVG(rating), COUNT(*)
FROM reviews 
GROUP BY gig_title
"""
)

print("\n=== SUMMARY ===")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]:.1f}/5 from {row[2]} clients")

conn.close()
