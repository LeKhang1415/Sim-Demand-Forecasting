# Phân công và cấu trúc dự án

Phân công **[MỀM]** theo review D4, cập nhật ngày 26/09/2026; chưa phải cam kết nhân sự. Phạm vi: quantity success/order_date UTC, forecast đủ tuyến × SKU, tồn kho/config riêng từng carrier.

| Thành viên | Công việc gợi ý |
|---|---|
| Nguyên | Tích hợp, cách đo KPI Top 10, model/fallback và quyết định còn mở |
| Khang | ETL/schema/version, UTC, mapping tuyến, đối soát 118.296 đơn vị success |
| Hiếu | Feature/baseline, backtest mọi tuyến × SKU, nhóm thưa và sai số horizon |
| Du | Config SS/ROP/MOQ/ngưỡng theo carrier/type, override SKU, phân bổ |
| Cường | Stock đầu kỳ/receipts, projected stock và mô phỏng policy |
| Anh | Kiểm thử rule/cảnh báo, lifecycle/successor và EOL scenario |

Dashboard ghép sau khi schema output ổn định. Nhóm tự dựng đầu vào M3; không giao việc chờ kho/config thật. Tiến độ ở [ROADMAP](ROADMAP.md), trạng thái nghiệp vụ ở [DECISIONS](DECISIONS.md).

## Thư mục

| Hiện có | Vai trò |
|---|---|
| `data/` | CSV nguồn; giữ raw bất biến |
| `docs/` | Tài liệu hiện hành, PDF và ảnh đề bài lịch sử |
| `review_work/` | Script/artifact kiểm chứng review, chưa phải pipeline sản phẩm |
| `Review_SIGMA_M2_M3.md` | Review lịch sử và số liệu kiểm chứng |
| `AGENTS.md` | Luật kỹ thuật khi triển khai |

**[MỀM]** Khi bắt đầu code có thể tách `pipeline/`, `features/`, `models/`, `eval/`, `config/`, `inventory/` theo chức năng. Chỉ tạo phần cần cho milestone, chưa ấn định thư viện/hạ tầng hoặc giả vờ đã có lệnh chạy.

Hướng dẫn tái lập sẽ cập nhật tại [REPRODUCIBILITY](REPRODUCIBILITY.md).
