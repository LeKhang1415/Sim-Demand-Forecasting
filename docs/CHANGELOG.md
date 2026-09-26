# Changelog

## 26/09/2026 — Đồng bộ xác nhận mentor

- Contract v0.3: **quantity sold = SUM(quantity success) theo order_date UTC**; activation hạ thành tham khảo.
- Làm rõ công ty chỉ bán cho khách ở Việt Nam đi du lịch quốc tế; country/carrier là điểm đến sử dụng.
- Forecast tất cả 10 SKU × tuyến hợp lệ; Top 10 theo tổng quantity success trong train chỉ chấm KPI.
- Cấu hình tồn kho SS/ROP/MOQ/ngưỡng cảnh báo riêng từng carrier; giá trị chưa cung cấp vẫn là scenario cần xác nhận.
- Rút gọn tài liệu cho báo cáo M1, đồng bộ pipeline/output/feature/backtest/roadmap và AGENTS; giữ luật kỹ thuật và review lịch sử.
- Thêm quy tắc cập nhật GitHub trong AGENTS: kiểm tra phạm vi, commit, push và xác minh remote theo yêu cầu người dùng.
- Chỉ sửa Markdown; chưa chạy benchmark mới hoặc sửa CSV/pipeline.

## 25/09/2026 — Lịch sử

- Khởi tạo bộ tài liệu từ [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md).
- Theo ảnh đề bài và phạm vi chỉ có orders, đưa ra contract v0.2 activation/tuyến, tự dựng scenario M3. Định hướng target này đã được thay bằng xác nhận ngày 26/09/2026.

Nguồn quyết định hiện hành: [DECISIONS](DECISIONS.md).
