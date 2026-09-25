# Pipeline dữ liệu

Luồng dự kiến giữ tên **B1–B9 của mục VII.9 trong PDF**, đã sửa theo review và [phạm vi chỉ có orders](PROJECT_OVERVIEW.md). Target activation/tuyến đề xuất theo [DATA_CONTRACT v0.2](DATA_CONTRACT.md); chi tiết filter/metric còn cần chốt ở [DECISIONS](DECISIONS.md). Nhóm chủ động dựng đầu vào M3 có provenance, không chờ dữ liệu kho/config thật. Chưa có pipeline sản phẩm được triển khai.

## Các bước xử lý

| Bước | Input → output | Cách thực hiện sau review |
|---|---|---|
| B1. Nạp & chuẩn hóa | Orders raw → ORDERS chuẩn hóa | Giữ raw bất biến; parse order/activation UTC và suy ngày riêng cho từng sự kiện. Kiểm tra trùng, missingness, quantity/giá/doanh thu theo contract. Giữ activation NULL, không impute; xác định cửa sổ activation đủ quan sát. Lưu checksum, cutoff, target/filter/grain version |
| B2. Tách bảng tra cứu | ORDERS → REGION, COUNTRY, CARRIER, SKU_CATALOG; CUSTOMER nếu cần tra cứu | Kiểm tra phụ thuộc carrier → country → region và thuộc tính SKU. **[CỨNG]** Country–Carrier là 1–n; FK riêng không đủ ngăn bộ ba mâu thuẫn. Không dùng CUSTOMER tổng hợp toàn kỳ làm feature |
| B3. Lọc target & gộp | ORDERS → DAILY_DEMAND theo target version | Nhánh đáp ứng đề bài: activation_date × tuyến country/carrier với filter đã khai báo; xem success và success+refunded theo contract. Nhánh order_date × Region × SKU chỉ để tái lập v0.1. Không dùng kích thước/số liệu v0.1 làm đối soát activation. **[CỨNG]** Zero chỉ được điền trong cửa sổ đủ dữ liệu dưới giả định quan sát đã nêu |
| B4. Chuẩn bị CALENDAR | Calendar tự dựng + lịch ngày cần dự báo → CALENDAR có nguồn/version | Kiểm tra tính duy nhất/liên tục của ngày; đã có nhãn Tết Nguyên Đán. **[XÁC NHẬN]** Chưa gọi lịch tự dựng là chính thức. Mở rộng các ngày forecast trước inference |
| B5. Ghép calendar & tạo feature tại origin | DAILY_DEMAND + CALENDAR → feature/label theo origin, horizon_day | Ghép ngày theo event_date_basis UTC; thống kê trong từng tuyến hoặc grain được version hóa. Shift trước rolling; direct dùng thống kê tại origin và lịch origin+h, không actual tương lai. Không trộn lịch order và activation. Xem [FEATURE_SYSTEM](FEATURE_SYSTEM.md) |
| B6. Huấn luyện & chấm điểm | Feature theo split → baseline, model ứng viên, metric validation | Naive/moving average theo tuyến, so ứng viên SARIMA/Prophet/LightGBM phù hợp; global là lựa chọn thử nghiệm. Rolling-origin chỉ trên cửa sổ activation đủ quan sát; khóa Top 10 tuyến bằng train. Báo kết quả từng tuyến và KPI gốc, kèm metric/coverage; không tuning final test. Xem [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md) |
| B7. Dự báo | Model được khóa + thông tin đã có tại origin → FORECAST_RESULT | Output activation theo tuyến, horizon/version/cutoff rõ; forecast số thực. Có output hoặc lý do thiếu cho mỗi tuyến. Demo replay dữ liệu lịch sử; không chờ dữ liệu mới hoặc gọi forecast từ dữ liệu cũ là vận hành hiện tại |
| B8. Dựng scenario, phân bổ & đối chiếu kho | Forecast + config scenario → stock item, IP, projected stock | Chủ động dựng stock đầu kỳ/config/receipts, rồi cập nhật bằng mô phỏng. Nếu phân bổ tuyến xuống SKU/type, share phải cùng parent/target/origin. Sự kiện trừ kho là giả định khai báo. Khóa đủ carrier/type, có source/scenario/version; config thiếu khác với giá trị giả định đã khai báo |
| B9. Đề xuất & cảnh báo | Kết quả B8 → REORDER_RECOMMENDATION + Dashboard | Tính lượng nhập theo một policy đã định nghĩa; tách lượng đặt với rủi ro trước ETA. q_raw=0 không nâng MOQ. velocity=0 không suy ra OK; ngày cạn chỉ trong horizon đủ dữ liệu. Lưu liên kết forecast/snapshot/config/allocation/rule/scenario; xử lý rerun để không tạo đề xuất lặp cho đơn đã chấp nhận |

## Split và chống leakage

Thiết kế split cũ D2 và điều kiện điều chỉnh cho activation nằm tại [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md). Thực hiện các điểm sau trước khi công bố metric:

- **[CỨNG]** Feature, lag, rolling chỉ dùng lịch sử từng chuỗi tới origin. Nhãn là quantity ở origin+h; không đưa nhãn tương lai vào feature của các bước sau.
- **[MỀM]** Direct multi-horizon là default đơn giản; nếu dùng recursive, thay actual chưa biết bằng forecast trong thiết kế training/evaluation tương ứng.
- **[CỨNG]** Chỉ đưa direct training row vào khi toàn bộ nhãn của row đã nằm trước cutoff. Actual test đã trôi qua được dùng tại origin mới; actual sau origin thì không.
- **[CỨNG]** Top 10, cửa sổ phân bổ, feature và ngưỡng EOL chỉ chọn từ train/validation tương ứng; thống kê toàn kỳ của review là EDA.
- Giá/khuyến mãi tương lai chỉ dùng khi đã biết tại origin. Giá bình quân đơn của ngày cần dự báo, revenue/quantity cùng ngày và activation/trạng thái tương lai đều không hợp lệ.
- Calendar lễ/mùa hè là thử nghiệm **[MỀM]** riêng sau khi chốt ý nghĩa, có ablation. Các trường bị loại khỏi phạm vi tuân theo [DATA_CONTRACT](DATA_CONTRACT.md).

## Bàn giao

M2 bàn giao pipeline tái chạy, dữ liệu xử lý, config, metadata, model/baseline được chọn và báo cáo benchmark. M3 dùng cùng giao diện forecast để phân bổ và mô phỏng. Các điều kiện hoàn thành, lịch refit đề xuất và kế hoạch đóng gói ở [ROADMAP](ROADMAP.md); hướng dẫn chạy hiện để TODO tại [REPRODUCIBILITY](REPRODUCIBILITY.md).

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [A1–A2, B1–B6, B8, D2–D3]; khung B1–B9 từ PDF VII.9; cập nhật theo [đề bài và phạm vi người dùng](PROJECT_OVERVIEW.md), 25/09/2026.
