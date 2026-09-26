# Quyết định hiện hành

## Các xác nhận đã có

Ngày dưới đây là **ngày ghi nhận qua người dùng**, không tự gán ngày mentor phê duyệt cấu hình.

| Mã | Nội dung | Nguồn/trạng thái | Ngày ghi nhận |
|---|---|---|---|
| S1 | Chỉ được cấp orders; nhóm tự dựng dữ liệu dẫn xuất và scenario, không chờ kho/config thật | Người dùng xác nhận phạm vi | 25/09/2026 |
| S2 | Target chính là **quantity sold: SUM(quantity) của success theo order_date UTC**; activation chỉ tham khảo | Xác nhận mentor do người dùng cung cấp: “Mình chỉ quan tâm số bán ra chứ không quan tâm nó có active hay không.” | 26/09/2026 |
| S3 | MAPE ≤20% ở Top 10 tuyến; cảnh báo trước ≥7 ngày; dashboard actual/forecast/sai số | KPI giữ từ đề bài, chưa có kết quả nghiệm thu | 25/09/2026 |
| S4 | Công ty ở Việt Nam, chỉ bán cho khách ở Việt Nam đi du lịch quốc tế; country là nước sử dụng, carrier là nhà mạng nước đích | Người dùng làm rõ nghiệp vụ | 26/09/2026 |
| S5 | SS/ROP/MOQ/ngưỡng cảnh báo và quy tắc nhập phải cấu hình riêng theo carrier/đối tác | Mentor xác nhận qua người dùng: “Báo hết hàng tồn kho cho từng đối tác sẽ khác nhau”; chưa cung cấp giá trị ngưỡng | 26/09/2026 |
| S6 | Dự báo tất cả 10 SKU × tuyến hợp lệ; Top 10 chỉ dùng chấm KPI, xếp theo tổng quantity success trong train | Người dùng cập nhật phạm vi; train-only giữ luật chống leakage | 26/09/2026 |

Xác nhận mới ưu tiên hơn [ảnh đề bài](PROJECT_REQUIREMENTS.png) và các đề xuất lịch sử trong [review](../Review_SIGMA_M2_M3.md). Không cần xác nhận lại target, filter success, đơn vị quantity hoặc phạm vi toàn bộ sản phẩm.

## 12 câu hỏi — trạng thái cập nhật

| Câu | Quyết định hiện hành | Còn mở / trạng thái |
|---|---|---|
| 1. Cấp dự báo? | Output ngày × (country, carrier) × SKU cho đủ 10 SKU trên mọi tuyến hợp lệ; cộng SKU/type để đánh giá tuyến | Phạm vi đã xác nhận. Cấp huấn luyện/global hay riêng là **[MỀM]** |
| **2. Order hay activation?** | **Order quantity sold**, theo order_date UTC; activation không phải target | **Đã xác nhận theo S2**. Sự kiện trừ kho trong M3 vẫn phải khai báo như giả định |
| 3. Success hay refunded? | Chỉ success trong target chính; không yêu cầu activation có giá trị | **Đã chốt filter**. Success+refunded chỉ là sensitivity tùy chọn; refunded không chứng minh hoàn kho |
| 4. SS/ROP chung hay riêng? | Cấu hình riêng theo **carrier**, tách type và cho phép override SKU; không áp một bộ tham số chung | **Đã xác nhận nguyên tắc**. L/R, MOQ, SS, ROP, mức cảnh báo, policy và xử lý đúng ngưỡng còn cần mentor xác nhận |
| 5. Nguồn tồn kho? | Stock, config và receipts/ETA là scenario do nhóm dựng | **Đã xác nhận S1**; từng giá trị có source/lý do/status/version |
| 6. Kho map theo gì? | Stock item có country/carrier/SKU/type; region để tổng hợp, không mặc nhiên là kho vật lý | Tổ chức kho logic là **[MỀM]**; giữ riêng hàng không thay thế được |
| 7. Chuỗi thưa? | Vẫn có forecast hoặc lý do thiếu cho mọi tuyến × SKU; so baseline/global/fallback trên validation | Model và cửa sổ là **[MỀM]**; xét MAE, bias, tổng horizon và stockout |
| 8. MAPE ≤20%? | Top 10 theo tổng quantity success trong train; tính trên tổng tuyến, kèm MAPE_positive/coverage/MAE/WAPE | KPI và cách xếp hạng đã chốt. Đề xuất metric ngày, báo từng tuyến và macro; quy tắc nghiệm thu macro hay từng tuyến **cần mentor xác nhận** |
| 9. Chi phí? | Giá vốn có trong orders; chi phí lưu kho/thiếu hàng/đặt mua nếu dùng là scenario | Không tối ưu chi phí thật khi thiếu thành phần; giá trị scenario cần xác nhận |
| 10. Dashboard? | Actual quantity sold, forecast, sai số của toàn bộ sản phẩm; bộ lọc Top 10; stock/cảnh báo theo carrier | Nội dung chính đã rõ; bố cục/drill-down là **[MỀM]** |
| 11. Tự động mức nào? | Đề xuất tự động tính khuyến nghị, con người quyết định mua; không tự gửi đơn | **[XÁC NHẬN]** Luồng duyệt/override chưa chốt |
| 12. EOL/SKU mới? | Sự kiện và successor scenario có scope/effective date; giữ history, kiểm tra tương thích, không suy EOL thật từ zero | Luật kỹ thuật ở [AGENTS](../AGENTS.md); hệ số chuyển đổi/cold-start còn **[MỀM] / [XÁC NHẬN]** |

## Version và những điểm cần chốt tiếp

- **Contract v0.3:** quantity success/order_date UTC/tuyến × SKU. v0.2 activation đã hạ thành tham khảo tùy chọn; v0.1 order/Region × SKU chỉ là benchmark khác grain.
- Cần chốt quy tắc nghiệm thu MAPE (macro hay từng tuyến), horizon/refit, policy và giá trị cấu hình từng carrier. Có thể triển khai đề xuất có version, không biến chúng thành luật đã duyệt.
- Mọi giả định lưu source, lý do, status, version, scenario_id và seed nếu có. Đổi target/filter/timezone/grain phải version hóa, tính lại artifact phụ thuộc.
- Bảng D1 gốc được giữ tại review để tra lịch sử; không dùng trạng thái “chưa xác nhận” cũ để mở lại S1–S6.
