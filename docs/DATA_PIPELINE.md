# Pipeline dữ liệu

**Input → xử lý → output:** orders → quantity success/order_date UTC/tuyến/SKU → forecast tất cả sản phẩm → policy theo carrier → khuyến nghị và cảnh báo. [Contract v0.3](DATA_CONTRACT.md) đã chốt target; activation chỉ tham khảo. Đây là pipeline dự kiến, chưa có code sản phẩm.

## Các bước B1–B9

| Bước | Input → output | Việc thực hiện |
|---|---|---|
| B1. Nạp/chuẩn hóa | CSV → ORDERS | Raw bất biến; parse UTC, kiểm tra trùng/missing/quantity/giá/doanh thu; giữ activation NULL. Lưu checksum/cutoff/version |
| B2. Danh mục | ORDERS → country/carrier/region/SKU | Kiểm tra carrier → country → region và thuộc tính SKU; catalog dùng tại origin phải khai báo |
| B3. Target | ORDERS → DAILY_DEMAND | Lọc success, SUM(quantity) theo order_date × country × carrier × SKU; gộp type. Đối soát toàn kỳ 118.296 đơn vị; zero có điều kiện |
| B4. Calendar | Lịch tự dựng → calendar có nguồn/version | Phủ train và forecast; lịch lễ Việt Nam/mùa du lịch thử riêng |
| B5. Feature | Target + calendar → feature/label tại origin | Lag/rolling trong chuỗi, shift đúng; direct dùng thống kê origin và lịch origin+h |
| B6. Backtest | Feature/split → baseline/model/metric | Naive/moving average cho tất cả tuyến × SKU; Top 10 tuyến theo quantity success trong train; chọn model/fallback bằng validation |
| B7. Forecast | Model + dữ liệu tới origin → FORECAST_RESULT | Đủ 10 SKU × mọi tuyến hợp lệ; số thực, metadata và lý do thiếu rõ; cộng SKU/type lên tuyến để chấm KPI |
| B8. Tồn kho | Forecast + scenario → projected stock | Tách type, share cùng target/parent/cửa sổ tại origin; dùng stock/receipts/config riêng carrier; khai báo giả định một đơn vị bán trừ một đơn vị kho |
| B9. Quyết định | Projected stock + policy → recommendation/alert/dashboard | Áp SS/ROP/MOQ/ngưỡng riêng carrier, tách rủi ro trước ETA; lưu run/snapshot/config/allocation/rule/scenario, rerun không lặp đơn đã chấp nhận |

## Kiểm tra trước khi công bố

- **[CỨNG]** Không dùng actual tương lai cho forecast nhiều bước. Direct training row chỉ dùng khi toàn bộ nhãn nằm trước cutoff; recursive thay actual chưa biết bằng forecast.
- Top 10 chỉ từ train; model/feature/cửa sổ/ngưỡng chỉ chọn bằng train/validation. Khóa trước final test.
- Không dùng activation/trạng thái tương lai, giá bình quân/revenue/quantity ngày dự báo, CUSTOMER tổng hợp toàn kỳ hoặc các cột bị cấm trong [AGENTS](../AGENTS.md).
- Đối soát tổng tuyến/SKU/type; benchmark Region × SKU v0.1 không phải benchmark tuyến v0.3.
- MAPE_positive kèm coverage và MAE/WAPE; không epsilon. Stock/config/ETA thiếu có trạng thái riêng; q_raw=0 không nâng MOQ; velocity=0 không tự cho OK.
- Calendar và mọi giả định có nguồn/status/version. Chỉ có orders được cấp; nhóm tự dựng scenario, không chờ dữ liệu mới.

Bàn giao gồm dữ liệu xử lý, config, checksum/metadata, baseline/model, predictions và báo cáo metric. [REPRODUCIBILITY](REPRODUCIBILITY.md) sẽ bổ sung lệnh thực khi có code; split ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md), policy ở [ARCHITECTURE](ARCHITECTURE.md).
