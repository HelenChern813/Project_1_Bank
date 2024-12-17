# Приложение для анализа банковских операций
Приложение для анализа транзакций, которые находятся в Excel-файле. 
Будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы

## Содержание
- [Технологии](#технологии)
- [Начало работы](src/main.py)
- [Тестирование](tests)

## Разработка
- в модуле reports.py реализована функция формирования отчета по тратам по категориям и декоратор к ней,
который записывает отчет в JSON-формате в файл
- в модуле services.py реализована функция, которая выбирает только переводы по номеру телефона и формирует JSON-ответ 
- в модуле views.py реализован функционал главной страницы: 
 1. get_hello - Вычисление текущего времени и определение
нужного вступительного сообщения 
2. info_cards - Для сбора данных о транзакциях по картам, кроме стандартного ДФ и даты,
принимает путь к самому файлу
3. top_transactions - Для сбора данных о 5 самых больших транзакции
4. get_actual_currencies_price - Возвращает список актуального курса валют
5. get_actual_stocks_price - Возвращает список актуальной стоимости акций
6. home_page - Основная функция, которая формирует JSON-ответ
7. Вспомогательные функции: actual_df_mouth - Формирование нового итерируемого объекта с транзакциями от начала месяца
convert_exchange_rate - Функция возращает актуальный курс
convert_stocks - Функция возращает JSON-объект с данными по акциям
- в модуле utils.py собраны вспомогательные функции для открытия файлов
- в модуле main.py собрана примерная реализация работы приложения с указанием комментариев по корректировке работы
### Требования
Для установки и запуска проекта, необходим [NodeJS](https://nodejs.org/) v8+.

### Установка зависимостей
Для установки зависимостей, выполните команду:
```sh
poetry update
```
или
```sh
poetry install
```

## Тестирование
Пакет tests
#### В модулях расположены тесты разработанные с помощью pytest 


### Зачем вы разработали этот проект?
Чтобы был. :)

## To do
- [x] Добавить крутое README
- [ ] Всё переписать
- [ ] ...
 