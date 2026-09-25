# Decision log — phạm vi hiện tại và 12 câu hỏi gốc

## Cập nhật có hiệu lực ngày 25/09/2026

| Mã | Nội dung đã được cung cấp/xác nhận | Trạng thái | Nguồn/người cung cấp | Ngày |
|---|---|---|---|---|
| S1 | Chỉ có orders được cấp; nhóm tự dẫn xuất hoặc giả định dữ liệu khác. Không chờ nguồn inventory/config thật | Đã xác nhận phạm vi | Người dùng trong trao đổi này | 2026-09-25 |
| S2 | Dự báo lượng kích hoạt theo ngày và tuyến quốc gia–nhà mạng | Đã ghi nhận yêu cầu gốc | Ảnh đề bài T2 do người dùng cung cấp | 2026-09-25 |
| S3 | MAPE ≤20% ở Top 10 tuyến; cảnh báo trước ≥7 ngày; dashboard dự báo và sai số thực tế | Đã ghi nhận yêu cầu gốc, chưa chứng minh đạt | Ảnh đề bài T2 do người dùng cung cấp | 2026-09-25 |

[Ảnh nguồn](PROJECT_REQUIREMENTS.png) và [PROJECT_OVERVIEW](PROJECT_OVERVIEW.md) ưu tiên hơn đề xuất cũ khi mâu thuẫn phạm vi. Xác nhận S1 không đồng nghĩa mentor đã duyệt mọi stock/L/MOQ giả định; S2/S3 không tự chốt filter, đơn vị target hoặc cách chấm KPI.

## Bảng D1 — giữ nguyên ba cột gốc để đối chiếu

**[XÁC NHẬN]** Cột default và câu hỏi mentor là nội dung review v0.1, không phải toàn bộ kế hoạch hiện tại. Các đề xuất xin dữ liệu, order-date/Region × SKU và “nếu phải giữ” KPI đã có cập nhật ở cột cuối. Không thực hiện mặc định cũ trái S1–S3.

Số đầu cột Câu là question_id. Trạng thái `chưa xác nhận` nghĩa là còn chi tiết cần chốt; `đã đổi` ở câu 5 là thay phạm vi do người dùng xác nhận, không gán cho mentor. Các default chưa được xác nhận vẫn là **đề xuất — cần mentor xác nhận** cho nghiệm thu.

