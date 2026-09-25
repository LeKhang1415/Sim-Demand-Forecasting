# Team SIGMA — Dự báo nhu cầu & tối ưu tồn kho kho số SIM / gói data

Dự án dự báo lượng kích hoạt SIM/gói data theo ngày và theo tuyến quốc gia–nhà mạng, từ đó đề xuất mức đặt hàng và cảnh báo cạn kho số. **Chỉ được cung cấp orders**; dữ liệu khác do nhóm dẫn xuất hoặc giả định có nguồn, dùng mô phỏng tồn kho.

Đã review xong yêu cầu đề tài; đang ở M2, hạn **17/10/2026**.
Trạng thái này được ghi nhận tại ngày 25/09/2026; chưa xác nhận các artifact M1 đã hoàn thành.
Yêu cầu gốc và phạm vi dữ liệu đã được người dùng bổ sung; chi tiết target/metric và tham số scenario còn là đề xuất cần xác nhận.

## Tài liệu dự án

- [PROJECT_OVERVIEW](docs/PROJECT_OVERVIEW.md): mục đích, phạm vi, nguồn dữ liệu và trạng thái các milestone.
- [DATA_CONTRACT](docs/DATA_CONTRACT.md): contract v0.2, target activation đề xuất và số liệu kiểm chứng v0.1 được giữ riêng.
- [DATA_PIPELINE](docs/DATA_PIPELINE.md): chín bước xử lý đã điều chỉnh theo review và các điểm chống leakage.
- [METHODOLOGY](docs/METHODOLOGY.md): cấp dự báo, baseline, mô hình ứng viên và tham chiếu phương pháp.
- [FEATURE_SYSTEM](docs/FEATURE_SYSTEM.md): feature đề xuất, thử nghiệm calendar và giới hạn thông tin tại origin.
- [EVALUATION_AND_BACKTEST](docs/EVALUATION_AND_BACKTEST.md): metric, split, benchmark chẩn đoán và điều kiện hoàn thành M2.
- [ARCHITECTURE](docs/ARCHITECTURE.md): ba khối dữ liệu, khóa bảng, phân bổ và chính sách tồn kho đề xuất.
- [PRODUCT](docs/PRODUCT.md): bốn output cùng giới hạn của dự báo, khuyến nghị và cảnh báo.
- [DECISIONS](docs/DECISIONS.md): yêu cầu đã bổ sung, 12 câu gốc và quyết định cập nhật.
- [ROADMAP](docs/ROADMAP.md): timeline M2/M3 và rủi ro cần xử lý ở từng giai đoạn.
- [PROJECT_MAP](docs/PROJECT_MAP.md): phân công theo vai trò và cấu trúc code dự kiến.
- [AGENTS](AGENTS.md): checklist luật cứng dành cho AI coding agent.
- [CHANGELOG](docs/CHANGELOG.md): ghi nhận khởi tạo bộ tài liệu.
- [REPRODUCIBILITY](docs/REPRODUCIBILITY.md): TODO hướng dẫn tái lập khi pipeline hoàn thành.

## Nguồn và cách đọc

- [Đề bài T2](docs/PROJECT_REQUIREMENTS.png) và [phạm vi cập nhật](docs/PROJECT_OVERVIEW.md): yêu cầu gốc, chỉ có orders; ưu tiên hơn các đề xuất cũ mâu thuẫn.
- [Review_SIGMA_M2_M3.md](Review_SIGMA_M2_M3.md): số liệu đã kiểm chứng và ràng buộc kỹ thuật; các đề xuất cũ được ghi rõ phạm vi áp dụng.
- [Báo cáo chi tiết Sigma.pdf](docs/B%C3%A1o%20c%C3%A1o%20chi%20ti%E1%BA%BFt%20Sigma.pdf): đề xuất gốc, chỉ dùng ở phần chưa bị review phản biện.

Giữ nguyên ý nghĩa các nhãn: **[CỨNG]** là lỗi/rủi ro cần xử lý; **[MỀM]** là phương án có thể thay; **[XÁC NHẬN]** là giả định chưa được chốt.
Tra DECISIONS trước khi dùng một default; không coi bảng đề xuất là quyết định của mentor.
MAPE ≤20% ở Top 10 tuyến và cảnh báo trước ≥7 ngày vẫn là mục tiêu đề bài; báo kết quả đo, không tự bỏ KPI hoặc bảo đảm chưa có bằng chứng.
Chưa có pipeline sản phẩm; các script kiểm chứng trong `review_work/` không chứng minh M1/M2 đã hoàn thành.
