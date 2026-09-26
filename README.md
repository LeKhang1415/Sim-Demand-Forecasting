# SIGMA — Dự báo số lượng bán SIM/eSIM du lịch

Công ty đặt tại Việt Nam, **chỉ bán cho khách hàng ở Việt Nam** mua SIM/eSIM để du lịch nước ngoài. `destination_country` là nước sử dụng SIM; `carrier` là nhà mạng tại nước đích; tuyến = (quốc gia đích, nhà mạng).

**Target:** `SUM(quantity) WHERE order_status = 'success'`, theo `order_date` UTC. Activation chỉ để tham khảo. Dự báo **tất cả 10 SKU trên các tuyến hợp lệ**; Top 10 tuyến chỉ là nhóm đánh giá KPI MAPE ≤20%, chọn bằng tổng quantity success trong train.

## Dữ liệu và sản phẩm

- 100.000 đơn hàng; 18 quốc gia đích, 46 nhà mạng, 8 khu vực, 10 SKU; hai loại `eSIM` và `physical_SIM`.
- Giai đoạn 01/01/2024–31/12/2025: **731 ngày**. Có 93.104 đơn success, tương ứng **118.296 đơn vị bán ra**.
- Chỉ có orders được cấp. Calendar, tồn kho, receipts và quy tắc nhập do nhóm dẫn xuất hoặc cấu hình scenario.
- SS, ROP, MOQ và ngưỡng cảnh báo cấu hình **riêng từng carrier/đối tác**, có version và hiệu lực; giá trị cụ thể chưa được mentor duyệt.

## Input → xử lý → output

`Orders → kiểm tra → quantity success/ngày/tuyến/SKU → baseline/model → forecast`

`Forecast + tồn kho/config theo đối tác → lượng nhập đề xuất + cảnh báo + dashboard`

KPI: **MAPE ≤20% ở Top 10 tuyến**, cảnh báo cạn kho trước **≥7 ngày**. MAPE dùng các điểm actual>0 với tên `MAPE_positive`, kèm coverage và MAE/WAPE. Tồn kho và cảnh báo được đánh giá bằng mô phỏng.

## Tài liệu

| Đọc để làm gì | File |
|---|---|
| Hiểu sản phẩm, thị trường và phạm vi; chuẩn bị slide M1 | [PROJECT_OVERVIEW](docs/PROJECT_OVERVIEW.md) |
| Tra target, schema và số liệu | [DATA_CONTRACT v0.3](docs/DATA_CONTRACT.md) |
| Tra xác nhận mentor và nội dung còn mở | [DECISIONS](docs/DECISIONS.md) |
| Triển khai xử lý, mô hình và feature | [DATA_PIPELINE](docs/DATA_PIPELINE.md), [METHODOLOGY](docs/METHODOLOGY.md), [FEATURE_SYSTEM](docs/FEATURE_SYSTEM.md) |
| Đánh giá và mô phỏng | [EVALUATION_AND_BACKTEST](docs/EVALUATION_AND_BACKTEST.md) |
| Xây schema, cấu hình tồn kho và output | [ARCHITECTURE](docs/ARCHITECTURE.md), [PRODUCT](docs/PRODUCT.md) |
| Theo dõi kế hoạch, phân công và tái lập | [ROADMAP](docs/ROADMAP.md), [PROJECT_MAP](docs/PROJECT_MAP.md), [REPRODUCIBILITY](docs/REPRODUCIBILITY.md) |
| Kiểm tra luật kỹ thuật và lịch sử | [AGENTS](AGENTS.md), [Review](Review_SIGMA_M2_M3.md), [CHANGELOG](docs/CHANGELOG.md) |

Cập nhật ngày **26/09/2026** theo xác nhận mentor do người dùng cung cấp, ưu tiên hơn phần activation trong [ảnh đề bài](docs/PROJECT_REQUIREMENTS.png) và đề xuất cũ. **[CỨNG]** là ràng buộc kỹ thuật; **[MỀM]** là phương án có thể thay; **[XÁC NHẬN]** là nội dung còn cần chốt. Chi tiết đã xác nhận được ghi riêng trong decision log.

Hiện ở M2 (hạn 17/10/2026), M3 hạn 07/11/2026. Chưa có pipeline sản phẩm; script trong `review_work/` phục vụ kiểm chứng, chưa chứng minh các artifact M1/M2 đã hoàn thành.