| Câu | Default đề xuất | Điều cần chốt với mentor | Trạng thái | Người quyết định | Ngày | Phần pipeline bị ảnh hưởng | Quyết định cập nhật |
|---|---|---|---|---|---|---|---|
| 1. Tổng vùng hay vùng × SKU? | 80 Region × SKU; tổng vùng lấy bằng cộng các SKU. | Cấp nghiệm thu và có phải phục vụ đủ 8 vùng ngay M2 không. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Target/grain, forecast, evaluation | Ảnh yêu cầu output theo tuyến quốc gia–nhà mạng. Region × SKU chỉ còn là phương án gộp/phụ; chốt grain, khóa tuyến và cách đưa output về tuyến trước nghiệm thu. |
| 2. Order hay activation? | Quantity success theo order_date UTC để khớp validation; giữ activation để phân tích nghiệp vụ. | Sự kiện phát sinh nhu cầu/trừ kho, timezone và thời điểm chốt ngày. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Target, UTC, daily grid, cutoff | Yêu cầu gốc là lượng kích hoạt. Chuyển định hướng target sang activation_date; order_date giữ tham chiếu v0.1. Còn chốt UTC, lượng quantity/số đơn, cửa sổ quan sát và sự kiện trừ kho mô phỏng. |
| 3. Success hay thêm refunded? | Success chính; sensitivity success+refunded, không nhập nhằng với hàng trả lại. | Hoàn tiền có giải phóng hàng/mã không, lý do hoàn và nhãn có độ trễ bao lâu. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Target, sensitivity, inventory flows | Với activation, đánh giá riêng success và success+refunded có activation. Chưa chốt filter; không suy refunded là hoàn kho. |
| 4. SS/ROP chung hay theo SKU? | Tham số mặc định theo carrier/type; override SKU khi có căn cứ. SS/ROP tính riêng cho stock item, không copy cùng lượng tuyệt đối cho mọi SKU. | Carrier có đúng NCC không; L, R, service target, MOQ và ưu tiên manual ROP. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Supplier config, policy SS/ROP/MOQ | Nhóm tự cấu hình L/R/MOQ/service target và policy theo scenario có nguồn/lý do/sensitivity. Không chờ cấu hình NCC thật; các giá trị cụ thể còn cần xác nhận cho nghiệm thu. |
| 5. Nguồn tồn kho? | Xin snapshot + open receipts/ETA; nếu chưa có thì scenario minh họa với nguồn/giả định rõ. | Có dữ liệu thật trước thời điểm khóa M3 không; người cung cấp và tần suất. **Cần mentor xác nhận.** | đã đổi | Người dùng — xác nhận phạm vi dữ liệu | 2026-09-25 | Snapshot, receipts, scenario | Người dùng xác nhận chỉ được cấp orders. Inventory, snapshot và receipts/ETA do nhóm giả định/sinh qua mô phỏng; bỏ phụ thuộc xin hoặc chờ nguồn kho thật. |
| 6. Kho map theo gì? | Một kho logic/region cho demo, stock item theo carrier × SKU × type. | Region destination có thực sự là vị trí kho hoặc pool có thể dùng chung không. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Stock item, inventory, allocation | Kho logic/region là giả định tổ chức mô phỏng cần ghi rõ; không cần kiểm chứng kho vật lý để chạy demo. Tách stock item theo carrier/SKU/type nếu giữ thiết kế Mục 8.5. |
| 7. Chuỗi thưa? | Có forecast cho mọi chuỗi; MA28/56, SBA/TSB/global model là ứng viên; chấm MAE, bias, total-horizon và mô phỏng thay vì ép MAPE. | Tiêu chí chấp nhận nhóm thưa, không chỉ “nới 20%”. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Baseline/model, metric nhóm thưa | Đánh giá lại độ thưa trên activation/tuyến; số liệu order/Region × SKU chỉ là tham chiếu. Giữ metric bổ sung nhưng không thay KPI đề bài. |
| 8. MAPE ≤20%? | Nếu phải giữ, đề xuất MAPE_positive macro-average Top 10 khóa từ train, công bố từng chuỗi và coverage; không hứa trước đạt 20%. | Mỗi chuỗi hay trung bình, theo ngày hay tổng tuần, xử lý zero và quyết định khi KPI không khả thi. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Top 10, metric, nghiệm thu | MAPE ≤20% ở Top 10 tuyến là mục tiêu gốc. Còn chốt cách chọn tuyến bằng train, lọc target, macro/từng tuyến, ngày/tổng horizon và xử lý zero; không tự bỏ hoặc coi KPI đã đạt. |
| 9. Chi phí? | Dùng giá vốn cho báo cáo phơi nhiễm vốn, không tối ưu lợi nhuận/EOQ khi thiếu holding/shortage/order cost. | Có cần bài toán tối ưu thật và có cung cấp đủ thành phần chi phí không. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Báo cáo vốn, phạm vi tối ưu | Không được cấp thêm chi phí vận hành. Có thể dựng chi phí scenario nếu mở rộng tối ưu tài chính, phải ghi giả định/sensitivity; không gọi là chi phí thật. |
| 10. Dashboard? | Actual/forecast 7 ngày, MAE/WAPE/MAPE có coverage, forecast age, stock/ETA, SS/ROP, cover/stockout horizon, qty và lý do cảnh báo; nhãn minh họa. | Chỉ số bắt buộc, đối tượng sử dụng, mức lọc carrier/type có drill-down phân bổ. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Output/dashboard, drill-down | Dashboard dự báo và sai số thực tế là yêu cầu gốc; actual activation lấy từ orders trong cửa sổ đủ quan sát. Stock/ETA/stockout là mô phỏng, phải có nhãn riêng. |
| 11. Tự động mức nào? | Tự động tính khuyến nghị; con người quyết định mua. Không tự gửi đơn cho NCC. | Có cần phiếu đề xuất nội bộ, người phê duyệt và lưu vết override không. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Recommendation, approval/override | — |
| 12. EOL/SKU mới? | Lifecycle do vận hành xác nhận; chặn nhập đúng offering, giữ history, successor phải tương thích; cold-start bằng offering tương đồng và hệ số scenario. | Ngày cuối bán/kích hoạt/dịch vụ, grace theo hợp đồng, khả năng xả/chuyển đổi và quyền xác nhận EOL. **Cần mentor xác nhận.** | chưa xác nhận | — | — | Lifecycle, successor, cold-start | EOL là mở rộng từ PDF. Dùng sự kiện giả định có scope/effective date trong scenario, không chờ log vận hành và không suy ngừng thật chỉ từ zero. |

## Cách cập nhật và việc còn mở

- Giữ nguyên ba cột nguồn; ghi quyết định hiện hành ở cột cuối cùng người/ngày khi có xác nhận. Không coi code/config đã chạy là mentor đã duyệt.
- Có thể bắt đầu các bước kỹ thuật đảo ngược và dựng scenario khai báo rõ trong lúc chờ; không yêu cầu cấp kho/config/receipt thật để tiếp tục.
- Ưu tiên chốt câu 1–3, 8: định nghĩa tuyến, quantity hay số đơn, success/refunded, cửa sổ activation và metric nghiệm thu. Không xin xác nhận lại việc chỉ có orders đã được người dùng làm rõ.
- Câu 4/6/9/12 là thiết kế giả định mô phỏng và mức chi tiết cần nghiệm thu; câu 10/11 là output và mức tự động hóa. Các giá trị scenario ghi source/lý do/status/version, thử sensitivity; không biến thành quy tắc doanh nghiệp.
- MAPE ≤20% và cảnh báo trước ≥7 ngày là mục tiêu giữ nguyên. Cách xử lý zero, ca không đủ quan sát, trường hợp không đạt và cách tổng hợp cần thống nhất, không tự sửa KPI.
- Tài liệu hiện dùng contract v0.2; thay filter/timezone/grain phải version hóa và chạy lại phần phụ thuộc, không tái gắn số liệu v0.1 cho target mới.

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [D1, B1–B8, D2–D3]; [ảnh đề bài T2](PROJECT_REQUIREMENTS.png) và xác nhận phạm vi của người dùng ngày 25/09/2026.
