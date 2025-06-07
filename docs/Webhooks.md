# GitBucket API Documentation

## Webhooks API

### 1. List Repository Webhooks

Retrieves a list of webhooks for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/hooks`

#### Request

```
GET /api/v3/repos/:owner/:repository/hooks
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Repository not found |

##### Response Body

Returns an array of webhook objects with the following structure:

```json
[
  {
    "type": "string",
    "id": 0,
    "name": "string",
    "active": "boolean",
    "events": ["string"],
    "config": {
      "content_type": "string",
      "url": "string"
    },
    "url": "string"
  }
]
```

The `events` field contains a list of event types that the webhook is subscribed to. Possible values include:
- `push`: Any Git push to the repository
- `issues`: Activity related to issues
- `issue_comment`: Activity related to issue comments
- `pull_request`: Activity related to pull requests
- `pull_request_review_comment`: Activity related to pull request review comments
- `repository`: Activity related to repository creation, deletion, etc.
- `create`: Branch or tag creation
- `delete`: Branch or tag deletion
- `release`: Release creation, editing, or deletion

The `content_type` field in the `config` object can be either `form` or `json`.

### 2. Get a Repository Webhook

Retrieves a specific webhook for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/hooks/:id`

#### Request

```
GET /api/v3/repos/:owner/:repository/hooks/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The ID of the webhook. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Webhook or repository not found |

##### Response Body

Returns a webhook object with the same structure as in the "List Repository Webhooks" endpoint.

### 3. Create a Repository Webhook

Creates a new webhook for a repository.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/hooks`

#### Request

```
POST /api/v3/repos/:owner/:repository/hooks
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "name": "web",
  "config": {
    "url": "string",
    "content_type": "form",
    "insecure_ssl": "0",
    "secret": "string"
  },
  "events": ["push"],
  "active": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | No | The name of the webhook. Default: `web` |
| `config` | `object` | **Yes** | Configuration object for the webhook |
| `config.url` | `string` | **Yes** | The URL to which the payloads will be delivered |
| `config.content_type` | `string` | No | The content type for the payload. Can be `json` or `form`. Default: `form` |
| `config.insecure_ssl` | `string` | No | Whether to verify SSL certificates when delivering payloads. Default: `0` |
| `config.secret` | `string` | No | A secret string used to compute the HMAC hex digest value in the `X-Hub-Signature` header. Can be `null` |
| `events` | `array[string]` | No | The events the webhook should subscribe to. Default: `["push"]` |
| `active` | `boolean` | No | Whether the webhook is active. Default: `true` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Repository not found or invalid parameters |

##### Response Body

Returns the created webhook object with the same structure as in the "Get a Repository Webhook" endpoint.

### 4. Update a Repository Webhook

Updates an existing webhook for a repository.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/hooks/:id`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/hooks/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The ID of the webhook. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "name": "web",
  "config": {
    "url": "string",
    "content_type": "form",
    "insecure_ssl": "0",
    "secret": "string"
  },
  "events": ["push"],
  "add_events": ["string"],
  "remove_events": ["string"],
  "active": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | No | The name of the webhook. Default: `web` |
| `config` | `object` | No | Configuration object for the webhook. Can be `null` |
| `config.url` | `string` | No | The URL to which the payloads will be delivered |
| `config.content_type` | `string` | No | The content type for the payload. Can be `json` or `form`. Default: `form` |
| `config.insecure_ssl` | `string` | No | Whether to verify SSL certificates when delivering payloads. Default: `0` |
| `config.secret` | `string` | No | A secret string used to compute the HMAC hex digest value in the `X-Hub-Signature` header. Can be `null` |
| `events` | `array[string]` | No | The events the webhook should subscribe to. Replaces the existing events. Default: `["push"]` |
| `add_events` | `array[string]` | No | The events to add to the webhook subscription. Default: `[]` |
| `remove_events` | `array[string]` | No | The events to remove from the webhook subscription. Default: `[]` |
| `active` | `boolean` | No | Whether the webhook is active. Default: `true` |

**Note:** All fields are optional. Only specified fields will be updated.

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Webhook or repository not found |

##### Response Body

Returns the updated webhook object with the same structure as in the "Get a Repository Webhook" endpoint.

### 5. Delete a Repository Webhook

Deletes a webhook from a repository.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/hooks/:id`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/hooks/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The ID of the webhook. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 204 | Success (No Content) |
| 401 | Unauthorized |
| 404 | Webhook or repository not found |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/webhooks
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Webhook Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryWebhookControllerBase.scala`
  - API Webhook: `gitbucket/src/main/scala/gitbucket/core/api/ApiWebhook.scala`
  - Create A Repository Webhook: `gitbucket/src/main/scala/gitbucket/core/api/CreateARepositoryWebhook.scala`
