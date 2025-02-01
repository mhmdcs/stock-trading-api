INSERT INTO alert_rules (id, name, threshold_price, symbol)
VALUES
    (gen_random_uuid(), 'Tesla Below $800', 800, 'TSLA'),
    (gen_random_uuid(), 'Apple Above $150', 150, 'AAPL')
ON CONFLICT (name) DO NOTHING;
