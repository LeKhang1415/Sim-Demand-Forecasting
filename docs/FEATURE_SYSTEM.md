# Feature cho dự báo quantity sold

Target: quantity success theo **order_date UTC × tuyến × SKU**, theo [DATA_CONTRACT v0.3](DATA_CONTRACT.md). Feature tạo riêng trong từng chuỗi, chỉ dùng dữ liệu đã biết tại forecast origin. Các lựa chọn dưới đây là **[MỀM]**, chọn bằng train/validation.

## Feature ứng viên

| Nhóm | Feature | Điều kiện |
|---|---|---|
| Định danh | country, carrier, sku; region để tổng hợp; type nếu tách chuỗi | Chỉ dùng giá trị đúng với grain của dòng |
| Lịch cơ bản | Thứ, tháng, horizon_day, lịch origin+h | Biết trước, theo UTC; calendar phủ mọi ngày forecast |
| Lag | 1/7/14/28 | Lấy lịch sử tại origin, không lag actual tương lai |
| Rolling | Mean 7/28/56, std 28 | Với dự báo ngày t từ dữ liệu đến t−1: shift trước rolling |
| Độ thưa | Tỷ lệ zero 28/56, số ngày từ lần bán gần nhất | Tính tới origin; không suy EOL từ zero-run |
| Thuộc tính SKU | plan_type, data_gb, validity_days | Chỉ trên dòng một SKU; không chọn đại diện tùy ý cho tổng tuyến |
| Lễ/mùa du lịch | Lễ Việt Nam, mùa hè; lịch điểm đến nếu có lý do | Calendar tự dựng có nguồn/version; thử riêng có/không feature |

Khách mua ở Việt Nam nên lịch lễ Việt Nam là ứng viên phù hợp để kiểm tra. Điểm đến nước ngoài không tự chứng minh lịch nước đó chi phối lượng mua. Không coi nhãn calendar là tác động đã được xác nhận. Hệ số mùa vụ chưa tái lập phải có công thức/cửa sổ/mẫu số/trọng số/xử lý xu hướng và code; không nhân mùa vụ hai lần.

## Luật chống leakage **[CỨNG]**

- Lag/rolling nằm trong từng chuỗi; feature không chứa target hay thông tin sau origin.
- Direct multi-horizon dùng thống kê tại origin + horizon_day/lịch origin+h. Một training row chỉ hợp lệ khi **toàn bộ nhãn** đã nằm trước cutoff huấn luyện.
- Recursive phải dùng forecast thay actual chưa biết trong training/evaluation tương ứng; không dự báo bước sau bằng actual của bước tương lai.
- Không dùng quantity, revenue, giá bình quân đơn của ngày cần dự báo. Giá/khuyến mãi tương lai chỉ dùng nếu đã biết tại origin.
- Activation/trạng thái tương lai không hợp lệ; CSV chỉ có trạng thái cuối nên backtest phải công bố giả định nhãn đủ chín.
- Không dùng `customer_type` trong phân tích/feature; không dùng `is_suspected_anomaly`, `anomaly_note` trong logic/feature; không dùng CUSTOMER tổng hợp toàn kỳ.
- Không đưa một carrier đơn lẻ lên dòng Region × SKU chứa nhiều carrier; share nếu dùng chỉ từ lịch sử tại origin.
- Khóa feature và cửa sổ trước final test; không tuning bằng test. Actual test đã trôi qua có thể dùng ở origin mới, actual sau origin không được dùng.

Chọn Top 10 theo quantity success trong train, không dùng feature hoặc bảng xếp hạng toàn kỳ để thay quy tắc này. Xem [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md) và [AGENTS](../AGENTS.md).
