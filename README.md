# Пример локального запуска

### Выкачиваем образ Python версии 3.10
> Откуда взял образ: https://hub.docker.com/_/python
```shell
docker pull python:3.10-slim
```
### Собираем образ со скриптом
> Пояснение ключевых моментов:
>- -t, --tag stringArray   Name and optionally a tag (format: "name:tag")

```shell
docker build -t blackbox .
```
### Запуск контейнера
> Пояснение ключевых моментов:
>- -i (интерактивный режим) позволяет оставлять стандартный ввод открытым, чтобы можно было отправлять данные в контейнер.
>- -t создает TTY (виртуальный терминал), который требуется для корректного отображения и ввода данных в консоли.
```shell
docker run -it blackbox
```