# Сервис выполняет заявку на регистрацию багажа - лыжи

## [Техническое задание](https://github.com/BystriakovSemyon/baggage_order/blob/develop/readme_static/issue.pdf)

### Требования к сервису:
 - stateless сервис, для разбора инцидентов логи отгружаются в ELK по http   
 - интеграции сервиса сомостоятельно проверяют информацию на дубликаты заявок, 
 т.е. данный сервис не реализует проверку копий запросов на регистрацию багажа  
 - не нужно настраивать аутентификацию и авторизацию 
 - логи пишутся синхронно, что может повлиять на производительность сервиса или падение из-за недоступности инфраструктуры
 - для удобства тестирования заглушки добавлены методами АПИ сервиса 

### Уточнения задания:
 - в задании querystring = {"number":"AAAAAA","passengerId":"ivanov"}, passengerId - это фамилия,
  но по ответам из примеров видно что это не фамилия, а 16-ти символьная строка из литинских букв и цифр.
   Из-за противоречивой информации сервис проверяет длину строки не в 16 символов, а 255, так же проверяем что  числа быть не могут.   
 - если в ответе сервиса /orders baggagePricings->baggages есть несколько альтернативных предложений по провозу лыж, мы берем все
 - может оказаться что на каком-то из flight/route нет возможности провезти лыжи, это не является ошибкой
 - поле redemption в запросе к /bags всегда false
 - заглушки работают только для запроса querystring = {"number":"AAAAAA","passengerId":"ivanov"}, для остальных 404

 ### Для внешних зависимостей использовались следующие заглушки
<details><summary>/orders</summary>
<p>

#### Запрос
{"number":"AAAAAA","passengerId":"ivanov"}
#### Ответ
{
   "ancillariesPricings":[
      {
         "airId":"ef8ff876-9b29-448f-97ba-094898deef98",
         "baggagePricings":[
            {
               "passengerIds":[
                  "dKCLeweYNb6iDO66",
                  "qauJTpuMlDrASaty"
               ],
               "passengerTypes":[
                  "ADT"
               ],
               "purchaseType":"PAID",
               "routeId":"RyucZ4TVI1EseYCp",
               "baggages":[
                  {
                     "id":"nqNNipOwlK7i9fRr",
                     "overWeight":true,
                     "amount":1,
                     "unit":"KG",
                     "weight":{
                        "amount":50,
                        "unit":"KG"
                     },
                     "code":"0IK",
                     "descriptions":[
                        "EXCESS WEIGHT"
                     ],
                     "registered":false
                  },
                  {
                     "id":"q0YIbjcv2zSx4JGK",
                     "overWeight":false,
                     "amount":1,
                     "unit":"PC",
                     "weight":{
                        "amount":23,
                        "unit":"KG"
                     },
                     "code":"0CC",
                     "descriptions":[
                        "CHECKED BAG FIRST"
                     ],
                     "registered":false
                  },
                  {
                     "id":"KChsLeEHhHqEvGmw",
                     "overWeight":false,
                     "amount":2,
                     "unit":"PC",
                     "weight":{
                        "amount":23,
                        "unit":"KG"
                     },
                     "code":"0CD",
                     "descriptions":[
                        "CHECKED BAG SECOND"
                     ],
                     "registered":false
                  },
                  {
                     "id":"siEct88JoxGWpe5v",
                     "overWeight":false,
                     "amount":1,
                     "unit":"PC",
                     "code":"0DD",
                     "descriptions":[
                        "SNOWSKI SNOWBOARD EQUIPMENT"
                     ],
                     "registered":false,
                     "equipmentType":"ski"
                  }
               ]
            },
            {
               "passengerIds":[
                  "dKCLeweYNb6iDO66",
                  "qauJTpuMlDrASaty"
               ],
               "passengerTypes":[
                  "ADT"
               ],
               "purchaseType":"PAID",
               "routeId":"iqCrFYw8oDTwVpWD",
               "baggages":[
                  {
                     "id":"xawp8dUZHYaJqmVS",
                     "overWeight":true,
                     "amount":1,
                     "unit":"KG",
                     "weight":{
                        "amount":50,
                        "unit":"KG"
                     },
                     "code":"0IK",
                     "descriptions":[
                        "EXCESS WEIGHT"
                     ],
                     "registered":false
                  },
                  {
                     "id":"AzD5GiHPkxVruI3B",
                     "overWeight":false,
                     "amount":1,
                     "unit":"PC",
                     "weight":{
                        "amount":23,
                        "unit":"KG"
                     },
                     "code":"0CC",
                     "descriptions":[
                        "CHECKED BAG FIRST"
                     ],
                     "registered":false
                  },
                  {
                     "id":"7UPUB3KhGSI12ZXF",
                     "overWeight":false,
                     "amount":2,
                     "unit":"PC",
                     "weight":{
                        "amount":23,
                        "unit":"KG"
                     },
                     "code":"0CD",
                     "descriptions":[
                        "CHECKED BAG SECOND"
                     ],
                     "registered":false
                  },
                  {
                     "id":"CMQs0BgMVGpAJcOP",
                     "overWeight":false,
                     "amount":1,
                     "unit":"PC",
                     "code":"0DD",
                     "descriptions":[
                        "SNOW SKI SNOWBOARD EQUIPMENT"
                     ],
                     "registered":false,
                     "equipmentType":"ski"
                  }
               ]
            }
         ],
         "baggageDisabled":false,
         "seatsDisabled":false,
         "mealsDisabled":false,
         "upgradesDisabled":true,
         "loungesDisabled":false,
         "fastTracksDisabled":false,
         "petsDisabled":true
      }
   ]
}
</p>
</details>
<details><summary>/bags</summary>
<p>

