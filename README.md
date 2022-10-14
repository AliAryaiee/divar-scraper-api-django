
# Divar Scraper REST API with Django

This application retrieve all maximum 24 ads from Divar search result.

## Description
For each `not registered user` IP there is a limitation equal to 3 request.
For each `registered user` there is a limitation equal to 7 request.

### Parameters
- **query**: what you want to search
- **limit**: the number of results
- **has_photo**: search for ads that have image
- **urgent**: search for ads that are urgent

## Installation

Extract divar-scraper-api-django files and then run these command:

- You need Python v3.8 minimum

```bash
  virtualenv env
  env\scripts\activate
  pip install -r requirements.txt
  python manage.py runserver
```

- API will run on port 8000

```bash
  localhost:8000
```

## API Reference

#### Get Ads
- returns list of ads

```http
  POST /api/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `query` | `string` | **Required**. |
| `limit` | `integer` | **DEFAULT=24**. |
| `has_photo` | `boolean` | **DEFAULT=false**. true / false |
| `urgent` | `boolean` | **DEFAULT=false**. true / false |

#### Register

```http
  GET /auth/register
```
- returns `access` and `refresh` token after successful registration

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `mobile`      | `string` | **Required**. 09xxxxxxxxx |
| `password`      | `string` | **Required**. |

```http
  GET /auth/token
```
- returns `access` and `refresh` (Login)

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `mobile`      | `string` | **Required**. 09xxxxxxxxx |
| `password`      | `string` | **Required**. |

