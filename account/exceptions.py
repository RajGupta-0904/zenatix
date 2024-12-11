from rest_framework.exceptions import APIException
from rest_framework import status

class BlogPostNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Blog post not found.'
    default_code = 'blog_post_not_found'

class CategoryNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Category not found.'
    default_code = 'category_not_found'

class UnauthorizedAccess(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'unauthorized_access'

class InvalidBlogData(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid blog post data.'
    default_code = 'invalid_blog_data' 