#### Запрос
{
   "baggageSelections":[
      {
         "passengerId":"dKCLeweYNb6iDO66",
         "routeId":"RyucZ4TVI1EseYCp",
         "baggageIds":[
            "siEct88JoxGWpe5v"
         ],
         "redemption":false
      },
      {
         "passengerId":"dKCLeweYNb6iDO66",
         "routeId":"iqCrFYw8oDTwVpWD",
         "baggageIds":[
            "CMQs0BgMVGpAJcOP"
         ],
         "redemption":false
      },
      {
         "passengerId":"qauJTpuMlDrASaty",
         "routeId":"RyucZ4TVI1EseYCp",
         "baggageIds":[
            "siEct88JoxGWpe5v"
         ],
         "redemption":false
      },
      {
         "passengerId":"qauJTpuMlDrASaty",
         "routeId":"iqCrFYw8oDTwVpWD",
         "baggageIds":[
            "CMQs0BgMVGpAJcOP"
         ],
         "redemption":false
      }
   ]
}
#### Ответ
 (Status_code 200):
{
 "shoppingCart": {....}
}
</p>
</details>

## Поднять сервис

Основные настройки лежат в .env

Поднять сервис можно в докере: 
```
docker-compose up -d
```
#### Решение проблем
На моей машине не получилось скачать образы ELK без прокси:
```
The Amazon CloudFront distribution is configured to block access from your country.
```

## Ручное тестирование

Swagger достепен по следующему адресу
```
http://localhost:8080/swagger-ui
```
Логи смотреть в кибане.
```
http://localhost:5601/app/discover
```
При первом запуске нужно создать индекс.
<details><summary>Много скринов</summary>
<p>

![Шаг 1](https://github.com/BystriakovSemyon/baggage_order/blob/develop/readme_static/Step_1.png)
![Шаг 2](https://github.com/BystriakovSemyon/baggage_order/blob/develop/readme_static/Step_2.png)
![Шаг 3](https://github.com/BystriakovSemyon/baggage_order/blob/develop/readme_static/Step_3.png)

</p>
</details>
<details><summary>Запрос в Swagger + логи в Kibana</summary>
<p>

![Шаг 4](https://github.com/BystriakovSemyon/baggage_order/blob/develop/readme_static/Step_4.png)
![Шаг 5](https://github.com/BystriakovSemyon/baggage_order/blob/develop/readme_static/Step_6.png)

</p>
</details>

## Запустить тесты
Тесты запускаются в докере:
```
docker-compose -f docker-compose-run-tests.yml --env-file .test-env up -d
```
Отчет о тестировании сохраняется в:
```
./test_reports
```
