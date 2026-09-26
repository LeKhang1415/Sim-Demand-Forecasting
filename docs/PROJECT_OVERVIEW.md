# Tổng quan dự án SIGMA

## Mô hình kinh doanh

SIGMA nghiên cứu bài toán của **công ty bán SIM/eSIM và gói data du lịch quốc tế đặt tại Việt Nam**. Công ty **chỉ bán cho khách hàng ở Việt Nam**, không bán cho người ở nước ngoài. Người Việt mua sản phẩm trước chuyến đi để sử dụng tại nước đến.

**Khách hàng ở Việt Nam → mua SIM/eSIM → du lịch và dùng data ở nước ngoài.**

| Khái niệm | Ý nghĩa |
|---|---|
| `destination_country` | Quốc gia đích sử dụng SIM, không phải nơi bán |
| `carrier` | Nhà mạng tại nước đích mà SIM kết nối, ví dụ AIS ở Thái Lan, NTT Docomo ở Nhật; là chiều đối tác cấu hình tồn kho |
| `region` | Nhóm địa lý của các nước đích như SEA, East Asia, Americas; không phải vị trí kho |
| Tuyến | Cặp (`destination_country`, `carrier`), tức tuyến sản phẩm theo điểm đến |
| `sku` | Mẫu gói data; cùng SKU có thể xuất hiện ở nhiều tuyến |
| `product_type` | `eSIM` hoặc `physical_SIM`; quản lý tồn kho riêng |

**10 SKU:** D1G-3D, D3G-5D, D5G-7D, D10G-10D, D15G-15D, D20G-30D, UL-5D, UL-7D, UL-15D, UL-30D.

## Target và phạm vi dự báo

Mentor xác nhận, được người dùng cung cấp ngày 26/09/2026: **“Mình chỉ quan tâm số bán ra chứ không quan tâm nó có active hay không.”**

- Target chính: **số lượng bán ra (quantity sold)** = `SUM(quantity) WHERE order_status = 'success'` theo `order_date` UTC.
- Dự báo cho **tất cả 10 SKU × các tuyến (country, carrier) hợp lệ**, gồm cả hai product_type. Cấp output cơ sở là ngày × tuyến × SKU; tổng tuyến bằng cộng các SKU. M3 tách tiếp product_type.
- **Top 10 tuyến chỉ dùng đánh giá KPI MAPE ≤20%**, không giới hạn phạm vi dự báo. Xếp hạng theo tổng quantity success của tuyến trong train, gộp SKU/type và khóa danh sách trước đánh giá.
- Activation là thông tin phụ; không dùng làm target, không lọc đơn success theo việc đã kích hoạt.

Mentor cũng xác nhận quy tắc nhập và ngưỡng tồn **khác nhau giữa các đối tác**. SS/ROP/MOQ/ngưỡng cảnh báo phải cấu hình theo carrier; các giá trị cụ thể vẫn là scenario cần mentor xác nhận.

## Dữ liệu và luồng xử lý

| Nội dung | Phạm vi |
|---|---|
| Nguồn được cấp | 100.000 đơn hàng |
| Thời gian đặt hàng | 01/01/2024–31/12/2025, 731 ngày |
| Danh mục | 18 quốc gia đích, 46 nhà mạng, 8 khu vực, 10 SKU, 2 product_type |
| Đơn thành công | 93.104 đơn success |
| Sản lượng thành công | **118.296 đơn vị** |

`Orders → chuẩn hóa UTC/lọc success → tổng quantity/ngày/tuyến/SKU → baseline/model → forecast tất cả sản phẩm`

`Forecast + stock/receipts/config từng carrier → đề xuất nhập → cảnh báo → dashboard`

Chỉ có orders được cấp (phạm vi xác nhận ngày 25/09/2026). Nhóm tự dựng calendar, stock đầu kỳ, L/R/MOQ, receipts/ETA và EOL scenario; lưu nguồn, lý do, version và seed nếu có. Demo replay quantity bán theo ngày đặt; giả định một đơn vị bán tiêu thụ một đơn vị kho phải khai báo. Orders không xác định stock hoặc lead time thật.

## Milestone và đầu ra báo cáo

| Mốc | Nội dung theo phạm vi cập nhật |
|---|---|
| M1 — 19/09/2026 | Chuẩn hóa orders, mô tả sản phẩm/dữ liệu, phân tích bán hàng theo tuần/lễ/mùa và baseline naive/moving average |
| M2 — 17/10/2026 | Forecast tất cả tuyến × SKU, so baseline/model, đánh giá MAPE ≤20% ở Top 10 tuyến |
| M3 — 07/11/2026 | Policy riêng từng carrier, mô phỏng cảnh báo trước ≥7 ngày, dashboard actual/forecast/sai số và tồn kho |

**Gợi ý 5 slide M1:** bài toán và khách hàng → sản phẩm/tuyến → dữ liệu/target → pipeline/baseline → KPI và bước tiếp theo. M1 đã qua hạn; cần kiểm kê artifact, không tự ghi đã hoàn thành.

Cách đo KPI và chống leakage ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md); target/schema ở [DATA_CONTRACT](DATA_CONTRACT.md); quyết định hiện hành ở [DECISIONS](DECISIONS.md). Kết quả tồn kho là mô phỏng; báo đạt/chưa đạt KPI theo thực nghiệm.

Nguồn: cập nhật mentor do người dùng cung cấp ngày 26/09/2026; [review A1–A4, B1–B8](../Review_SIGMA_M2_M3.md). Phần activation trong [ảnh đề bài cũ](PROJECT_REQUIREMENTS.png) đã được thay bằng quantity sold.
