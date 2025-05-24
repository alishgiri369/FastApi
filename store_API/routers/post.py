from fastapi import APIRouter, HTTPException

from store_API.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()


post_table = {}
comment_table = {}


def find_postid(post_id: int):
    return post_table.get(post_id)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.dict()
    last_post_id = len(post_table)
    new_post = {**data, "id": last_post_id}
    post_table[last_post_id] = new_post
    return new_post


@router.get("/post", response_model=list[UserPost])
async def return_all_post():
    return list(post_table.values())


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_postid(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No Post Found")
    data = comment.dict()
    last_comment_id = len(comment_table)
    new_comment = {**data, "id": last_comment_id}
    comment_table[last_comment_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comment(post_id: int):
    return [
        comment for comment in comment_table.values() if comment["post_id"] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_comment(post_id: int):
    post = find_postid(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No Post")

    return {
        "post": post,
        "comments": await get_comment(post_id),
    }
