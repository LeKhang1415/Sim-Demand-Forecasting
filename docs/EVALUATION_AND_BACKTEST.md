# Đánh giá và backtest

**M2:** MAPE ≤20% ở Top 10 tuyến. **M3:** cảnh báo cạn kho trước ≥7 ngày. Target chính là **quantity success theo order_date UTC**; forecast cho tất cả 10 SKU × các tuyến hợp lệ.

## 1. Chọn Top 10 và đo đúng cấp

1. Trong **train**, cộng quantity success theo (country, carrier) qua mọi SKU/product_type.
2. Xếp giảm dần; tie-break đề xuất theo country rồi carrier. Lưu danh sách/cutoff, khóa trước validation/test và không đổi theo kết quả tương lai.
3. Cộng forecast và actual SKU/type lên tổng tuyến mỗi ngày trước khi tính KPI.
4. Báo Top 10 cho ngưỡng ≤20%; đồng thời chấm tất cả tuyến × SKU, region, nhóm thưa và cấp stock item nếu có phân bổ.

**[MỀM] / [XÁC NHẬN]** Đề xuất metric ngày, báo từng tuyến và macro-average Top 10. Quy tắc nghiệm thu “mọi tuyến đạt” hay “macro đạt” còn cần mentor xác nhận; không tự đổi sang metric tuần để đạt KPI. Nếu một tuyến không có actual dương, ghi N/A và số tuyến tính được, không im lặng bỏ tuyến đó.

## 2. Metric

Đặt sai số e = forecast − actual.

| Metric | Cách tính / xử lý |
|---|---|
| MAE | mean(ABS(e)), gồm actual=0 |
| MAPE_positive | mean(ABS(e)/actual) ×100% **chỉ tại actual>0** |
| Coverage MAPE | Số điểm actual>0 / tổng điểm; luôn báo cả số đếm và tỷ lệ |
| WAPE | SUM(ABS(e))/SUM(actual) ×100%; mẫu số 0 → N/A, báo MAE/forecast excess |
| Bias | SUM(e)/SUM(actual) ×100%; mẫu số 0 → N/A |
| MASE/RMSSE, tùy chọn | Mẫu số chuẩn hóa chỉ dùng train; mẫu số 0 → N/A |
| Sai số tổng horizon | Cộng actual và forecast theo từng chuỗi/origin rồi tính; báo riêng với metric ngày |

**[CỨNG]** Không chèn epsilon vào MAPE, không gọi MAPE đã bỏ zero là MAPE toàn bộ. Các zero vẫn nằm trong MAE/WAPE. Không chọn model chỉ bằng MAE của nhóm thưa; xét bias, sai số cộng dồn và hệ quả stockout.

## 3. Split và thông tin tại origin

**[MỀM] — cần mentor xác nhận thiết kế đánh giá:** train 01/01/2024–30/06/2025; validation 01/07–30/09/2025; final test 01/10–31/12/2025. Origin cuối ngày UTC, cách 7 ngày; dự báo h=1…7, chỉ chấm horizon đầy đủ trong partition. Top 10 khóa bằng train ban đầu đến 30/06/2025.

- **[CỨNG]** Lag/rolling chỉ dùng lịch sử trong chuỗi tới origin; shift trước rolling khi dự báo ngày t từ t−1.
- Direct training row chỉ dùng khi toàn bộ nhãn đã nằm trước cutoff; recursive thay actual chưa biết bằng forecast. Không kiểm thử nhiều bước bằng actual tương lai.
- Chọn model/feature/cửa sổ phân bổ/ngưỡng EOL bằng train/validation; khóa trước final test, không tuning trên test. Thống kê toàn kỳ chỉ là EDA.
- Lịch refit phải cố định trước test; đề xuất expanding window/refit cuối tháng. Actual test đã trôi qua được dùng tại origin mới.
- Lưu target/filter/grain/UTC/cutoff. CSV chỉ có trạng thái cuối: backtest giả định nhãn đủ chín, không tái hiện đầy đủ lịch sử trạng thái.
- Mở rộng và backtest horizon M3 theo policy; không lấy chất lượng 7 ngày làm bằng chứng cho horizon dài hơn.

## 4. Benchmark cũ và nghiệm thu

[Review A4](../Review_SIGMA_M2_M3.md) đã chấm **order-date × Region × SKU v0.1**: naive, seasonal naive, MA7, MA28 trên 13 origin, tổng 910 điểm; coverage MAPE 905/910 = 99,45%. Bảng metric chi tiết giữ ở nguồn để tránh lặp.

v0.3 dùng cùng quantity success/order_date nhưng **khác grain và Top 10**. Chạy lại benchmark tuyến; không gắn metric cũ cho tuyến hoặc kết luận trước khả năng đạt 20%.

**Hoàn thành kỹ thuật:** pipeline tái chạy; mọi tuyến × SKU có forecast/fallback hoặc lý do thiếu; baseline/model cùng split/horizon; tổng hợp SKU/type nhất quán; báo đầy đủ metric/coverage.

**Nghiệm thu KPI:** báo đạt/chưa đạt theo cách đo được thống nhất. Pipeline chạy được hoặc model không thắng baseline không tự đồng nghĩa đạt KPI.

## 5. Mô phỏng tồn kho và cảnh báo

Stock đầu kỳ, L/R/MOQ/SS/ROP, ETA và ngưỡng cảnh báo cấu hình **riêng từng carrier**, có source/status/version/scenario_id. Replay quantity bán theo order_date; giả định một đơn vị bán tiêu thụ một đơn vị kho phải được khai báo. Đây là mô phỏng trên bán hàng quan sát được, không phải hiệu quả với nhu cầu tiềm ẩn thật.

**[CỨNG]** Policy chỉ thấy thông tin có tại origin, nhận hàng theo ETA, bảo toàn tồn kho, tránh trừ reservation/backorder hai lần và dùng nhất quán lost-sales hoặc backorder. So các policy trên cùng scenario/demand/randomness; lưu seed nếu có.

Báo fill rate = đơn vị đáp ứng / đơn vị yêu cầu, lost units/backorder, stock trung bình/cuối kỳ và lượng nhập. Mẫu số lượng yêu cầu bằng 0 thì fill rate=N/A.

Đánh giá cảnh báo bằng hai nhánh:

1. **Đối chứng:** không đặt thêm ngoài receipts đã có tại origin, để đo rủi ro được cảnh báo.
2. **Có hành động:** policy nhập hàng, để đo kết quả thực hiện. Nhập kịp rồi không cạn không tự là false positive.

Đếm theo **sự kiện**, không đếm lặp stockout mỗi ngày. Lead time cảnh báo = ngày thiếu ở nhánh đối chứng − ngày cảnh báo đầu tiên tương ứng; báo ca ≥7 ngày, muộn, bỏ sót, không có sự kiện đối ứng và chưa đủ quan sát. Quy tắc ghép sự kiện cần khai báo trước đánh giá.

Sai số ngày cạn chỉ tính khi cả dự báo và đối chứng có sự kiện trong cửa sổ; không gán ngày cạn giả. Phân biệt hết tồn cuối ngày và thiếu nhu cầu trong ngày. Nếu chưa cạn, chỉ kết luận trong horizon đủ dữ liệu; forecast 7 ngày không bảo đảm mọi cảnh báo sớm 7 ngày.

Policy ở [ARCHITECTURE](ARCHITECTURE.md); ca kiểm thử bắt buộc ở [AGENTS](../AGENTS.md).
