# Sản phẩm và output

**Input:** orders → quantity success/order_date UTC; inventory, receipts và config từng carrier do nhóm dựng.

**Xử lý:** forecast tất cả tuyến × SKU → tách type cho kho → policy theo đối tác → cảnh báo.

**Output:** bốn nhóm dưới đây, theo [contract v0.3](DATA_CONTRACT.md).

## 1. Sales Forecast — Dự báo số lượng bán

Mỗi dòng là một ngày × tuyến (destination_country, carrier) × SKU, cho **tất cả 10 SKU trên mọi tuyến hợp lệ**. Output cơ sở gộp eSIM/physical_SIM; output cấp type nếu có phải giữ tổng. Top 10 không phải bộ lọc phạm vi forecast.

Trường chính: `run_id`, `series_key`, `origin`, `forecast_date`, `horizon_day`, `destination_country`, `carrier`, `sku`, `forecast_quantity`, `model_version`, `target_version`, `data_cutoff`, `status`.

Actual = SUM(quantity success) theo order_date UTC. Forecast giữ số thực; thiếu đầu ra có lý do rõ. Activation chỉ tham khảo, không quyết định một đơn có vào actual hay không. PK dùng run_id + series_key + forecast_date; run_date riêng lẻ không phân biệt rerun.

## 2. Inventory Recommendation — Đề xuất nhập

Một khuyến nghị cho stock item **country/carrier/SKU/product_type**, kèm region để tổng hợp. Hiển thị usable stock, reserved/backorder, receipts/ETA, nhu cầu trong kỳ bảo vệ, SS, ROP, MOQ, lượng nhập và lý do.

**Chính sách riêng từng carrier/đối tác:** dùng config có scope, version và hiệu lực; hỗ trợ khác SS, ROP, MOQ, ngưỡng cảnh báo, L/R và policy. Override SKU/type theo thứ tự rõ. Không áp một bộ tham số chung hoặc tự điền ngưỡng “Vina” khi mentor chưa cho con số.

Liên kết forecast run, snapshot, config/allocation/rule version và scenario_id. Lưu cơ sở so ngưỡng (on-hand hay IP), toán tử < hoặc ≤ và kết quả áp rule. Các giá trị chưa duyệt mang trạng thái **cần mentor xác nhận**.

**[CỨNG]** Thiếu stock/config/ETA có trạng thái riêng; q_raw=0 thì q=0 dù có MOQ. MOQ không phải bội số đóng gói. Tách lượng đặt khỏi rủi ro thiếu trước ETA; rerun không sinh đề xuất lặp cho đơn đã chấp nhận.

## 3. Stockout Alert — Cảnh báo thiếu hàng

Tính projected stock mỗi ngày theo forecast, tồn khả dụng, reservation/backorder và lịch nhận hàng. Áp ngưỡng riêng từng carrier; hiển thị ngày thiếu đầu tiên, horizon đã xét, mức cảnh báo và config version.

- **Mục tiêu:** cảnh báo trước ≥7 ngày; đo ca đủ sớm/muộn/bỏ sót/chưa đủ quan sát bằng mô phỏng.
- velocity_7d=0 không tự cho OK; days_of_cover=N/A. Thiếu bằng chứng thì “chưa đủ dữ liệu”.
- Hàng về sau ngày thiếu không xóa cảnh báo trước ETA. Phân biệt hết tồn cuối ngày với thiếu nhu cầu trong ngày.
- Chưa cạn thì ghi “chưa thấy cạn trong horizon”; ngoại suy run-rate phải có nhãn.
- EOL chỉ tác động đúng offering; zero-run chỉ là dấu hiệu nghi gián đoạn, không chứng minh ngừng vĩnh viễn.

## 4. Dashboard

| Khối | Hiển thị |
|---|---|
| Bán hàng | Actual/forecast/sai số; lọc country, carrier, SKU, type, region |
| KPI | Top 10 theo quantity success trong train; MAPE_positive, số điểm/tổng điểm, coverage, MAE/WAPE/bias; mục tiêu ≤20% |
| Tồn kho theo đối tác | Stock, receipts/ETA, SS/ROP/MOQ, config version, lượng đề xuất, cảnh báo |
| Truy vết | Target/filter/UTC, cutoff, model/run, scenario và trạng thái thiếu dữ liệu |

**[CỨNG]** MAPE không tính actual=0, không chèn epsilon; metric ngày khác metric tổng horizon. Phần kho/cảnh báo ghi nhãn **mô phỏng**; actual bán hàng là dữ liệu lịch sử từ orders.

**[MỀM] / [XÁC NHẬN]** Tự động tính khuyến nghị, con người quyết định mua; chưa có quyết định tự gửi đơn. Chi tiết policy ở [ARCHITECTURE](ARCHITECTURE.md), cách chấm ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md).
