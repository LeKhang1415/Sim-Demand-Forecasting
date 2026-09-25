# Tổng quan dự án SIGMA

## Yêu cầu gốc và phạm vi đã được bổ sung

Ngày 25/09/2026, người dùng cung cấp [ảnh đề bài T2](PROJECT_REQUIREMENTS.png) và xác nhận: **dữ liệu duy nhất được cấp là orders; dữ liệu khác nhóm phải tự dẫn xuất hoặc giả định**. Đây là cập nhật phạm vi từ người dùng, không phải xác nhận của mentor cho mọi tham số.

Đề bài: **Dự báo nhu cầu & tối ưu tồn kho kho số SIM / gói data**. Dự báo lượng kích hoạt theo ngày và theo tuyến (quốc gia, nhà mạng), từ đó đề xuất mức đặt hàng và ngưỡng cảnh báo cạn kho số.

| Mốc trong ảnh | Nội dung yêu cầu |
|---|---|
| M1 — đến 19/09 | Chuẩn hóa đơn hàng và kích hoạt; phân tích mùa vụ tuần, lễ Tết, mùa du lịch; baseline naive và moving average |
| M2 — đến 17/10 | Mô hình chuỗi thời gian theo tuyến (SARIMA / Prophet / LightGBM); MAPE ≤20% ở Top 10 tuyến chủ lực; so baseline và chọn mô hình cho từng tuyến |
| M3 — đến 07/11 | Chuyển forecast thành chính sách tồn kho (safety stock, điểm đặt hàng lại); cảnh báo cạn kho trước ≥7 ngày; dashboard dự báo và sai số thực tế |

Các mốc năm 2026 theo PDF/review. Danh sách mô hình là lựa chọn nêu trong đề bài, chưa phải yêu cầu chạy đủ mọi mô hình.

## Phạm vi triển khai

M2 cần có đầu ra và đánh giá **activation theo tuyến quốc gia–nhà mạng**. Phương án order_date × Region × SKU trong review là phương án v0.1 để tham chiếu/so sánh; không tự coi nó tương đương yêu cầu gốc. Cách đếm quantity, lọc success/refunded, khóa tuyến chi tiết, timezone và cửa sổ activation còn được mô tả dưới dạng **[MỀM] / [XÁC NHẬN]** trong [DATA_CONTRACT v0.2](DATA_CONTRACT.md).

M3 là **bài toán chính sách tồn kho trên scenario do nhóm dựng** ngay từ thiết kế, không chờ kho/lead time thật. Có thể dùng lượng kích hoạt quan sát để mô phỏng tiêu thụ, nhưng quan hệ “một kích hoạt trừ một đơn vị kho” phải ghi là giả định; orders không chứng minh thời điểm trừ kho thực tế. “Tối ưu” được đánh giá bằng so sánh policy trong cùng scenario, không khẳng định tối ưu vận hành doanh nghiệp.

## Ba nguyên tắc

1. **Tách dữ liệu quan sát, dữ liệu dẫn xuất và giả định.** Dẫn xuất cần công thức và cutoff; giả định cần lý do, source, trạng thái và sensitivity. Không suy ngược stock/lead time thật chỉ từ lịch sử orders.
2. **Đánh giá đúng cấp của đề bài.** Tuyến quốc gia–nhà mạng là cấp output cần đáp ứng. Dự báo theo SKU hoặc mô hình global/gộp chỉ là lựa chọn kỹ thuật, phải đưa được kết quả về tuyến và chấm đúng target.
3. **Tách tồn kho theo stock item trong mô phỏng.** Kho logic/region là **[MỀM]**, không chứng minh có kho vật lý. Giữ đủ carrier × SKU × product_type nếu dùng thiết kế Mục 8.5; không gộp hàng không thay thế được.

## Nguồn dữ liệu và dữ liệu nhóm dựng

| Nhóm | Nguồn/trạng thái | Cách sử dụng |
|---|---|---|
| Orders | Nguồn duy nhất được cấp; có order_datetime và activation_datetime trong cùng file | Xây target theo sự kiện tương ứng; giữ NULL và giới hạn trạng thái cuối |
| Dẫn xuất | Mapping country/carrier/region/SKU, target, lag/rolling từ orders; thứ/tháng từ ngày | Lưu công thức, phạm vi thời gian và version; chỉ dùng lịch sử tới origin khi dự báo |
| Calendar lễ/mùa | Nhóm tự dựng, không phải nguồn doanh nghiệp cấp | Ghi nguồn/quy tắc nhãn, kiểm tra ý nghĩa và ablation; không suy lịch lễ từ biến động target |
| Inventory/config/receipts và EOL | Giả định/scenario do nhóm cấu hình hoặc trạng thái sinh từ mô phỏng | Stock đầu kỳ, L/R/MOQ, ETA, service target, chi phí chưa có phải được khai báo; không xin/chờ nguồn thật như điều kiện triển khai |

Phân loại chi tiết ở [DATA_CONTRACT](DATA_CONTRACT.md); quyết định còn mở ở [DECISIONS](DECISIONS.md).

## Trạng thái và nghiệm thu

M1 đã qua hạn nhưng chưa đủ bằng chứng artifact hoàn thành; đang ở M2, hạn 17/10/2026; M3 hạn 07/11/2026. Kiểm kê và bù phần thiếu theo [ROADMAP](ROADMAP.md).

Giữ nguyên hai mục tiêu MAPE ≤20% và cảnh báo trước ≥7 ngày. Quy định cách đo, zero coverage và scenario; báo đạt/chưa đạt và các ca không quan sát đủ. Không tự thay KPI của đề bài bằng metric bổ sung, cũng không hứa đạt trước thực nghiệm. EOL không được nêu riêng trong ảnh nhưng vẫn giữ các kịch bản từ PDF/review; đầu vào EOL cũng do nhóm khai báo dưới dạng scenario, không chờ xác nhận vận hành thật.

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [A, B1–B8, D, E]; [ảnh đề bài T2](PROJECT_REQUIREMENTS.png) và xác nhận phạm vi chỉ có orders của người dùng ngày 25/09/2026, ưu tiên khi khác đề xuất cũ.
