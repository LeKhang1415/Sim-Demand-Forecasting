# Hệ thống feature đề xuất

**[MỀM]** Các cửa sổ feature kế thừa review B2, chưa được xác nhận trên target activation/tuyến. Theo [DATA_CONTRACT v0.2](DATA_CONTRACT.md), lag/rolling phải tính lại theo sự kiện kích hoạt và grain đã khai báo; không tái dùng feature order-date dưới tên activation. Chọn bằng train/validation; tra [DECISIONS](DECISIONS.md).

## Danh sách ứng viên

| Nhóm | Feature | Trạng thái và điều kiện |
|---|---|---|
| Định danh | destination_country, carrier cho tuyến; sku nếu mô hình tách SKU; region là chiều tổng hợp | **[MỀM]** Điều chỉnh cho yêu cầu tuyến; không nhầm carrier là feature hợp lệ trên một dòng tổng hợp nhiều carrier |
| Lịch cơ bản | Ngày trong tuần, tháng | **[MỀM]** Lịch của ngày cần dự báo, cùng quy ước ngày của contract |
| Lag | Lag 1/7/14/28 | **[MỀM]** Theo từng chuỗi; chỉ lấy giá trị đã biết tại origin |
| Rolling | Mean 7/28/56; độ lệch chuẩn 28 ngày | **[MỀM]** Shift trước tổng hợp khi dự báo ngày t từ dữ liệu tới t−1 |
| Độ thưa | Tỷ lệ zero 28/56 ngày; số ngày từ lần bán gần nhất | **[MỀM]** Tính từ lịch sử tại origin; không suy ra EOL chỉ từ khoảng trống |
| Thuộc tính SKU | data_gb, validity_days, plan_type | **[MỀM]** Dùng trực tiếp khi dòng ứng với một SKU; tuyến có nhiều SKU không được gán tùy ý một thuộc tính. Có thể bỏ nhóm này khi dự báo tổng tuyến; cố định theo SKU không tạo thông tin thời gian mới |
| Direct multi-horizon | horizon_day và lịch origin+h | **[MỀM]** Dùng cùng thống kê tại origin để dự báo quantity ở origin+h |
| Lễ/mùa hè | Feature lịch lễ và mùa hè trong calendar | **[MỀM] / [XÁC NHẬN]** Thử riêng sau khi chốt ý nghĩa/nguồn calendar; so có/không calendar bằng ablation |

Calendar có nhãn lễ không đồng nghĩa đã xác nhận tác động nhu cầu. Khách đến Đông Á không chỉ chịu lịch lễ Đông Á; dữ liệu thiếu thị trường nguồn của khách nên không tự chọn lịch quốc gia chi phối. Các hệ số mùa vụ chưa tái lập được không được biến thành tham số chắc chắn hoặc dùng để nhân mùa vụ hai lần.

## Ràng buộc thông tin tại origin

- **[CỨNG]** Không đưa feature hoặc nhãn chứa thông tin sau origin vào đầu vào dự báo. Nhãn huấn luyện origin+h chỉ dùng khi đã nằm trước cutoff của tập huấn luyện. Các phép lag/rolling phải ở trong chuỗi; rolling trên ngày t dùng dữ liệu tới t−1 phải shift trước tổng hợp.
- **[CỨNG]** Kiểm thử đúng nhiều bước: không dùng lag_1 với actual ngày tương lai để dự báo bước tiếp theo. Direct dùng thống kê tại origin; recursive phải thay actual chưa biết bằng forecast trong training/evaluation tương ứng.
- Giá/khuyến mãi tương lai chỉ dùng khi đã biết tại origin. Giá bình quân của các đơn trong ngày cần dự báo, revenue và quantity cùng ngày là leakage.
- Không dùng activation/trạng thái tương lai; CSV chỉ có trạng thái cuối nên phải công bố giả định nhãn đủ chín.
- Không đặt một carrier categorical đơn lẻ trên dòng Region × SKU có nhiều carrier. Nếu cần, chỉ dùng tỷ trọng lịch sử tại origin; review chưa yêu cầu bước này cho M2.
- Không dùng CUSTOMER tổng hợp toàn kỳ làm feature. Không dùng `customer_type`, `is_suspected_anomaly`, `anomaly_note` trong feature/logic.
- **[CỨNG]** Khóa feature trước final test; không dùng test để chọn cửa sổ hoặc cách xử lý nhóm thưa. Quy tắc nhãn direct/cutoff ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md).

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [phạm vi, A2.4, A2.6, B1–B4, B7.f, D2]; điều chỉnh grain theo [đề bài](PROJECT_OVERVIEW.md), 25/09/2026.
