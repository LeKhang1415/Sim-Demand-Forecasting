# Phương pháp dự báo số lượng bán

## Bài toán

**Input:** quantity success theo order_date UTC, lịch và danh mục đã biết tại origin.

**Output:** forecast mỗi ngày cho **tất cả 10 SKU × tuyến (country, carrier) hợp lệ**, gồm cả hai product_type; cộng SKU/type để đánh giá tổng tuyến.

Target đã xác nhận ở [DATA_CONTRACT v0.3](DATA_CONTRACT.md). Activation chỉ tham khảo. Top 10 tuyến xếp theo tổng quantity success trong train chỉ phục vụ KPI MAPE ≤20%; các tuyến còn lại vẫn được dự báo và đánh giá.

## Cách làm

1. Chuẩn hóa orders, lọc success, cộng quantity theo ngày/tuyến/SKU; ghi rõ điều kiện điền zero.
2. Chạy naive và moving average cho toàn bộ chuỗi.
3. So mô hình ứng viên bằng rolling-origin validation, cùng split/horizon/target.
4. Chọn model hoặc fallback cho từng tuyến dựa trên validation; xuất đủ SKU và giữ tổng tuyến.
5. Phân bổ xuống product_type nếu cần, backtest cấp stock item rồi mô phỏng tồn kho theo config từng carrier.

| Lựa chọn **[MỀM]** | Mục đích / điều kiện |
|---|---|
| Naive, seasonal naive, MA7/28/56 | Baseline dễ giải thích; cửa sổ chọn bằng validation |
| LightGBM global trên tuyến × SKU | Dùng chung lịch sử nhiều chuỗi; so với baseline trước khi chọn |
| SARIMA / Prophet | Thử khi phù hợp đặc điểm chuỗi; đề bài không bắt buộc chạy đủ mọi model |
| SBA / TSB | Ứng viên cho chuỗi thưa, không mặc định tốt hơn |
| Dự báo tổng tuyến rồi phân bổ SKU/type | Phương án thay thế khi chuỗi con quá thưa; vẫn phải xuất đủ 10 SKU/tuyến và đo lỗi phân bổ |

Có thể thử Poisson loss cho quantity không âm; không coi đó là bằng chứng về phân phối dữ liệu. Region × SKU là cấp gộp của benchmark v0.1; nếu thử lại, vẫn phải đưa output về đúng tuyến × SKU và backtest cấp nhận phân bổ.

## Điều kiện chọn kết quả

- **[CỨNG]** Feature/lag/rolling chỉ dùng lịch sử tại origin; dự báo nhiều bước không được lấy actual tương lai. Xem [FEATURE_SYSTEM](FEATURE_SYSTEM.md).
- **[CỨNG]** Không chọn Top 10, feature, model hoặc cửa sổ phân bổ bằng test. Top 10 dùng tổng quantity success của train, gộp SKU/type.
- Báo MAPE_positive với coverage, MAE/WAPE/bias và sai số tổng horizon; không chọn model chỉ vì MAE thấp trên nhóm thưa.
- Forecast số thực; tổng SKU bằng tuyến, tổng type bằng SKU. Forecast tốt ở cấp cha chưa chứng minh quyết định kho tốt ở cấp con.
- Không dùng một carrier hay một thuộc tính SKU đại diện cho dòng tổng hợp nhiều carrier/SKU. Lễ Việt Nam là ứng viên theo thị trường bán; tác động vẫn cần ablation, không nhân thêm hệ số mùa vụ chưa tái lập.

Chi tiết split/metric ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md); phân bổ/policy ở [ARCHITECTURE](ARCHITECTURE.md). Tham khảo phương pháp lịch sử được giữ tại mục C của [review](../Review_SIGMA_M2_M3.md).
