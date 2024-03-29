**Содержание**

[TOCM]


## Тестовое задание

<p>stripe.com/docs - платёжная система с подробным API и бесплатным тестовым режимом для имитации и тестирования платежей. С помощью python библиотеки stripe можно удобно создавать платежные формы разных видов, сохранять данные клиента, и реализовывать прочие платежные функции. 
<p>Мы предлагаем вам познакомиться с этой прекрасной платежной системой, реализовав простой сервер с одной html страничкой, который общается со Stripe и создает платёжные формы для товаров.
<p>Для решения нужно использовать Django. Решение бонусных задач даст вам возможность прокачаться и показать свои умения, но это не обязательно. 

## Задание
Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
•	Django Модель Item с полями (name, description, price) 
•	API с двумя методами:
<p>GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
<p>GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее  с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)

•	Пример реализации можно посмотреть в пунктах 1-3 тут
•	Залить решение на Github, описать запуск в Readme.md
•	Опубликовать свое решение чтобы его можно было быстро и легко протестировать. 
•	Решения доступные только в виде кода на Github получат низкий приоритет при проверке.

## Бонусные задачи: 
•	:fa-plus: Запуск используя Docker 
•	:fa-plus: Использование environment variables
•	:fa-plus: Просмотр Django Моделей в Django Admin панели
•	:fa-plus: Запуск приложения на удаленном сервере, доступном для тестирования
•	:fa-plus: Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
•	:fa-plus: Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
•	:fa-plus: Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
•	:fa-minus: Реализовать не Stripe Session, а Stripe Payment Intent.
##Стэк
Django, 
postgres, 
docker-compose, 
stripe,
cd/cd

## Ссылки
[Главная](http://saqartvel.store) - страница заказа Order (выбираются товары и их количество)
[Страница товара](https://saqartvel.store/item/1/) - страница отдельного товара Item
[Админ панель](https://saqartvel.store/admin/)

-------------

