# Stripe Django

Django + Stripe API для оплаты товаров.

## Сайт

https://stripe-django-production-5647.up.railway.app

## Админка

URL: https://stripe-django-production-5647.up.railway.app/admin
Логин: admin
Пароль: admin

## Эндпоинты

- `/shop/item/{id}` — страница товара с кнопкой Buy
- `/shop/buy/{id}` — получить Stripe Session для оплаты товара
- `/shop/buy/order/{id}` — получить Stripe Session для оплаты заказа
- `/shop/buy/intent/{id}` — получить Stripe Payment Intent для товара
- `/admin` — админка

## Тестовая оплата

Карта: `4242 4242 4242 4242`
Дата: любая в будущем
CVC: любые 3 цифры

## Функционал

- Модель Item (название, описание, цена, валюта)
- Модель Order (несколько товаров, общая оплата)
- Модели Discount и Tax (скидки и налоги в Stripe Checkout)
- Две валюты (USD и EUR) с разными Stripe ключами
- Stripe Checkout Session и Payment Intent
- Docker
- Django Admin
