# Сервис выполняет заявку на регистрацию багажа - лыжи

Требования к сервису:
 - stateless сервис, для разбора инцидентов логи отгружаются в ELK по http   
 - интеграции сервиса сомостоятельно проверяют информацию на дубликаты заявок, 
 т.е. данный сервис не реализует проверку копий запросов на регистрацию багажа 
 - не нужно настраивать инфраструктурные сервисы такие как nginx, будет использована общая инфраструктура проекта, раздавать статику можно приложением 
 - не нужно настраивать аутентификацию и авторизацию 
 - логи пишутся синхронно, что может повлиять на производительность сервиса или падение из-за недоступности инфраструктуры

## Поднять сервис

Поднять сервис можно в докере: 
```
docker-compose up -d
```
#### Решение проблем
На моей машине не получилось скачать образы ELK без прокси:
```
The Amazon CloudFront distribution is configured to block access from your country.
```
Lostash может пройти healthchek, но продолжать не обслуживать входящие запросы.
Нужно подождать полного запуска Lostash:
```
Successfully started Logstash API endpoint {:port=>9600}
```
## Ручное тестирование
 - описать как пройтись по всем методам в swagger

## Запустить тесты
Тесты запускаются в докере:
```
docker-compose up -d
```
Отчет о тестировании сохраняется в:
```
./
```

# TODO
- добавить views
- добавить тесты
- добавить остановку сервиса 
- добавить open api спецификацию 
- добавить описание как расследовать инциденты - ELK
- проверить typing
- проверить нагрузку 
