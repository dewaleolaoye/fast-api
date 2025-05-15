from data import all_posts

def find_post(post_id: int):
    find_post = (post for post in all_posts if post["id"] == post_id)
    post = next(find_post, None)
    
    return post

    # for post in all_posts:
    #     if post["id"] == post_id:
    #         return post
