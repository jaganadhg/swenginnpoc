CREATE table userdata(
    record_id BIGINT,
    user_name VARCHAR(10),
    email_id VARCHAR(100)
);

CREATE TABLE kaggle_data (
        id BIGINT,
        timestamp TIMESTAMP, 
        instrument_token BIGINT, 
        last_price FLOAT(53), 
        volume BIGINT, 
        sell_quantity BIGINT, 
        last_quantity BIGINT, 
        change FLOAT(53), 
        "average_price" FLOAT(53), 
        "open" FLOAT(53), 
        high FLOAT(53), 
        low FLOAT(53), 
        "close" FLOAT(53), 
        "depth_buy_price_0" FLOAT(53), 
        "depth_buy_orders_0" FLOAT, 
        "depth_buy_quantity_0" FLOAT, 
        "depth_sell_price_0" FLOAT(53), 
        "depth_sell_orders_0" FLOAT, 
        "depth_sell_quantity_0" FLOAT, 
        "depth_buy_price_1" FLOAT(53), 
        "depth_buy_orders_1" FLOAT
);

