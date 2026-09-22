# =====================================================================================================
#  STAGE 2: DIRECT DATABASE (RAW psycopg2)
#  Talks straight to Postgres with raw SQL and a psycopg2 cursor — no ORM.
# =====================================================================================================

from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List

from . import schemas

app = FastAPI()


# Retry loop: keep trying to connect to Postgres until it succeeds
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='FastAPI',
            user='postgres',
            password="8106710994Amma@",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database Connection was Successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(5)


# =====================================================================================================
# GET
# =====================================================================================================

@app.get("/getAllPostsFromDB", response_model=List[schemas.Post])
def get_all_posts_from_db():
    """Retrieve all posts from Postgres database using raw psycopg2 cursor."""
    cursor.execute("""SELECT * FROM POSTS""")  # no WHERE/params here, so no SQL-injection risk in this query
    posts = cursor.fetchall()  # RealDictCursor -> list of dict-like rows

    print(posts)  # debug print; remove or replace with proper logging before production
    return posts


@app.get("/getPostFromDB/{id}", response_model=schemas.Post)
def get_post_from_db(id: int):
    """Retrieve a specific post by ID from Postgres using raw psycopg2. Returns 404 if post not found."""
    cursor.execute("""SELECT * FROM posts WHERE id =(%s)""", (id,))
    post_dict = cursor.fetchone()
    if post_dict is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not Found")

    return post_dict


# =====================================================================================================
# POST
# =====================================================================================================

@app.post("/createPostInDB", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post_in_db(post: schemas.CreatePost):
    """Create a new post in Postgres database using raw psycopg2. Returns the created post with 201 status."""
    cursor.execute(
        """ INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


# =====================================================================================================
# DELETE
# =====================================================================================================

@app.delete("/deletePostFromDB/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_from_db(id: int):
    """Delete a post from Postgres database using raw psycopg2. Returns 204 on success, 404 if post not found."""
    cursor.execute(""" DELETE from posts where id= (%s) RETURNING * """, (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)  # 204 = success, no body returned


# =====================================================================================================
# PUT
# =====================================================================================================

@app.put("/updatePostInDB/{id}", response_model=schemas.Post)
def update_post_in_db(id: int, post: schemas.UpdatePost):
    """Update an existing post in Postgres database using raw psycopg2. Returns 404 if post not found."""
    cursor.execute(
        """ UPDATE posts SET title=%s , content = %s , published=%s Where id = %s RETURNING * """,
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    return updated_post
