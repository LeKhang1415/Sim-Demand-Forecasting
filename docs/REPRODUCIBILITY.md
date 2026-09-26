# Tái lập — chờ pipeline sản phẩm

Hiện chỉ có script kiểm chứng trong `review_work/`. Khi triển khai, bổ sung lệnh cài/chạy thực và artifact tương ứng:

1. Checksum orders, môi trường/thư viện và seed.
2. Contract **v0.3**: quantity success/order_date UTC, cửa sổ 01/01/2024–31/12/2025, grain tuyến × SKU và catalog tại origin.
3. Đối soát 100.000 đơn, 93.104 success, **118.296 đơn vị**; tổng SKU/type/tuyến nhất quán.
4. Split/origin/refit, Top 10 theo quantity success trong train, feature/model/config version.
5. Predictions và metric mọi tuyến × SKU; KPI Top 10 kèm MAPE_positive/coverage/MAE/WAPE.
6. Calendar có nguồn/version; stock/receipts/SS/ROP/MOQ/ngưỡng riêng carrier có scenario/source/status/version và quy tắc sinh.
7. Rerun/idempotency, bảo toàn kho và các ca biên trong [AGENTS](../AGENTS.md).

v0.1 Region × SKU và v0.2 activation là artifact lịch sử, không gắn lại nhãn thành kết quả tuyến v0.3. Chỉ có orders được cấp; không đặt điều kiện tải thêm dữ liệu kho thật. Xem [DATA_CONTRACT](DATA_CONTRACT.md) và [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md).
