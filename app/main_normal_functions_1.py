# =====================================================================================================
#  STAGE 1: NORMAL FUNCTIONS (IN-MEMORY LIST)
#  No database at all — posts live in a plain Python list and reset every time the app restarts.
# =====================================================================================================

from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
from typing import List

from . import schemas

app = FastAPI()


# In-memory data store (not persisted — resets every time the app restarts)
my_posts = [
    {"title": "My First Post", "content": "Content of the first post", "id": 1},
    {"title": "My Second Post", "content": "Content of the Second post", "id": 2},
    {"title": "My Third Post", "content": "Content of the Third post", "id": 3},
]


# Root health-check route
@app.get("/")
def home():
    """Health check endpoint that returns a simple greeting message."""
    return {"message": "Hello World"}


# Simple sample route
@app.get("/mohan")
def mohan1():
    """Simple welcome route for testing."""
    return {"message": "Welcome Mohan"}


# =====================================================================================================
# GET
# =====================================================================================================

# All Posts Simple way to get all posts
@app.get("/getAllPosts", response_model=List[schemas.Post])
def get_all_posts():
    """Retrieve all posts from the in-memory list."""
    return my_posts


# NOTE: this must be registered before "/getPost/{id}" or FastAPI would try to match
# "latest" as the {id} path parameter and fail int conversion
@app.get("/getPost/latest", response_model=schemas.Post)
def get_latest_post():
    """Retrieve the most recently added post from the in-memory list."""
    return my_posts[len(my_posts) - 1]  # last item in the list = most recently added post


# Helper: linear search my_posts for a matching id, used by the GET-by-id route below
def get_post(id):
    """Search in-memory post list for a post matching the given ID. Returns post dict or None if not found."""
    for post in my_posts:
        if post["id"] == id:
            return post
    return None  # no match found


@app.get("/getPost/{id}", response_model=schemas.Post)
def get_post_by_id(id: int):
    """Retrieve a specific post by ID from the in-memory list. Returns 404 if post not found."""
    post_dict = get_post(id)
    if post_dict is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not Found")

    return post_dict


# =====================================================================================================
# POST
# =====================================================================================================

@app.post("/createPost", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost):
    """Create a new post in the in-memory list with random ID. Returns the created post with 201 status."""
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return post_dict


# =====================================================================================================
# DELETE
# =====================================================================================================

# Helper: find the list index (not the id) of the post matching id, so it can be popped
def find_post_index(id):
    """Find the list index of a post by ID in the in-memory list. Returns index or None if not found."""
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    # implicit return None here if no match is found (falls through the loop)


@app.delete("/deletePost/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """Delete a post from the in-memory list. Returns 204 on success, 404 if post not found."""
    idx = find_post_index(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # 204 = success, no body returned


# =====================================================================================================
# PUT
# =====================================================================================================

@app.put("/updatePost/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.UpdatePost):
    """Update an existing post in the in-memory list. Returns 404 if post not found."""
    idx = find_post_index(id)
    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    post_dict = post.dict()
    post_dict["id"] = id  # preserve the original id (the request body's Post schema doesn't include one)
    my_posts[idx] = post_dict  # full replace of the post at that index (PUT semantics, not a partial PATCH)

    return post_dict
