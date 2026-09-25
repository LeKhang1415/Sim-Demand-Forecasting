# Sản phẩm và bốn output

Giữ bốn nhóm output từ PDF, cập nhật theo [đề bài gốc và phạm vi chỉ có orders](PROJECT_OVERVIEW.md). M2 cần forecast activation theo tuyến; M3 dùng tồn kho/config do nhóm giả định. Các tham số và cách đo chi tiết theo [DECISIONS](DECISIONS.md), vẫn là **đề xuất — cần mentor xác nhận**; mục tiêu KPI gốc không bị bỏ.

## Output 1 — Demand Forecast

Bảng dự báo lượng kích hoạt theo ngày, theo tuyến country/carrier. **[MỀM]** Các trường đề xuất: `run_id`, `run_date`, `destination_country`, `carrier`, `forecast_date`, `horizon_day`, `forecast_quantity`, `model_version`, `target_version`, `data_cutoff`; SKU/type nếu có đầu ra cấp con. Nhánh order-date × Region × SKU giữ nhãn v0.1 riêng. Horizon và cách chấm ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md).

**[CỨNG]** run_date không phân biệt nhiều lượt chạy; giữ metadata theo [ARCHITECTURE](ARCHITECTURE.md). Forecast là số thực. Actual lấy từ các dòng activation theo filter/cửa sổ quan sát đã công bố; không gọi là nhu cầu tiềm ẩn hoặc lượng trừ kho thật. Dashboard dùng replay lịch sử, không gọi dữ liệu cũ là dự báo vận hành hiện tại.

## Output 2 — Inventory Recommendation

Hiển thị tồn kho và đề xuất theo **region × carrier × SKU × product_type**. Các trường đề xuất gốc: `generated_date`, `region`, `carrier`, `sku`, `product_type`, `current_stock`, `in_transit_qty`, `forecast_7d_qty`, `safety_stock`, `reorder_point`, `days_of_cover`, `expected_stockout_date`, `recommended_qty`, `alert_level`.

**[CỨNG]** Chỉnh khóa/metadata để truy vết run forecast, snapshot, config, allocation, rule và scenario. Không sao chép công thức nhập mâu thuẫn của PDF; dùng một policy có L/R/IP rõ ở [ARCHITECTURE](ARCHITECTURE.md). Nếu mở horizon M3, thể hiện rõ kỳ bảo vệ và tổng nhu cầu tương ứng; trường forecast_7d_qty không thay thế nhu cầu L+R khi L+R khác kỳ này.

Stock/config/receipts được nhóm dựng cho scenario; stock sau đó cập nhật theo mô phỏng. Ghi rõ giả định trừ kho, source/scenario/version và chính sách cho từng type. Tách lượng đặt với nguy cơ thiếu trước ETA; config thiếu vẫn là “chưa đủ dữ liệu”, khác giá trị giả định đã khai báo. Không coi stock thiếu là 0; q_raw=0 không nâng MOQ. Output phải ghi “mô phỏng/chưa phải số liệu vận hành thật”.

## Output 3 — Stockout Alert

Cảnh báo ngày dự kiến thiếu hàng đầu tiên dựa trên projected stock, forecast và snapshot/receipts mô phỏng. **Mục tiêu đề bài là cảnh báo trước ≥7 ngày**; trình kết quả đo đủ sớm/muộn/bỏ sót và ca chưa đủ quan sát theo [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md), không tự bỏ mục tiêu.

- **[CỨNG]** Không hứa cảnh báo trước ≥7 ngày trong mọi trường hợp. Nếu chưa thấy cạn trong horizon, chỉ kết luận trong horizon đó; ngày cạn từ ngoại suy run-rate phải được ghi rõ là ngoại suy.
- **[CỨNG]** velocity_7d=0 không tự cho OK; nếu không đủ bằng chứng thì “chưa đủ dữ liệu”. days_of_cover khi velocity=0 là N/A, không tạo ngày cạn giả.
- **[CỨNG]** Hàng đang về sau ngày thiếu không xóa cảnh báo trước ETA. Phân biệt “hết tồn cuối ngày” với “không đáp ứng đủ nhu cầu trong ngày”.
- EOL trong demo là sự kiện scenario được khai báo; không giả danh xác nhận vận hành. Zero-run/lỗi chỉ là tín hiệu “nghi ngừng/gián đoạn”, không tự kết luận EOL thật.

## Output 4 — Dashboard

Dashboard dự báo và sai số thực tế là yêu cầu đề bài. Hiển thị actual activation lịch sử từ orders, forecast và sai số theo tuyến, kết quả Top 10 so với mục tiêu MAPE ≤20%; ghi filter/cửa sổ/cutoff. Phần stock, SS/ROP, ETA, lượng đặt, ngày cạn và cảnh báo có nhãn mô phỏng/scenario. Có thể drill-down SKU/type/region và nguồn giả định; chi tiết giao diện ở câu 10 còn cần chốt.

**[CỨNG]** MAPE không xác định khi actual=0: hiển thị MAPE_positive cùng coverage và MAE/WAPE; không chèn epsilon hoặc gọi số đã bỏ zero là MAPE toàn bộ. Phân biệt metric ngày với metric tổng horizon. Trạng thái thiếu dữ liệu và nhãn minh họa phải thấy được trong output.

**[XÁC NHẬN]** Default câu 11 là tự động tính khuyến nghị, con người quyết định mua; không tự gửi đơn cho NCC. Đây chưa phải quyết định nghiệp vụ đã duyệt. Giới hạn mô phỏng/đánh giá cảnh báo ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md).

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [B1, B3–B8, D1–D3]; bốn nhóm output từ PDF VI; điều chỉnh theo [đề bài và phạm vi người dùng](PROJECT_OVERVIEW.md), 25/09/2026.
