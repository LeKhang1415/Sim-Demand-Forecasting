# Roadmap M1–M3

Cập nhật **26/09/2026**: target quantity success theo order_date UTC; forecast **tất cả 10 SKU × tuyến**, Top 10 chỉ chấm KPI; tồn kho/config riêng từng carrier. Lịch dưới đây là **[MỀM]**, các tham số còn mở ở [DECISIONS](DECISIONS.md).

## Bù artifact và chuẩn bị slide M1

M1 hạn 19/09/2026 đã qua; chưa đủ bằng chứng hoàn thành. Kiểm kê và bù: mô tả khách hàng/sản phẩm → 100.000 orders, 18 nước, 46 carrier, 8 region, 10 SKU → 731 ngày, 118.296 quantity success → pipeline → baseline và KPI. Dùng [PROJECT_OVERVIEW](PROJECT_OVERVIEW.md) làm khung slide, không coi cập nhật tài liệu là đã chạy baseline.

## M2 — đến 17/10/2026

| Mốc | Công việc | Bàn giao |
|---|---|---|
| 25–27/09 | Đồng bộ xác nhận mentor, kiểm kê M1, thống nhất cách tổng hợp KPI | Contract v0.3, decision log, danh sách artifact thiếu |
| 28–30/09 | Pipeline quantity success/ngày/tuyến/SKU, checksum, split và Top 10 từ train; chạy naive/moving average | Target đối soát 118.296 toàn kỳ, profile và baseline mọi chuỗi |
| 01–05/10 | Feature tại origin, thử global model; calendar ablation | Predictions validation đúng horizon, không leakage |
| 06–09/10 | Rolling-origin; chọn model/fallback theo tuyến, kiểm tra nhóm thưa | So sánh model, bias, lỗi ngày/tổng horizon và SKU |
| 10–12/10 | Khóa model/feature, chạy final test; thử phân bổ type | KPI Top 10 có coverage, metric toàn bộ sản phẩm; không tuning trên test |
| 13–15/10 | Đóng gói batch, metadata, rerun và replay lịch sử | Lệnh thực, config/artifact, output mọi tuyến × SKU |
| 16–17/10 | Chạy lại từ đầu, rà kết quả và trình bày | Nộp M2; tách hoàn thành kỹ thuật và đạt/chưa đạt KPI |

Split đề xuất: train đến 30/06/2025, validation quý III, test quý IV/2025; chi tiết tại [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md). Số dòng output theo catalog và horizon, không dùng 80 chuỗi của benchmark cũ làm phạm vi.

## M3 — 18/10–07/11/2026

| Mốc | Công việc | Bàn giao |
|---|---|---|
| 18–20/10 | Dựng stock/receipts/config theo từng carrier/type, override SKU; khai báo policy và ngưỡng | Scenario có source/lý do/status/version, hiệu lực và giả định tiêu thụ quantity bán |
| 21–25/10 | Phân bổ, projected stock, lượng nhập, cảnh báo; mở/backtest horizon | Tách rủi ro trước ETA, dữ liệu thiếu và rerun; bảo toàn kho |
| 26–29/10 | So policy cùng demand/scenario/randomness; sensitivity, EOL | Fill rate, lost units/backorders, tồn kho, cảnh báo đủ sớm/muộn/bỏ sót |
| 30/10–02/11 | Dashboard actual quantity sold/forecast/sai số và tồn kho theo carrier | Demo luồng đầy đủ, nhãn mô phỏng và config version |
| 03–05/11 | Kiểm thử biên, idempotency; chuẩn bị slide/diễn tập | Ca bắt buộc pass, báo scenario chưa đạt/chưa đủ quan sát |
| 06–07/11 | Sửa lỗi, đóng gói | Demo, config, hướng dẫn chạy và báo cáo KPI |

**[MỀM] — cần mentor xác nhận:** có thể thử L={1,3,7} ngày, R={1,7}, stock đầu kỳ tương đương {3,7,14} ngày bán trung bình train; MOQ/SS/ROP/ngưỡng khai báo riêng carrier. Đây là stress test, không phải tham số ước lượng từ orders. Thêm nhận hàng trễ, không có hàng về và EOL có báo trước/đột ngột/suspended hồi phục; lưu seed nếu ngẫu nhiên.

## Điều kiện bàn giao

- Đúng target/grain và đủ sản phẩm; không giới hạn forecast ở Top 10.
- Không leakage, metric zero đúng; giữ KPI MAPE ≤20% và cảnh báo ≥7 ngày.
- Stock/config/ETA thiếu khác 0; zero velocity không tự là an toàn; policy có scope carrier/version.
- EOL đúng offering, successor tương thích; dữ liệu scenario không gọi là vận hành thật.
- Dữ liệu order kết thúc 31/12/2025: demo replay lịch sử hoặc forecast sau đó ghi chưa có actual bán hàng; không gọi là forecast vận hành 2026.

Không chờ thêm orders/inventory/config thật. Checklist chi tiết ở [AGENTS](../AGENTS.md), phân công ở [PROJECT_MAP](PROJECT_MAP.md).
