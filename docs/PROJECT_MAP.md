# Phân công và cấu trúc dự án

## Phân công gợi ý theo review D4

Đây là phân công **[MỀM]**, chưa ghi thành cam kết nhân sự đã xác nhận. Cập nhật đầu việc theo [phạm vi chỉ có orders và yêu cầu activation/tuyến](PROJECT_OVERVIEW.md); không giao việc chờ nguồn kho/config thật.

| Thành viên | Vai trò/công việc gợi ý |
|---|---|
| Nguyên | Khóa định nghĩa activation/tuyến và KPI, quyết định mentor, model/fallback từng tuyến và tích hợp; cần hỗ trợ backtest |
| Khang | ETL/schema/version, cửa sổ activation đủ quan sát, đối soát đúng target và giao diện dữ liệu |
| Hiếu | Feature/baseline, đo lại độ thưa và sai số theo tuyến/horizon; hỗ trợ mô hình |
| Du | Tự dựng supplier config/L/R/MOQ và override có lý do/sensitivity; phân bổ theo [ARCHITECTURE](ARCHITECTURE.md) |
| Cường | Tự dựng stock đầu kỳ/receipts theo scenario, projected stock và mô phỏng policy; truy vết nguồn giả định |
| Anh | Kiểm thử nghiệp vụ/cảnh báo, lifecycle/successor và ba EOL scenario theo review |

Dashboard ghép vào nhánh tích hợp sau khi schema output ổn định. Không ưu tiên hoàn thiện đủ các bảng vật lý, tối ưu tài chính hay thêm model trước khi contract/backtest chạy đúng. Lịch giao việc ở [ROADMAP](ROADMAP.md); người quyết định nghiệp vụ được cập nhật riêng tại [DECISIONS](DECISIONS.md), không tự gán theo bảng vai trò này.

## Cấu trúc thư mục

Hiện có `data/`, `docs/`, `review_work/` và file review ở gốc. `review_work/` chứa artifact/script kiểm chứng phục vụ review; chưa có pipeline sản phẩm. Bộ tài liệu không tạo sẵn các thư mục code dưới đây.

**[MỀM] Dự kiến, sẽ điều chỉnh khi bắt đầu code.** Đây là đề xuất tổ chức theo các vai trò/đầu ra D2–D4, không phải cấu trúc đã triển khai hay yêu cầu phải tạo đủ:

```text
TTDN_Sigma/
├── README.md                 # Điểm vào bộ tài liệu
├── AGENTS.md                 # Luật cho coding agent
├── Review_SIGMA_M2_M3.md      # Nguồn review ưu tiên
├── data/                     # Nguồn dữ liệu hiện có; giữ raw bất biến
├── docs/                     # PDF và tài liệu dự án hiện có
├── review_work/              # Artifact kiểm chứng review hiện có
├── pipeline/                 # Dự kiến: nạp, validation, daily grid, batch
├── features/                 # Dự kiến: feature tại origin
├── models/                   # Dự kiến: baseline và global model
├── eval/                     # Dự kiến: rolling-origin, metric, simulation
├── config/                   # Dự kiến: default có source/status, scenario
└── inventory/                # Dự kiến: allocation, policy, projected stock, EOL
```

Chỉ tạo module khi cần cho milestone; chưa ấn định thư viện, lệnh cài đặt hay hạ tầng. Hướng dẫn tái lập để TODO ở [REPRODUCIBILITY](REPRODUCIBILITY.md).

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [B4, D2–D4]; cập nhật vai trò theo [phạm vi mới](PROJECT_OVERVIEW.md), 25/09/2026. Cấu trúc code vẫn là đề xuất dự kiến.
