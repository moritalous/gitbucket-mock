from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from fastapi.security import OAuth2PasswordBearer

from models.base import ApiPath
from models.webhooks import (
    ApiWebhook,
    ApiWebhookConfig,
    CreateARepositoryWebhook,
    UpdateARepositoryWebhook,
)

router = APIRouter(tags=["Webhooks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    "/repos/{owner}/{repository}/hooks",
    response_model=List[ApiWebhook],
    summary="List repository webhooks",
    description="Retrieves a list of webhooks for a repository.",
)
async def list_webhooks(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    token: str = Depends(oauth2_scheme),
) -> List[ApiWebhook]:
    """
    List webhooks for a repository.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        token: OAuth2 token

    Returns:
        List[ApiWebhook]: List of webhooks

    Raises:
        HTTPException: If repository not found
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return mock data
    return [
        ApiWebhook(
            type="web",
            id=1,
            name="web",
            active=True,
            events=["push", "pull_request"],
            config=ApiWebhookConfig(
                content_type="json",
                url="https://example.com/webhook",
            ),
            url=ApiPath(f"/api/v3/repos/{owner}/{repository}/hooks/1"),
        ),
    ]


@router.get(
    "/repos/{owner}/{repository}/hooks/{id}",
    response_model=ApiWebhook,
    summary="Get a repository webhook",
    description="Retrieves a specific webhook for a repository.",
)
async def get_webhook(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    id: int = Path(..., description="The ID of the webhook"),
    token: str = Depends(oauth2_scheme),
) -> ApiWebhook:
    """
    Get a specific webhook.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        id: The ID of the webhook
        token: OAuth2 token

    Returns:
        ApiWebhook: Webhook information

    Raises:
        HTTPException: If repository or webhook not found
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if webhook does not exist
    if id != 1:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Return mock data
    return ApiWebhook(
        type="web",
        id=1,
        name="web",
        active=True,
        events=["push", "pull_request"],
        config=ApiWebhookConfig(
            content_type="json",
            url="https://example.com/webhook",
        ),
        url=ApiPath(f"/api/v3/repos/{owner}/{repository}/hooks/1"),
    )


@router.post(
    "/repos/{owner}/{repository}/hooks",
    response_model=ApiWebhook,
    summary="Create a repository webhook",
    description="Creates a new webhook for a repository.",
)
async def create_webhook(
    webhook: CreateARepositoryWebhook,
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    token: str = Depends(oauth2_scheme),
) -> ApiWebhook:
    """
    Create a new webhook.

    Args:
        webhook: Webhook data
        owner: The owner of the repository
        repository: The name of the repository
        token: OAuth2 token

    Returns:
        ApiWebhook: Created webhook information

    Raises:
        HTTPException: If repository not found or webhook configuration is invalid
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 400 if webhook configuration is invalid
    if not webhook.is_valid():
        raise HTTPException(status_code=400, detail="Invalid webhook configuration")

    # Return mock data
    return ApiWebhook(
        type="web",
        id=1,
        name=webhook.name,
        active=webhook.active,
        events=webhook.events,
        config=ApiWebhookConfig(
            content_type=webhook.config.content_type, url=webhook.config.url
        ),
        url=ApiPath(f"/api/v3/repos/{owner}/{repository}/hooks/1"),
    )


@router.patch(
    "/repos/{owner}/{repository}/hooks/{id}",
    response_model=ApiWebhook,
    summary="Update a repository webhook",
    description="Updates an existing webhook for a repository.",
)
async def update_webhook(
    webhook: UpdateARepositoryWebhook,
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    id: int = Path(..., description="The ID of the webhook"),
    token: str = Depends(oauth2_scheme),
) -> ApiWebhook:
    """
    Update a webhook.

    Args:
        webhook: Updated webhook data
        owner: The owner of the repository
        repository: The name of the repository
        id: The ID of the webhook
        token: OAuth2 token

    Returns:
        ApiWebhook: Updated webhook information

    Raises:
        HTTPException: If repository or webhook not found, or webhook configuration is invalid
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if webhook does not exist
    if id != 1:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Return 400 if webhook configuration is invalid
    if not webhook.is_valid():
        raise HTTPException(status_code=400, detail="Invalid webhook configuration")

    # Return mock data
    return ApiWebhook(
        type="web",
        id=1,
        name=webhook.name,
        active=webhook.active,
        events=webhook.events,
        config=ApiWebhookConfig(
            content_type=webhook.config.content_type, url=webhook.config.url
        ),
        url=ApiPath(f"/api/v3/repos/{owner}/{repository}/hooks/1"),
    )


@router.delete(
    "/repos/{owner}/{repository}/hooks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a repository webhook",
    description="Deletes a webhook from a repository.",
)
async def delete_webhook(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    id: int = Path(..., description="The ID of the webhook"),
    token: str = Depends(oauth2_scheme),
) -> Response:
    """
    Delete a webhook.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        id: The ID of the webhook
        token: OAuth2 token

    Returns:
        Response: Empty response with 204 status code

    Raises:
        HTTPException: If repository or webhook not found
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if webhook does not exist
    if id != 1:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Return 204 No Content
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/repos/{owner}/{repository}/hooks/{id}/test",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Test a repository webhook",
    description="Tests a webhook by sending a ping event.",
)
async def test_webhook(
    owner: str = Path(..., description="The owner of the repository"),
    repository: str = Path(..., description="The name of the repository"),
    id: int = Path(..., description="The ID of the webhook"),
    token: str = Depends(oauth2_scheme),
) -> Response:
    """
    Test a webhook.

    Args:
        owner: The owner of the repository
        repository: The name of the repository
        id: The ID of the webhook
        token: OAuth2 token

    Returns:
        Response: Empty response with 204 status code

    Raises:
        HTTPException: If repository or webhook not found
    """
    # Return 404 if repository does not exist
    if owner == "nonexistent" or repository == "nonexistent":
        raise HTTPException(status_code=404, detail="Repository not found")

    # Return 404 if webhook does not exist
    if id != 1:
        raise HTTPException(status_code=404, detail="Webhook not found")

    # Return 204 No Content
    return Response(status_code=status.HTTP_204_NO_CONTENT)
