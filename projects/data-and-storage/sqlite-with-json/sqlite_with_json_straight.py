import json
import sqlite3

# Connect to database
conn = sqlite3.connect("gigs_json.db")
cursor = conn.cursor()

# Create simple table with JSON column
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS gigs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    reviews_json TEXT  -- All reviews stored as JSON array
)
"""
)

conn.commit()

# Create several gigs
gigs = [
    ("Professional Logo Design",),
    ("Website Development",),
    ("Social Media Marketing",),
    ("Video Editing",),
]
cursor.executemany("INSERT INTO gigs (title) VALUES (?)", gigs)

# Define reviews for each gig as JSON
# Each gig has an array of reviews from different clients

# Gig 1: Logo Design
logo_reviews = json.dumps(
    [
        {
            "client": "John Smith",
            "rating": 5,
            "comment": "Amazing logo!",
            "reply": "Thanks John!",
        },
        {
            "client": "Sarah Johnson",
            "rating": 4,
            "comment": "Good but took time",
            "reply": "We'll improve timing",
        },
        {
            "client": "Mike Wilson",
            "rating": 5,
            "comment": "Perfect design",
            "reply": "Thank you!",
        },
        {
            "client": "Emily Davis",
            "rating": 3,
            "comment": "It's okay",
            "reply": "Thanks for feedback",
        },
    ]
)

# Gig 2: Website Development
web_reviews = json.dumps(
    [
        {
            "client": "Alex Chen",
            "rating": 5,
            "comment": "Great website!",
            "reply": "Glad you liked it",
        },
        {
            "client": "Maria Garcia",
            "rating": 4,
            "comment": "Works well on mobile",
            "reply": "Thanks Maria",
        },
        {
            "client": "Tom Brown",
            "rating": 2,
            "comment": "Had some bugs",
            "reply": "We'll fix them",
        },
    ]
)

# Gig 3: Social Media Marketing
social_reviews = json.dumps(
    [
        {
            "client": "Lisa Wang",
            "rating": 5,
            "comment": "Increased followers by 50%",
            "reply": "Great results!",
        },
        {
            "client": "David Lee",
            "rating": 4,
            "comment": "Good strategy",
            "reply": "Thank you David",
        },
    ]
)

# Gig 4: Video Editing (no reviews yet)
video_reviews = json.dumps([])

# Update gigs with reviews JSON
cursor.execute(
    "UPDATE gigs SET reviews_json = ? WHERE title = ?",
    (logo_reviews, "Professional Logo Design"),
)
cursor.execute(
    "UPDATE gigs SET reviews_json = ? WHERE title = ?",
    (web_reviews, "Website Development"),
)
cursor.execute(
    "UPDATE gigs SET reviews_json = ? WHERE title = ?",
    (social_reviews, "Social Media Marketing"),
)
cursor.execute(
    "UPDATE gigs SET reviews_json = ? WHERE title = ?", (video_reviews, "Video Editing")
)

conn.commit()

# SHOW ALL DATA
print("=== ALL GIGS WITH REVIEWS ===")
cursor.execute("SELECT title, reviews_json FROM gigs")

for row in cursor.fetchall():
    title, reviews_json = row
    reviews = json.loads(reviews_json) if reviews_json else []

    print(f"\n{title}:")
    print(f"Total Reviews: {len(reviews)}")

    for review in reviews:
        print(f"  - {review['client']}: {review['rating']}/5")
        print(f"    Comment: {review['comment']}")
        print(f"    Reply: {review['reply']}")
    print("-" * 50)

# ADD A NEW REVIEW TO A GIG
print("\n=== ADDING NEW REVIEW ===")
cursor.execute(
    "SELECT reviews_json FROM gigs WHERE title = ?", ("Professional Logo Design",)
)
current_reviews_json = cursor.fetchone()[0]
current_reviews = json.loads(current_reviews_json) if current_reviews_json else []

# Add new review
new_review = {
    "client": "Robert Kim",
    "rating": 4,
    "comment": "Nice work, good communication",
    "reply": "Thanks Robert!",
}
current_reviews.append(new_review)

# Save back to database
updated_reviews_json = json.dumps(current_reviews)
cursor.execute(
    "UPDATE gigs SET reviews_json = ? WHERE title = ?",
    (updated_reviews_json, "Professional Logo Design"),
)
conn.commit()

print(f"Added review from {new_review['client']} to Logo Design gig")

# CALCULATE AVERAGE RATINGS
print("\n=== AVERAGE RATINGS ===")
cursor.execute("SELECT title, reviews_json FROM gigs")

for row in cursor.fetchall():
    title, reviews_json = row
    reviews = json.loads(reviews_json) if reviews_json else []

    if reviews:
        total_rating = sum(r["rating"] for r in reviews)
        avg_rating = total_rating / len(reviews)
        print(f"{title}: {avg_rating:.1f}/5 from {len(reviews)} clients")
    else:
        print(f"{title}: No reviews yet")

# SEARCH FOR HIGH RATED REVIEWS
print("\n=== 5-STAR REVIEWS ===")
cursor.execute("SELECT title, reviews_json FROM gigs")

for row in cursor.fetchall():
    title, reviews_json = row
    reviews = json.loads(reviews_json) if reviews_json else []

    five_star_reviews = [r for r in reviews if r["rating"] == 5]
    if five_star_reviews:
        print(f"\n{title} has {len(five_star_reviews)} 5-star reviews:")
        for review in five_star_reviews:
            print(f"  - {review['client']}: '{review['comment']}'")

# GET REVIEWS FROM SPECIFIC CLIENT
print("\n=== FIND ALL REVIEWS BY A CLIENT ===")
client_name = "Sarah Johnson"
cursor.execute("SELECT title, reviews_json FROM gigs")

print(f"Reviews by {client_name}:")
for row in cursor.fetchall():
    title, reviews_json = row
    reviews = json.loads(reviews_json) if reviews_json else []

    for review in reviews:
        if review["client"] == client_name:
            print(f"  - {title}: {review['rating']}/5 - '{review['comment']}'")

# ADD REPLY TO A REVIEW
print("\n=== ADDING REPLY TO REVIEW ===")
cursor.execute(
    "SELECT title, reviews_json FROM gigs WHERE title = ?", ("Website Development",)
)
title, reviews_json = cursor.fetchone()
reviews = json.loads(reviews_json)

# Find Tom Brown's review and add/update reply
for review in reviews:
    if review["client"] == "Tom Brown":
        review["reply"] = "All bugs have been fixed now. Thanks for your patience!"
        break

# Save updated reviews
cursor.execute(
    "UPDATE gigs SET reviews_json = ? WHERE title = ?",
    (json.dumps(reviews), "Website Development"),
)
conn.commit()
print("Updated reply for Tom Brown's review")

# SHOW FINAL STATE
print("\n=== FINAL DATA ===")
cursor.execute("SELECT title, reviews_json FROM gigs")

for row in cursor.fetchall():
    title, reviews_json = row
    reviews = json.loads(reviews_json) if reviews_json else []
    print(f"{title}: {len(reviews)} reviews")

conn.close()
