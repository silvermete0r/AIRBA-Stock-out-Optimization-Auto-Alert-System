# AIRBA Technodom Stock-Out Optimization

*Team 200: AIRBA Case Championship; mr. Arman & mr. Zhassulan; March, 2025*

**🔗 Ссылка на демо:** [airba-stock-out-optimization-system.streamlit.app](https://airba-stock-out-optimization-system.streamlit.app/)

**🔗 Ссылка на short-summary:** [airba-short-summary.pdf](/AIRBA%20Case%20Championship%202025.pdf)

![image](https://github.com/user-attachments/assets/a8124b9a-60d2-4cd2-9b6f-aa5e4387859a)

![image](https://github.com/user-attachments/assets/d0a44dd9-225c-4c95-b943-1c0c80506b55)


Данная система базирована на данных полученных от LGBM time series forecasting моделей, которые описывают данные по будущему состоянию продаж товаров и количество товаров на складе делает анализ, чтобы заранее уведомлять о необходимых закупках для пополнения склада в магазинах Technodom.

1. Анализ взаимосвязи между прогнозируемыми продажами и текущими складскими остатками.
2. Сближение данных по продажам и складам с учётом временных и логистических задержек (time-lag & distance-based adjustments).
3. Автоматизация процесса закупки: при достижении заданного уровня confidence модель инициирует заказ и логистику поставки в магазин.
4. Уведомление магазинов при высокой вероятности увеличения спроса на конкретные товары — для заблаговременного пополнения запасов.

Система прогнозирует дисбаланс между остатками на складе и спросом в момент времени *t*:

$$
\Delta(t) = \text{Stocks}(t + \tau) - \text{Sales}(t)
$$

Целевая функция минимизирует ожидаемое абсолютное отклонение:

$$
\text{Цель:} \quad \min_{\tau} \; \mathbb{E}[|\Delta(t)|]
$$

### Обозначения

- **Δ(t)** — дисбаланс между прогнозируемыми остатками товара и продажами в момент времени *t*  
- **Stocks(t + τ)** — прогноз количества товара на складе через *τ* дней вперёд  
- **Sales(t)** — прогноз спроса в текущий момент времени *t*  
- **τ** — оптимальное временное смещение, при котором остатки максимально соответствуют спросу  
- **𝔼[|Δ(t)|]** — математическое ожидание абсолютной ошибки между остатками и продажами

## Data Samples

* Sales: [data/sales/](data/sales/)
* Stocks: [data/stocks/](data/stocks/)

### Technodom Stocks Data

| Date       | store_id                   | item_id                    | Quantity           |
|------------|----------------------------|----------------------------|--------------------|
| 2025-01-01 | jsySHiRm8fJNrz6IubJskA==   | jbAAUFaNLXIR6Yt2FTw+Hg==   | 2.452385727293056  |
| 2025-01-02 | jsySHiRm8fJNrz6IubJskA==   | jbAAUFaNLXIR6Yt2FTw+Hg==   | 2.405122783937093  |
| 2025-01-03 | jsySHiRm8fJNrz6IubJskA==   | jbAAUFaNLXIR6Yt2FTw+Hg==   | 2.4223353964458325 |
| 2025-01-04 | jsySHiRm8fJNrz6IubJskA==   | jbAAUFaNLXIR6Yt2FTw+Hg==   | 2.347860288832783  |
| 2025-01-05 | jsySHiRm8fJNrz6IubJskA==   | jbAAUFaNLXIR6Yt2FTw+Hg==   | 2.331904450387543  |

**Stocks Data Description**

* `Date` - текущая дата
* `store_id` - идентификатор магазина
* `item_id` - идентификатор товара
* `Quantity` - количество товара на складе

### Technodom Sales Data

| Дата       | store_id                   | grouptxt           | item_id                    | Quantity           |
|------------|----------------------------|---------------------|----------------------------|--------------------|
| 2025-01-01 | jsySHiRm8fJNrz6IubJskA==   | Стиральные машины  | jbAAUFaNLXIR6Yt2FTw+Hg==   | 1.4409293287718632 |
| 2025-01-02 | jsySHiRm8fJNrz6IubJskA==   | Стиральные машины  | jbAAUFaNLXIR6Yt2FTw+Hg==   | 1.6307553968496955 |
| 2025-01-03 | jsySHiRm8fJNrz6IubJskA==   | Стиральные машины  | jbAAUFaNLXIR6Yt2FTw+Hg==   | 1.6754884989712193 |
| 2025-01-04 | jsySHiRm8fJNrz6IubJskA==   | Стиральные машины  | jbAAUFaNLXIR6Yt2FTw+Hg==   | 1.7126000870697071 |
| 2025-01-05 | jsySHiRm8fJNrz6IubJskA==   | Стиральные машины  | jbAAUFaNLXIR6Yt2FTw+Hg==   | 1.7127691076051235 |

**Sales Data Description**

* `Дата` - текущая дата
* `store_id` - идентификатор магазина
* `grouptxt` - группа / категория товаров
* `item_id` - идентификатор товара
* `Quantity` - количество проданного (позитивное) / возвращенного (негативное) товара
