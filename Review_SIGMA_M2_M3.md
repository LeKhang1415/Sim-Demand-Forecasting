# Review yêu cầu đề tài Team SIGMA trước M2

**Ngày đánh giá: 25/09/2026. M2: 17/10/2026. M3: 07/11/2026.**

> **Bổ sung phạm vi sau review — 25/09/2026:** Người dùng xác nhận chỉ được cấp dữ liệu orders; đầu vào khác nhóm phải tự dẫn xuất hoặc giả định. [Ảnh đề bài T2](docs/PROJECT_REQUIREMENTS.png) yêu cầu dự báo lượng kích hoạt theo tuyến quốc gia–nhà mạng, MAPE ≤20% ở Top 10 tuyến và cảnh báo trước ≥7 ngày. Vì vậy không chờ nguồn inventory/config thật; target order_date × Region × SKU dưới đây là đề xuất v0.1, không thay thế yêu cầu activation/tuyến. Các số liệu A1–A4 và benchmark được giữ nguyên phạm vi kiểm chứng cũ; không có phân tích CSV mới trong lần cập nhật này. Đọc [PROJECT_OVERVIEW](docs/PROJECT_OVERVIEW.md), [DATA_CONTRACT v0.2](docs/DATA_CONTRACT.md) và [DECISIONS](docs/DECISIONS.md) để triển khai. Phần A–E bên dưới là bản review gốc để đối chiếu, gồm các đề xuất xin dữ liệu/target/KPI đã được cập nhật phạm vi; các ràng buộc no-leakage, zero metric, khóa stock item và giới hạn suy luận vẫn áp dụng.

**Kết luận:** Có thể triển khai M2 ngay với một hợp đồng dữ liệu tạm thời, có phiên bản. Chưa nên triển khai nguyên văn toàn bộ rule tồn kho/EOL trong bản nháp. Số liệu nền phần lớn chính xác; rủi ro lớn nằm ở cách diễn giải dữ liệu, sự không thống nhất giữa các mục và khoảng cách từ dự báo bán hàng đến quyết định nhập kho.

Quy ước để nhóm sửa từng phần:

- **[CỨNG]**: sai số có thể kiểm chứng, mâu thuẫn thiết kế hoặc rủi ro logic cần xử lý trước khi dùng kết quả.
- **[MỀM]**: phương án triển khai đề xuất, có thể thay nếu thực nghiệm hoặc mentor đưa ra lựa chọn khác.
- **[XÁC NHẬN]**: giả định nghiệp vụ/dữ liệu chưa thể kết luận từ CSV. Mọi default ở phần D đều cần mentor xác nhận.

Phạm vi: đã đọc 45 trang PDF, xem sơ đồ ERD/ba khối, chạy Python/pandas trên toàn bộ hai CSV và tra nguồn bên ngoài. Không đánh giá hai cột calendar mà nhóm yêu cầu loại trừ. `customer_type` không được dùng trong phân tích hay kế hoạch mô hình. Không sửa dữ liệu nguồn. Số trang dưới đây là số trang PDF, không phải số bảng bị đánh lại trong bản nháp.

## (A) Kết quả kiểm chứng dữ liệu

### A1. Quy ước tính và các số liệu khớp

Dùng ngày **UTC** lấy từ `order_datetime` có hậu tố `Z`; lọc `order_status = success`; target là tổng `quantity`. Dựng lưới 01/01/2024–31/12/2025 gồm **731 ngày**, bao gồm 29/02/2024. Với mỗi chuỗi, độ thưa là số ngày target bằng 0 chia 731; bình quân 80 chuỗi có cùng độ dài cũng là tỷ lệ ô bằng 0 trên toàn lưới.

| Nội dung | Kết quả tính lại | Đối chiếu báo cáo |
|---|---:|---|
| Order | 100.000 dòng, 20 cột | Khớp |
| Trùng `order_id` / trùng nguyên dòng | 0 / 0 | Khớp |
| Khoảng đặt hàng | 01/01/2024 00:21:01–31/12/2025 23:36:13 UTC | Khớp phạm vi ngày |
| Số ngày có order | 731 | Đầy đủ lịch |
| Region / destination_country / carrier / SKU | 8 / 18 / 46 / 10 | Khớp |
| Kênh / thanh toán / khách hàng phân biệt | 6 / 7 / 13.794 | Khớp |
| eSIM / physical_SIM | 73.092 / 26.908 | Khớp |
| fixed / unlimited | 72.052 / 27.948 | Khớp |
| Quantity 1 / 2 / 3 / 4 | 81.880 / 11.152 / 4.984 / 1.984 dòng | Khớp |
| Activation rỗng | 5.691 dòng, 5,691% | Khớp; các cột gốc khác không rỗng |
| `gross_revenue_vnd != quantity × unit_price_vnd` | 0 dòng | Khớp |
| Giá bán/giá vốn không dương | 0 dòng | Không vi phạm ràng buộc đề xuất |
| SKU → plan_type/data_gb/validity_days | Mỗi SKU có đúng một giá trị ở từng thuộc tính | Khớp |
| Chuỗi Region × SKU có success | 80/80 | Khớp |
| DAILY_DEMAND đầy đủ | 731 × 80 = **58.480** dòng | Khớp số dòng trong schema |
| Ô ngày bằng 0 | 31.012/58.480 = **53,0301%** | Khớp “khoảng 53%” |
| Thưa nhất | South Asia/UL-30D: **95,2120%** ngày bằng 0 | Khớp “khoảng 95%” |
| Dày nhất | East Asia/D5G-7D, SEA/D5G-7D, SEA/D10G-10D: 0% ngày bằng 0 | Khớp |

| Trạng thái | Số dòng | Tỷ lệ | Tổng quantity | Activation rỗng |
|---|---:|---:|---:|---:|
| success | 93.104 | 93,104% | 118.296 | 0 |
| failed | 2.330 | 2,330% | 2.958 | 2.330 |
| timeout | 2.214 | 2,214% | 2.814 | 2.214 |
| refunded | 1.205 | 1,205% | 1.520 | 0 |
| pending | 1.147 | 1,147% | 1.484 | 1.147 |

Quan sát missingness được xác nhận **ở từng dòng**, không chỉ trùng tổng: tất cả failed/timeout/pending thiếu activation; tất cả success/refunded có activation. Tuy nhiên, không được từ đây suy ra refunded đã trả lại được hàng vào kho.

### A2. Những chỗ cần sửa hoặc chưa tái lập được

**A2.1 — [CỨNG] “730 ngày” tại Bảng 2, trang 6 là sai.** Phải là 731. Tỷ lệ xấp xỉ 53% vẫn đúng; số 58.480 ở phần schema đã dùng 731 nên chỉ cần thống nhất cách viết/mẫu số.

**A2.2 — [CỨNG] “Carrier ánh xạ 1–1 với Country” tại trang 4 sai về cardinality.** Đúng là mỗi carrier thuộc đúng một country và mỗi country thuộc đúng một region trong dataset. Nhưng 10 country có 3 carrier, 8 country có 2 carrier. Quan hệ là **Country 1–n Carrier; Region 1–n Country**, phù hợp với bảng quan hệ tại trang 10. Đây là phụ thuộc một chiều, không phải song ánh. Chưa chứng minh cấu trúc này bất biến trong vận hành tương lai.

**A2.3 — [CỨNG] Bảng đặc tính SKU trang 26 đặt nhãn “Số đơn thành công” nhưng dùng toàn bộ trạng thái.** Chú thích đã thừa nhận điều này; cần sửa tiêu đề hoặc thay số để tránh đọc nhầm.

| SKU | Số dòng toàn bộ trạng thái trong báo cáo | Số đơn success đúng |
|---|---:|---:|
| D1G-3D | 7.987 | 7.435 |
| D3G-5D | 13.850 | 12.908 |
| D5G-7D | 18.089 | 16.792 |
| D10G-10D | 16.178 | 15.094 |
| D15G-15D | 8.966 | 8.359 |
| D20G-30D | 6.982 | 6.482 |
| UL-5D | 7.964 | 7.402 |
| UL-7D | 9.926 | 9.243 |
| UL-15D | 6.031 | 5.655 |
| UL-30D | 4.027 | 3.734 |

**A2.4 — Calendar khớp về cấu trúc, chưa được xác nhận về nghiệp vụ.** Có đúng 731 ngày duy nhất, không thiếu ngày; `day_of_week` 1–7, tên thứ, tháng và cờ mùa hè tháng 6–8 đều khớp ngày thực. Có 40 ngày gắn lễ, 18 ngày trước lễ, 12 ngày sau lễ và 184 ngày mùa hè. Nhãn lễ không mâu thuẫn với cờ lễ. CSV **đã có Tết Nguyên Đán**, trái với câu “dữ liệu chưa có nhãn lịch Âm lịch Việt Nam” tại M1/trang 42. Việc có nhãn không có nghĩa lịch này chính thức hoặc đã được mentor duyệt; review chỉ xác nhận cấu trúc và nội dung đang tồn tại.

**A2.5 — Một số số liệu EOL tái lập được, một số chưa đủ định nghĩa.**

| Tuyên bố trang 33–37 | Kết quả kiểm chứng |
|---|---|
| Cả 10 SKU vẫn có bán trong tháng cuối | Đúng: cả 10 có success trong 12/2025 |
| SKU toàn hệ thống: zero-run tối đa 1 ngày; 6/10 không có zero | Đúng |
| Top 10 Region × SKU: zero-run tối đa 1 ngày | Đúng khi xếp theo tổng quantity success toàn kỳ |
| Carrier × SKU: 460 cặp; zero-run trung bình 36,7, tối đa 243 ngày | Đúng: 36,7174 và 243 |
| Carrier × SKU: 78,2% ngày bằng 0; top 50 có khoảng trống tới 17 ngày | Đúng: 78,1830% và 17 |
| “Phần còn lại tầng A”: tối đa 12, trung bình 3,2 ngày | Chưa tái lập duy nhất: thiếu định nghĩa và danh sách tầng A |
| Độ trễ kích hoạt TB 6,1; P90 10,5; tối đa 15 ngày | Xấp xỉ đúng: 6,1474; 10,5417; 14,9583 ngày, tính trên 94.309 dòng có activation |
| UL-30D + D20G-30D + UL-15D: 37% doanh thu, 17% sản lượng | Đúng xấp xỉ trên success: **36,8870% doanh thu, 16,9938% quantity** |
| D5G-7D: 9,9% doanh thu; UL-30D: 13,0% | Đúng xấp xỉ: 9,8642% và 12,9604% |
| “Luôn khoảng 980 SIM đã bán chưa kích hoạt” | Chỉ là xấp xỉ trạng thái trung bình, không phải số tồn tại mọi thời điểm |

Đối với câu cuối, tính trực tiếp quantity success có `order_datetime < cutoff ≤ activation_datetime` tại cuối mỗi ngày, từ 01/02/2024 đến 01/12/2025: **trung bình 1.007,1; nhỏ nhất 600; lớn nhất 1.632**. Chọn khoảng này để tránh đầu kỳ thiếu lịch sử và cuối kỳ bị cắt mẫu. Công thức tốc độ bán × độ trễ là ước lượng kiểu Little’s law; muốn kiểm tra nghĩa vụ phục vụ tại một ngày cụ thể phải đếm các đơn thực tế chưa kích hoạt.

**A2.6 — Các hệ số mùa vụ chưa đủ thông tin để chứng nhận.** Báo cáo không quy định đầy đủ cửa sổ trước/sau lễ, mẫu số ngày thường, trọng số giữa hai năm, có loại xu hướng hay không. Để kiểm tra độ nhạy, dùng đúng nhãn calendar hiện có, tỷ số quantity/ngày trong kỳ lễ so với các ngày `is_holiday=0` cho kết quả:

- D3G-5D dịp Quốc khánh: **1,0406**, khác 1,37 trong báo cáo.
- D5G-7D dịp Tết Nguyên Đán: **1,5087**, khác 1,30.
- D20G-30D dịp Tết Nguyên Đán: **1,2730**, khác 1,33.
- Mùa hè so với ngoài mùa hè: D1G-3D **1,3023**, UL-5D **1,3312**, khác “khoảng 1,21”.

Đây **không phải bằng chứng nhóm tính sai** vì có thể khác định nghĩa cửa sổ. Kết luận cứng là hiện chưa tái lập được các hệ số đã công bố; cần kèm công thức/cửa sổ và code trước khi dùng làm hệ số điều chỉnh EOL. Calendar vẫn là bản tạm, không dùng các tỷ số kiểm tra này để thay thế hệ số chính thức.

### A3. Pattern bổ sung ảnh hưởng trực tiếp tới triển khai

1. **Top 10 không đại diện toàn bộ 8 region.** Cả 10 thuộc SEA/East Asia, chiếm 54,0390% quantity success. Hai region này cộng lại chiếm khoảng 80,41% quantity. Chỉ chấm Top 10 sẽ không đo chất lượng phục vụ sáu vùng còn lại.
2. **Cấp Reorder thưa hơn nhiều:** có đủ 920 tổ hợp carrier × SKU × product_type có success; carrier đã xác định region nên không nhân thêm 8. Trên lưới 731 ngày, **88,0888% ô bằng 0**, zero-run dài nhất 458 ngày. Trong bảy ngày cuối dataset, **336/920 tổ hợp không bán được đơn success nào**. `velocity_7d=0` vì thế là tình huống thường gặp, không phải ngoại lệ nhỏ.
3. **Phân biệt “nhiều zero” và “ngừng cung cấp”.** South Asia/UL-30D có 46 đơn vị trong 731 ngày, chỉ 35 ngày có bán, zero-run dài nhất 71 ngày. Mideast/UL-30D có zero-run tới 80 ngày. Một khoảng trống dài hoàn toàn có thể là hành vi lịch sử bình thường.
4. **Có tăng trưởng giữa hai năm:** quantity success từ 53.290 lên 65.006, tăng khoảng 21,99% tổng năm. So sánh mùa lễ xuyên năm cần tránh nhầm xu hướng với hiệu ứng lễ.
5. **Activation vượt phạm vi order:** thời điểm kích hoạt muộn nhất là **14/01/2026 02:12:19 UTC**; không có activation trước order. Nếu đổi sang target theo activation, không được cắt lịch tại 31/12/2025 rồi âm thầm mất dữ liệu; đầu/cuối khoảng activation còn chịu ảnh hưởng cửa sổ lấy mẫu order.
6. **Timezone có tác động lớn:** đổi từ UTC sang Asia/Ho_Chi_Minh làm **49.601/100.000 dòng đổi ngày**. Đây không tự chứng minh phải dùng giờ Việt Nam, nhưng phải khóa timezone trước khi tính daily target và ghép calendar.
7. **Cả eSIM và physical_SIM xuất hiện trong cả 80 Region × SKU.** Tách chính sách tồn kho có cơ sở về phân loại dữ liệu, nhưng bản thân CSV không chứng minh hình thức mua mã, quota hay hàng vật lý có cùng cơ chế tồn kho.

### A4. Kiểm tra nhanh mức khó của KPI MAPE

Đã chạy thêm benchmark chẩn đoán, không phải huấn luyện đầy đủ M2: chọn Top 10 bằng dữ liệu **đến 30/06/2025**; 13 forecast origin cách nhau 7 ngày từ 30/06 đến 22/09/2025; mỗi origin dự báo một lần đủ 7 ngày, chỉ dùng dữ liệu đã có đến origin. Actual được chấm từ 01/07 đến 29/09/2025, tổng 910 điểm. Chưa dùng quý IV để chọn mô hình.

| Baseline | MAE, đơn vị/ngày/chuỗi | WAPE ngày | MAPE trên actual > 0 | WAPE tổng 7 ngày |
|---|---:|---:|---:|---:|
| Naive: lặp giá trị ngày cuối | 4,824 | 45,84% | 62,07% | 35,30% |
| Seasonal naive: lặp tuần cuối | 4,998 | 47,49% | 66,58% | 20,95% |
| MA7: giữ trung bình 7 ngày cho cả horizon | 3,980 | 37,82% | 57,53% | 20,95% |
| MA28 | 3,970 | 37,73% | 60,19% | 20,10% |

MAPE ở đây chỉ bao phủ **905/910 điểm, 99,45%**; năm điểm zero vẫn được tính trong MAE/WAPE. “WAPE tổng 7 ngày” tính sai số sau khi cộng bảy actual và bảy forecast của từng chuỗi, từng origin; không tương đương metric theo ngày. Các con số này không chứng minh ML không thể đạt 20%; chúng chứng minh **chưa có căn cứ cam kết KPI đó**, kể cả cho nhóm chuỗi dày.

## (B) Đánh giá phương pháp luận theo từng mục

### B1. Target và mốc thời gian — Mục IV–V

**[MỀM] Giữ target tạm thời là quantity success theo ngày đặt hàng** là lựa chọn thực dụng cho M2. Tên chính xác nên là **“lượng bán thành công quan sát được theo ngày đặt”**, chưa phải toàn bộ nhu cầu tiềm ẩn và chưa chắc là lượng trừ kho.

**[CỨNG] Lập luận chọn order vì activation thiếu 5,69% chưa đủ:** sau khi lọc success, activation không thiếu dòng nào. Lựa chọn phải dựa vào sự kiện kinh doanh cần dự báo: đặt mua, giữ chỗ, xuất kho, phát hành mã hay kích hoạt. Activation lag không phải procurement lead time; Mục 8.5 đã nêu đúng điểm này và cần giữ.

**[CỨNG] Không đồng nhất bán được với nhu cầu thực.** Khi hết hàng hoặc kênh không mở bán, quantity thấp có thể do thiếu cung; CSV không có availability/stockout nên chưa thể hiệu chỉnh phần nhu cầu bị che khuất. Với M2, công bố giới hạn này, không dựng nhãn “không có nhu cầu” như sự thật.

**[XÁC NHẬN] Refunded:** default không cộng vào target chính; thêm một báo cáo sensitivity với success + refunded. Phần tăng là 1.520 đơn vị, tương đương khoảng 1,285% target success toàn kỳ, nhưng có thể tập trung cục bộ. Có activation không chứng minh kho đã được hoàn, cũng không cho biết hoàn tiền do lý do gì. Cần tách dự báo bán hàng, gross consumption và dòng hàng trả lại nếu M3 cần quản lý kho thật.

**[CỨNG] Chốt thời điểm dữ liệu được biết:** CSV chỉ có trạng thái cuối, không có lịch sử chuyển trạng thái. Backtest hiện tại giả định nhãn đủ chín tại thời điểm dùng; không thể chứng minh pending/refunded đã được biết ngay lúc đặt. Không dùng trạng thái/kích hoạt tương lai làm feature. Lưu `data_cutoff`, timezone và phiên bản target; nêu rõ hạn chế point-in-time của dữ liệu.

### B2. Đơn vị dự báo, feature và chuỗi thưa

**[MỀM] Giữ 80 Region × SKU là cấp dự báo chính**, sau đó phân bổ cho quyết định. Với dữ liệu này, đó là thỏa hiệp hợp lý về độ thưa. **[CỨNG] Sửa Mục 8.3**, nơi “Route = Carrier + SKU” lại được gọi là đơn vị dự báo: phải phân biệt cấp forecast, cấp phân tích route và cấp quyết định tồn kho.

Không thể đưa trực tiếp một giá trị `carrier` làm categorical feature của một dòng Region × SKU có nhiều carrier. Nếu thực sự cần, dùng tỷ trọng lịch sử tính đến origin; M2 chưa cần bước này. `data_gb`, `validity_days`, `plan_type` là thuộc tính cố định, có thể hữu ích cho mô hình dùng chung nhưng không tạo thông tin thời gian mới.

**Feature đề xuất [MỀM]:**

- Bắt đầu bằng `region`, `sku`, ngày trong tuần, tháng; lag 1/7/14/28; mean 7/28/56, độ lệch chuẩn 28 ngày, tỷ lệ zero 28/56 ngày, số ngày từ lần bán gần nhất.
- Tất cả rolling/lag phải nằm trong chuỗi và chỉ dùng lịch sử đến forecast origin. Với thiết kế dự báo ngày t từ dữ liệu tới t−1, rolling phải shift trước khi tổng hợp.
- Feature lễ/mùa hè chỉ ở một thử nghiệm riêng sau khi chốt ý nghĩa calendar. Khách đi tới Đông Á không đồng nghĩa chỉ chịu lịch lễ Đông Á; CSV thiếu thị trường nguồn của khách nên chưa thể tự quyết định lịch quốc gia nào chi phối.
- Giá/khuyến mãi tương lai chỉ dùng nếu đã biết tại origin. Giá bình quân của các đơn phát sinh trong ngày cần dự báo là leakage. Revenue và quantity cùng ngày cũng vậy.

**[CỨNG] Horizon 7 ngày cần kiểm thử thật 7 bước.** Không được dự báo ngày thứ 7 bằng `lag_1` chứa actual ngày thứ 6 tương lai. Default đơn giản: mô hình direct dùng các thống kê tại origin, thêm `horizon_day` và lịch của ngày cần dự báo; nhãn là quantity ở origin+h. Hoặc dùng recursive, nhưng phải thay actual chưa biết bằng forecast trong cả training/evaluation tương ứng.

**[CỨNG] Điền zero có điều kiện.** Lưới đầy đủ là đúng cho tính toán, nhưng “không có bản ghi” chỉ được quy về 0 khi giả định dữ liệu đã nạp đủ và mặt hàng đang được bán. Khi có thông tin vận hành, phân biệt zero thật, chưa mở bán, tạm dừng, thiếu dữ liệu và hết hàng. Không nội suy để biến zero thật thành nhu cầu dương.

**[MỀM] Mô hình theo độ thưa:** baseline MA28/56 và seasonal naive cho tất cả 80 chuỗi; thêm SBA hoặc TSB cho nhóm thưa nếu kịp. TSB/SBA là ứng viên thử nghiệm, không mặc định thắng. So sánh một LightGBM global trên cả 80 chuỗi với baseline, thay vì 80 mô hình phức tạp riêng. Có thể tổng hợp tuần để kiểm tra ổn định nhưng không được trình metric tuần như metric ngày.

### B3. Metric và thiết kế đánh giá

**[CỨNG] MAPE không xác định khi actual = 0.** Không dùng epsilon tùy tiện hoặc bỏ zero rồi vẫn gọi là MAPE toàn bộ. Nếu milestone bắt buộc, ghi rõ `MAPE_positive`, tỷ lệ điểm được tính, và trình MAE/WAPE cùng lúc. Ngay Top 10 cũng có zero. Đây là vấn đề đã được giải thích trong [Forecasting: Principles and Practice — Evaluating accuracy](https://otexts.com/fpp3/accuracy.html).

**[MỀM] Bộ metric tối thiểu:** MAE; WAPE = Σ|forecast−actual|/Σactual; bias = Σ(forecast−actual)/Σactual; metric theo từng region và nhóm độ thưa; sai số tổng 7 ngày. WAPE/bias không xác định khi mẫu số bằng 0: ghi N/A và MAE/forecast excess riêng. Thêm RMSSE hoặc MASE dùng mẫu số trên train để so sánh chuỗi khác quy mô; nếu mẫu số train bằng 0 cũng phải ghi N/A.

Không chọn mô hình chỉ bằng MAE của chuỗi rất thưa: dự báo toàn 0 có thể thắng MAE nhưng không phục vụ nhu cầu cộng dồn tốt. Kiểm tra bias, sai số tổng horizon và hệ quả stockout trong mô phỏng. Nếu sau này có quantile forecast, thêm pinball loss và coverage theo horizon.

**[CỨNG] Chọn Top 10, cửa sổ phân bổ, feature và ngưỡng EOL chỉ từ train/validation tương ứng.** Thống kê toàn kỳ ở phần A là EDA; không được mang nguyên các ngưỡng đó vào backtest rồi gọi là kết quả ngoài mẫu. Dùng rolling-origin với đủ h=1…7; nguồn chuẩn là [FPP3 — Time series cross-validation](https://otexts.com/fpp3/tscv.html).

### B4. ERD/schema 12 bảng — Mục VII

Số lượng 12 bảng tự nó không phải vấn đề. Điều cần sửa là khóa, vòng đời và khả năng truy vết. Có thể giữ mô hình logic này và chỉ hiện thực phần cần cho từng milestone.

| Bảng | Nhận xét và thay đổi đề xuất |
|---|---|
| ORDERS | Giữ raw bất biến. `order_date` là cột suy ra theo timezone đã chốt. Nếu giữ đồng thời carrier/country/region, kiểm tra tính nhất quán khi nạp; FK riêng lẻ không ngăn được bộ ba mâu thuẫn. CHECK quantity 1–4 chỉ đúng với dữ liệu hiện có, không nên coi là giới hạn nghiệp vụ vĩnh viễn. |
| REGION | Đủ cho chiều phân tích. **[XÁC NHẬN]** Region điểm đến chưa chứng minh có kho vật lý tương ứng; demo có thể coi là kho logic, phải ghi rõ. |
| COUNTRY | Quan hệ 1–n với carrier hợp dữ liệu. Cho phép destination dạng nhóm nếu nghiệp vụ cần; không suy ra tương đương giữa các quốc gia cùng region. |
| CARRIER | Carrier nhà mạng chưa chắc là pháp nhân bán sỉ/NCC ký hợp đồng. Mapping carrier=NCC chỉ là giả định demo. `region_code` dư thừa so với country; có thể giữ có kiểm tra hoặc bỏ để tránh cập nhật lệch. |
| SKU_CATALOG | Tách thông số cố định là đúng. `sku` hiện giống mã mẫu gói dùng ở nhiều carrier; chưa đủ nhận diện hàng có thể thay thế cho nhau. `data_gb` của unlimited không nên tự hiểu là hard cap, cần data dictionary. |
| CUSTOMER | Không cần nằm trên đường chạy forecast M2. Có thể giữ phục vụ tra cứu; không dùng bảng tổng hợp toàn kỳ này làm feature. |
| CALENDAR | Cần phủ mọi ngày forecast, không chỉ ngày train. Lưu nguồn/phiên bản lịch được duyệt. Lịch tương lai thiếu phải tạo trước inference. |
| DAILY_DEMAND | Khóa ngày × region × SKU hợp lý; sum quantity để kiểm tra đối soát 118.296. Lưu target version/data cutoff ở metadata của dataset. |
| REGION_INVENTORY | **[CỨNG]** Khóa snapshot_date + region + SKU ở trang 20 không lưu được stock theo carrier và product_type tại Mục 8.5. Bổ sung hai chiều, hoặc một stock_item_id biểu diễn chúng. Lưu snapshot timestamp/source/scenario; định nghĩa stock khả dụng, đã giữ chỗ và hàng không thể bán. |
| SUPPLIER_CONFIG | Cần cấu hình mặc định + override có quy tắc rõ; khóa carrier+SKU hiện không giữ được nhiều phiên bản `effective_from`, chưa tách product_type. `sku='*'` không phải SKU thật: không ép nó qua FK SKU_CATALOG. Có thể dùng config_id, scope và SKU nullable với kiểm tra uniqueness/hiệu lực, hoặc tách bảng default/override nhỏ. |
| FORECAST_RESULT | **[CỨNG]** Danh sách entity bỏ model_version khỏi PK nhưng schema chi tiết đưa vào PK. Chọn một thiết kế; khuyến nghị run_id + region + SKU + forecast_date, metadata lưu model_version/data_cutoff. `run_date` một mình không phân biệt rerun trong ngày. |
| REORDER_RECOMMENDATION | **[CỨNG]** Cũng thiếu carrier/product_type trong khóa hiện tại. Cần liên kết run forecast, snapshot, config version, allocation version, rule version và scenario. Một recommendation dùng tổng nhiều forecast_date, không phải FK đơn giản tới một dòng forecast ngày. |

**[MỀM] Tối thiểu đủ để mô phỏng:** có danh sách hàng đang về kèm ETA, lượng đã đặt và trạng thái. Tổng `in_transit_qty` không đủ để biết hàng về trước hay sau ngày cạn. Có thể là bảng nhỏ `OPEN_RECEIPTS`; không cần ERP đầy đủ. Nếu không có ETA, giữ nhãn chưa đủ dữ liệu thay vì coi tất cả hàng đang về có sẵn ngay.

**[CỨNG] Trạng thái EOL phải đúng phạm vi:** SKU_CATALOG dùng chung không thể đặt một SKU thành EOL toàn hệ thống chỉ vì một carrier dừng bán. Cần lifecycle theo offering/stock item, gồm carrier + SKU + product_type, kèm vùng nếu thực tế cho phép nhiều vùng; có thể cascade khi toàn carrier hoặc toàn SKU dừng. `replace_sku` và `successor_sku` hiện trùng vai trò, nên thống nhất.

### B5. Phân bổ Region × SKU xuống cấp Reorder — Mục 8.5

**[MỀM] Tỷ trọng quantity 30 ngày, fallback 90 ngày là baseline chấp nhận được.** Ưu điểm là giảm số chuỗi phải dự báo trực tiếp, giữ tổng và dễ giải thích. Nhưng cần backtest **ở cấp nhận phân bổ**, không chỉ ở 80 chuỗi cha.

**[CỨNG] Các điều kiện phải bổ sung:**

1. Chỉ dùng lịch sử tới origin; denominator cùng region/SKU và cùng cửa sổ.
2. Lọc tập offering hợp lệ, phân biệt “chưa có lịch sử” với “không còn cung cấp”. Nếu cả 30/90 ngày bằng 0, xuất `allocation_unavailable` hoặc mapping demo đã cấu hình, không chia cho 0.
3. Tổng share bằng 1 chỉ phù hợp khi toàn bộ nhu cầu cha vẫn được phục vụ bởi các offering hợp lệ. Khi EOL mất khách, phải tách phần giữ được và phần không được phục vụ; không ép dồn 100% sang carrier còn lại.
4. Không coi hàng Nhật và hàng Thái là thay thế cho nhau chỉ vì cùng SEA/East Asia, cũng không tự chuyển eSIM sang physical_SIM. Cần compatibility theo điểm đến, thiết bị, gói/quyền sử dụng và nguồn cung.
5. Forecast được giữ số thực. Chỉ làm tròn khi tạo lượng nhập; nếu cần số nguyên phân bổ mà vẫn giữ tổng, dùng một quy tắc phân phối phần dư thống nhất.
6. Sau phân bổ, độ bất định còn gồm sai số share. Không lấy quantile của forecast cha nhân share rồi khẳng định đó là quantile đúng của từng con.

### B6. Safety Stock, Reorder Point, recommended_qty

**B6.1 — [CỨNG] Chưa có một chính sách thống nhất.** Trang 30 dùng `forecast_7d + SS − stock`; trang 40 dùng `ROP + forecast_7d − stock − in_transit`. Với nhu cầu đều 10/ngày, L=7, SS=20, stock=0, transit=0: công thức thứ nhất cho 90, thứ hai cho 160. Cả hai có thể tương ứng những kỳ bảo vệ khác nhau; bản nháp chưa định nghĩa kỳ kiểm tra/đặt hàng nên không thể chọn bằng cảm tính.

**B6.2 — [MỀM] Tách ba khái niệm:**

- `L`: thời gian từ đặt mua đến hàng sẵn sàng dùng, cùng đơn vị ngày với forecast.
- `R`: chu kỳ xem xét/đặt mua, chẳng hạn mỗi ngày hoặc mỗi tuần.
- `IP`: inventory position = on-hand khả dụng + đơn hàng đang về được công nhận − nghĩa vụ chưa đáp ứng. Nếu stock khả dụng đã trừ reservation thì không trừ reservation lần hai; backorder và reservation phải tránh trùng.

Một default dễ triển khai cho **periodic review**: mỗi R ngày, bổ sung tới mức S bảo vệ L+R ngày:

```text
mean_demand_H = sum(forecast[t+h], h=1..H)
H = L + R
S = ceil(mean_demand_H + SS_H)
q_raw = max(0, S - IP)
q = 0                         nếu q_raw = 0
q = max(MOQ, ceil(q_raw))      nếu q_raw > 0
```

Nếu có bội số đóng gói m: `q = m × ceil(max(MOQ, q_raw)/m)` khi q_raw>0. MOQ không đồng nghĩa bội số đóng gói. Sau đó kiểm tra sức chứa, hạn dùng, EOL và quy tắc xử lý thủ công nếu các ràng buộc xung đột.

Nếu mentor muốn **continuous review (s,S)**, dùng `s = forecast demand trong L + SS_L`, so IP với s để kích hoạt, rồi đặt lên S đã định nghĩa. Không trộn trigger của một chính sách với target của chính sách khác. `ROP + forecast_7d` trong báo cáo có thể là xấp xỉ L+7 ngày trong một chính sách phù hợp, **không tự động là lỗi đếm đôi**, nhưng cần nêu rõ.

**B6.3 — [MỀM] Safety Stock theo số ngày là heuristic minh họa, không phải mức phục vụ đã hiệu chỉnh.** `SS = velocity × safety_stock_days` có đơn vị đúng, nhưng không phản ánh đầy đủ độ bất định. Một lựa chọn sau baseline là:

```text
SS_H = max(0, quantile_alpha(actual cumulative H - forecast cumulative H))
S_H = mean_demand_H + SS_H
```

Residual lấy từ backtest không leakage và đúng horizon/cấp quyết định; ít mẫu thì gộp theo nhóm tương đồng và công bố hạn chế. Không cộng các quantile ngày rồi gọi đó là quantile tổng horizon.

Với giả định nhu cầu ngày độc lập, gần dừng và L cố định, công thức tham chiếu `SS = z × sigma_daily × sqrt(L)` có thể dùng làm đối chứng. Không áp đặt công thức chuẩn này cho chuỗi cực thưa hoặc lead time biến động. Lựa chọn service level là quyết định nghiệp vụ; 95% cycle service level không phải 95% fill rate. [NC State — Safety Stock Analysis](https://scm.ncsu.edu/scm-articles/article/safety-stock-analysis-inventory-management-models-a-tutorial) giải thích vai trò bất định demand/lead time và đánh đổi tồn kho–thiếu hàng.

**B6.4 — [CỨNG] Zero velocity gây lỗi quyết định:** nếu bảy ngày không bán, `velocity=0 ⇒ SS=ROP=0`; với stock=0, điều kiện `stock<ROP` sai và `stock≥ROP` lại cho OK. Điều này có thể xảy ra dù forecast tương lai >0. Dùng forecast cộng dồn và fallback cửa sổ dài hơn; nếu thiếu bằng chứng thì “chưa đủ dữ liệu”, không tự cho OK. `days_of_cover` khi velocity=0 là N/A, không phải 0 ngày hoặc một ngày cạn tự tạo.

**B6.5 — [CỨNG] Tách lượng đặt và rủi ro thiếu trước khi hàng về.** Mục 8.5 đã đúng khi không để in-transit xóa cảnh báo on-hand; đã đúng khi không nâng MOQ nếu lượng cần đặt bằng 0; đã đúng khi không coi thiếu stock là stock=0. Giữ các quy tắc đó. Bổ sung mô phỏng tồn kho theo ngày với ETA, reservation/backorder và thứ tự nhận hàng–tiêu thụ; tồn kho tương lai thiếu trước ETA vẫn cần hành động dù tổng IP cao.

**B6.6 — [CỨNG] Ngày cạn và horizon:** forecast 7 ngày chỉ cho phép nói “chưa thấy cạn trong 7 ngày” nếu stock còn dương cuối horizon. Ví dụ ngày cạn sau 16,7 ngày ở trang 9 cần ghi là ngoại suy run-rate, không phải ngày được xác định từ forecast 7 ngày. Mục 8.5/F đã thừa nhận không bảo đảm cảnh báo trước ≥7 ngày; phải đưa giới hạn này lên Output/M3, nơi vẫn đang hứa chắc.

Default M3 [MỀM]: H≥max(L+R,14), tăng theo lead time được duyệt; 14 ngày chỉ là khoảng thử nghiệm, không bảo đảm mọi ca được cảnh báo trước 7 ngày. Ghi rõ ngày dự kiến thiếu hàng đầu tiên theo forecast và dữ liệu receipt; tách “hết tồn cuối ngày” với “không đáp ứng đủ nhu cầu trong ngày”.

### B7. Review toàn bộ kịch bản EOL — Mục 8.4

| Tiểu mục | Nhận xét cần xử lý |
|---|---|
| a. Năm dạng ngừng | **[MỀM]** Danh mục phù hợp để tổ chức scenario. **[CỨNG]** Ngừng bán, ngừng nhập, hết khả năng kích hoạt và hết hỗ trợ dịch vụ là những thời điểm khác nhau. Suspended phải có đường quay lại active; hết hợp đồng có phạm vi carrier, không tự biến mọi SKU toàn hệ thống thành EOL. |
| b. Phát hiện | **[CỨNG]** Không phát sinh đơn, tỷ trọng 30 ngày bằng 0, tỷ lệ lỗi tăng hay không nạp mã không đủ chứng minh ngừng vĩnh viễn. Ba tín hiệu cùng xuất hiện vẫn có thể là gián đoạn, lỗi dữ liệu hoặc hết hàng. Xuất “nghi ngừng/gián đoạn”, cần thông báo/kiểm tra vận hành để xác nhận EOL. Rule nhìn lại 30 ngày không cung cấp cảnh báo trước 17 ngày. |
| b. Tỷ lệ lỗi nền | **[CỨNG]** 5,691% là failed+timeout+pending; pending chưa chắc là lỗi. Failed+timeout là 4,544%; tất cả non-success là 6,896%. Phải định nghĩa numerator, denominator, cửa sổ và số đơn tối thiểu trước khi áp ngưỡng 10%. |
| c. Ưu tiên giám sát | **[MỀM]** Dùng doanh thu và khả năng thay thế để xếp ưu tiên xử lý là hợp lý. **[CỨNG]** Chỉ chạy kiểm tra nhóm thấp mỗi tháng có thể bỏ lỡ toàn bộ cửa sổ EOL 17 ngày. Với 920 chuỗi, có thể chạy rule hằng ngày cho tất cả; khác nhau ở mức ưu tiên người xử lý. “Khó thay thế” phải có mapping nghiệp vụ, không suy ra chỉ từ giá. |
| d. Training sau EOL | **[CỨNG]** Chỉ loại/mask các đoạn không còn chào bán theo effective date; không xóa toàn bộ lịch sử SKU cũ. Giữ lịch sử để audit và cold-start. Với active nhưng stockout, zero cũng chưa chắc là không có nhu cầu. Sau EOL, forecast bán của offering dừng có thể bằng 0 theo constraint, trong khi nhu cầu tiềm ẩn vẫn tồn tại. “Đóng băng forecast” phải nói rõ đóng băng model hay output. |
| d. Gói thay thế | **[CỨNG]** Bảng hiện có nhóm chứa khả năng tự thay chính nó: D3G-5D xuất hiện cả nguồn/đích, tương tự D10G-10D và D20G-30D. Khi cả cặp cùng dừng, đích còn có thể nằm trong tập EOL. Kiểm tra self-loop, vòng thay thế, offering không hoạt động, sai country/thiết bị và nguồn cung thiếu. |
| d. Hệ số chuyển đổi | **[MỀM]** 0,8/0,7/0,6/0,5 chỉ là giả định scenario. Giữ được để demo sensitivity; không gọi là hệ số được học. Cần xét tổng nhu cầu giữ được, phần mất, nhiều successor và tránh cộng thêm chuyển đổi vào forecast successor đã học hiệu ứng chuyển đổi. |
| e. Xử lý tồn | **[CỨNG]** “eSIM là mã nên hủy gần như không mất chi phí” không được chứng minh: mã/quota có thể trả trước, không hoàn, hết hạn. Cả hai product_type cần chính sách hợp đồng. `validity_days` thời gian dùng gói không đồng nghĩa thời hạn lưu kho/kích hoạt; nếu có hạn lô thì ưu tiên FEFO thay vì FIFO thuần túy. |
| e. Ngày xả | **[CỨNG]** Công thức chia cho tốc độ bán phải xử lý 0; không nhân thêm hệ số mùa vụ nếu forecast đã có mùa vụ. Nên cộng dồn forecast phù hợp đến hạn cuối được phép bán/kích hoạt. Không khuyến nghị xả sản phẩm mà người mua không còn kích hoạt/sử dụng hợp lệ. |
| e. 17 ngày và grace | **[CỨNG]** 7+10,5417=17,5417; nếu thật sự áp logic cộng này thì phải làm tròn lên **18 ngày**, không 17. Nhưng quan trọng hơn, 7 ngày cam kết NCC chưa có dữ liệu xác thực, P90 không bảo vệ 10% đuôi còn lại, và activation lag không phải lead time. Chưa có căn cứ coi tổng này là deadline chuẩn. Max quan sát 14,9583 ngày cũng không bảo đảm “thêm 15 ngày” đủ nghĩa vụ hợp đồng hoặc thời gian sử dụng gói sau kích hoạt. |
| f. Mùa vụ | **[CỨNG]** Các hệ số chưa tái lập theo định nghĩa công bố; không dùng như tham số chắc chắn. **[MỀM]** Ngưỡng nâng ưu tiên 1,2 có thể giữ như giả định, kiểm tra sensitivity và tránh nhân mùa vụ hai lần. |
| g. Timeline | **[CỨNG]** Có dạng báo trước 0 ngày nên không thể luôn thực hiện T−17/T−14. Cần nhánh thông báo muộn, EOL ngay, hồi phục sau suspended và hủy thông báo. Last-buy phải xét ETA/MOQ/ngày cuối bán, không mặc định luôn dừng nhập đúng T−17. T+15 không tự chấm dứt nghĩa vụ với khách. |
| h. Metric | **[CỨNG]** Công thức cảnh báo trước bị đảo dấu: phải là `ngày dừng − ngày phát hiện`, không phải chiều ngược lại. MAE/bias vẫn tính được sau EOL; chỉ MAPE có vấn đề khi actual=0. “Giữ khách” bằng số đơn thay thế/nhu cầu quantity là lệch đơn vị nếu không thống nhất; nếu dùng đơn vị sản phẩm thì đổi tên thành tỷ lệ nhu cầu giữ được. |
| h. Mục tiêu | **[MỀM]** 95% xả tồn, <2% doanh thu, ≥70% giữ nhu cầu là mục tiêu đề xuất, chưa được dữ liệu chứng minh. Phải định nghĩa mẫu số/cửa sổ, xử lý doanh thu bằng 0 và nhu cầu đối chứng là ước lượng. Các hệ số giữ 50–60% cũng không thể đồng thời bảo đảm KPI 70% ở mọi ca. |
| i. Dữ liệu vòng đời | **[CỨNG]** Sáu cột là điểm khởi đầu, chưa đủ cho vòng đời theo carrier, nhiều successor, ngày cuối kích hoạt/dịch vụ, ETA và batch expiry. Cần lưu người cập nhật, thời điểm xác nhận, effective dates và provenance. Không tự dồn nhu cầu carrier hết hợp đồng sang carrier khác cùng region; cần kiểm tra tương thích và năng lực. |

**Đề xuất EOL tối thiểu cho M3 [MỀM]:** vận hành nhập một sự kiện có phạm vi, ngày hiệu lực và lý do; rule chặn đặt mới đúng phạm vi, đánh giá tồn/đơn chưa kích hoạt, xuất cảnh báo; successor chỉ hoạt động khi có mapping đã duyệt. Demo ba scenario: dừng có báo trước, dừng đột ngột không successor, tạm dừng rồi hồi phục. Có thể thêm cold-start successor bằng history tương đồng với một hệ số scenario được ghi rõ. Chưa cần xây bộ tự động “kết luận ngừng hẳn”.

### B8. Tính khả thi M1/M2/M3 và bốn điểm Mục XI

M1 đã qua hạn sáu ngày tại thời điểm review; PDF không đủ chứng minh các notebook/model M1 đã hoàn thành. Việc cần làm là kiểm kê artifact đang có và bù các đầu ra thiếu, không lên lại toàn bộ M1 như một giai đoạn tương lai. Còn 22 ngày tới M2 và 21 ngày từ M2 tới M3: đủ cho baseline, một global model, backtest và demo rule; khó đủ để đồng thời tối ưu chi phí thực, tự động suy luận EOL và hoàn thiện hệ thống kho sản xuất.

| Điểm chưa kết luận tại XI | Default đề xuất và giới hạn |
|---|---|
| physical_SIM/eSIM tách hay gộp | Forecast M2 vẫn gộp ở Region × SKU; tồn kho M3 giữ riêng product_type, cấu hình cho phép khác chính sách. Không suy ra eSIM tồn bằng 0 hay hủy miễn phí. **Cần mentor xác nhận.** |
| Activation rỗng | Giữ NULL và cột gốc để audit; không impute thành ngày đặt. Target success theo order không cần cột activation. **Cần mentor xác nhận sự kiện trừ kho.** |
| Đúng lượng hay đúng ngày cạn | M2 ưu tiên đánh giá forecast; M3 so chính sách bằng fill rate/lost units/stock trung bình và cảnh báo sớm. Chọn mô hình theo đánh đổi công bố, không chỉ ngày cạn. **Cần mentor xác nhận mục tiêu phục vụ.** |
| Chưa có SS/ROP thực | Dùng scenario có provenance, không tuyên bố tối ưu cho doanh nghiệp. Cấu hình thiếu cho trạng thái “chưa đủ dữ liệu”; không ngầm điền 0. **Cần mentor xác nhận phạm vi demo.** |

## (C) So sánh với project/bài toán tương tự

Đã truy cập nguồn internet. Các liên hệ dưới đây là so sánh phương pháp; không khẳng định dữ liệu retail có cùng cơ chế kinh doanh với SIM/eSIM.

| Nguồn cụ thể | Bài học từ nguồn | Áp dụng cho SIGMA |
|---|---|---|
| [M5 — repository của ban tổ chức](https://github.com/Mcompetitions/M5-methods) | Có dữ liệu, benchmark và phương pháp dự thi cho dự báo bán hàng phân cấp. | Giữ baseline và cấu trúc SKU/địa điểm là đúng hướng. Học cách tái lập evaluation, đánh giá nhiều cấp và giữ tổng; không sao chép độ phức tạp của giải thắng hoặc cho rằng M5 đã kiểm chứng rule kho của SIGMA. |
| [Long et al., 2023 — Scalable Probabilistic Forecasting in Retail with Gradient Boosted Trees](https://arxiv.org/abs/2311.00993) | Đề xuất dự báo ở cấp gộp bớt thưa rồi phân rã xuống cấp quyết định; thử trên dữ liệu doanh nghiệp, Favorita và M5. | Là tham chiếu sát với Region × SKU → carrier/type. Hướng nhóm chọn có căn cứ, nhưng hiệu quả share 30/90 ngày vẫn phải đo trên dữ liệu SIGMA. Bài học thêm là đánh giá bất định ở cấp nhận phân bổ. |
| [Amazon, 2017 — Probabilistic demand forecasting at scale](https://www.amazon.science/publications/probabilistic-demand-forecasting-at-scale) | Hệ thống retail kết hợp chuẩn bị dữ liệu, feature, forecast xác suất, evaluation và experimentation. | Nhóm đã tách forecast và decision là hợp lý. Nên bổ sung run metadata và uncertainty; với 80 chuỗi không cần sao chép Spark/hạ tầng triệu sản phẩm. |
| [NC State — Safety Stock Analysis](https://scm.ncsu.edu/scm-articles/article/safety-stock-analysis-inventory-management-models-a-tutorial) | Safety stock nhằm bù bất định demand/lead time, với đánh đổi mức phục vụ và tồn kho. | Rule theo số ngày là baseline demo dễ hiểu. Phải chốt lead time/service target, rồi đo kết quả inventory; không gọi một hệ số ngày tùy chọn là safety stock tối ưu. |
| [FPP3 — Rolling-origin evaluation](https://otexts.com/fpp3/tscv.html) | Đánh giá tại nhiều origin chỉ dùng quá khứ và đo đúng horizon cần dự báo. | Chia theo thời gian của nhóm là đúng nhưng chưa đủ. Bổ sung validation, final test và evaluation 7 bước thực; không dùng lag actual tương lai. |

Điểm đáng giữ của bản nháp: phân biệt dữ liệu thật/giả định, target theo quantity, baseline trước mô hình, forecast theo SKU thay vì chỉ tổng vùng, và Mục 8.5 đã xử lý MOQ=0/thiếu stock/cảnh báo khi chưa biết ETA tương đối rõ. Điểm cần học thêm là đánh giá đồng thời **forecast → allocation → policy**, thay vì giả định forecast tốt ở cấp cha tự động tạo quyết định kho tốt ở cấp con.

## (D) Plan đề xuất cho M2/M3

### D1. Default cho đủ 12 câu hỏi mentor

Mỗi dòng dưới đây là **đề xuất tạm thời — cần mentor xác nhận**, không ghi thành yêu cầu đã được duyệt. Lưu quyết định trong một bảng có `question_id`, default, trạng thái, người quyết định, ngày và phần pipeline bị ảnh hưởng. Có thể triển khai bằng config trong lúc chờ, tránh hard-code.

| Câu | Default đề xuất | Điều cần chốt với mentor |
|---|---|---|
| 1. Tổng vùng hay vùng × SKU? | 80 Region × SKU; tổng vùng lấy bằng cộng các SKU. | Cấp nghiệm thu và có phải phục vụ đủ 8 vùng ngay M2 không. **Cần mentor xác nhận.** |
| 2. Order hay activation? | Quantity success theo order_date UTC để khớp validation; giữ activation để phân tích nghiệp vụ. | Sự kiện phát sinh nhu cầu/trừ kho, timezone và thời điểm chốt ngày. **Cần mentor xác nhận.** |
| 3. Success hay thêm refunded? | Success chính; sensitivity success+refunded, không nhập nhằng với hàng trả lại. | Hoàn tiền có giải phóng hàng/mã không, lý do hoàn và nhãn có độ trễ bao lâu. **Cần mentor xác nhận.** |
| 4. SS/ROP chung hay theo SKU? | Tham số mặc định theo carrier/type; override SKU khi có căn cứ. SS/ROP tính riêng cho stock item, không copy cùng lượng tuyệt đối cho mọi SKU. | Carrier có đúng NCC không; L, R, service target, MOQ và ưu tiên manual ROP. **Cần mentor xác nhận.** |
| 5. Nguồn tồn kho? | Xin snapshot + open receipts/ETA; nếu chưa có thì scenario minh họa với nguồn/giả định rõ. | Có dữ liệu thật trước thời điểm khóa M3 không; người cung cấp và tần suất. **Cần mentor xác nhận.** |
| 6. Kho map theo gì? | Một kho logic/region cho demo, stock item theo carrier × SKU × type. | Region destination có thực sự là vị trí kho hoặc pool có thể dùng chung không. **Cần mentor xác nhận.** |
| 7. Chuỗi thưa? | Có forecast cho mọi chuỗi; MA28/56, SBA/TSB/global model là ứng viên; chấm MAE, bias, total-horizon và mô phỏng thay vì ép MAPE. | Tiêu chí chấp nhận nhóm thưa, không chỉ “nới 20%”. **Cần mentor xác nhận.** |
| 8. MAPE ≤20%? | Nếu phải giữ, đề xuất MAPE_positive macro-average Top 10 khóa từ train, công bố từng chuỗi và coverage; không hứa trước đạt 20%. | Mỗi chuỗi hay trung bình, theo ngày hay tổng tuần, xử lý zero và quyết định khi KPI không khả thi. **Cần mentor xác nhận.** |
| 9. Chi phí? | Dùng giá vốn cho báo cáo phơi nhiễm vốn, không tối ưu lợi nhuận/EOQ khi thiếu holding/shortage/order cost. | Có cần bài toán tối ưu thật và có cung cấp đủ thành phần chi phí không. **Cần mentor xác nhận.** |
| 10. Dashboard? | Actual/forecast 7 ngày, MAE/WAPE/MAPE có coverage, forecast age, stock/ETA, SS/ROP, cover/stockout horizon, qty và lý do cảnh báo; nhãn minh họa. | Chỉ số bắt buộc, đối tượng sử dụng, mức lọc carrier/type có drill-down phân bổ. **Cần mentor xác nhận.** |
| 11. Tự động mức nào? | Tự động tính khuyến nghị; con người quyết định mua. Không tự gửi đơn cho NCC. | Có cần phiếu đề xuất nội bộ, người phê duyệt và lưu vết override không. **Cần mentor xác nhận.** |
| 12. EOL/SKU mới? | Lifecycle do vận hành xác nhận; chặn nhập đúng offering, giữ history, successor phải tương thích; cold-start bằng offering tương đồng và hệ số scenario. | Ngày cuối bán/kích hoạt/dịch vụ, grace theo hợp đồng, khả năng xả/chuyển đổi và quyền xác nhận EOL. **Cần mentor xác nhận.** |

Ưu tiên trao đổi trước: **1–3, 6, 8** khóa thiết kế M2; **4–5, 11–12** khóa M3; 7/9/10 chốt cùng tiêu chí nghiệm thu. Nếu chưa có phản hồi, ghi rõ “default chưa xác nhận” và tiến hành các bước kỹ thuật có thể đảo ngược; không tự ghi thành quyết định của mentor.

### D2. Kế hoạch M2: 25/09–17/10/2026

| Mốc | Việc thực hiện theo thứ tự | Đầu ra/điều kiện hoàn thành |
|---|---|---|
| **25–27/09** | Kiểm kê M1; họp mentor các câu khóa M2. Chốt tạm target, timezone, grain, horizon và metric. Đồng bộ các mục đang mâu thuẫn trong báo cáo. | Data contract v0.1; decision log 12 câu; danh sách phần cần sửa có người phụ trách. |
| **28–30/09** | Pipeline raw → validation → daily grid; lưu checksum nguồn; tạo split cố định. Hoàn thành baseline toàn 80 chuỗi và hồ sơ độ thưa. | 58.480 dòng nếu giữ UTC/success; tổng 118.296; notebook/script tái lập; bảng metric theo vùng, Top 10 và nhóm thưa. |
| **01–05/10** | Feature tại origin, direct h=1…7; thử một LightGBM global cho 80 chuỗi. Poisson loss là ứng viên cho quantity không âm; so với lựa chọn regression phù hợp, không giả định Poisson mô tả đúng toàn bộ phân phối. Thử calendar riêng. | Predictions validation cùng schema baseline; không feature tương lai; ablation có/không calendar. |
| **06–09/10** | Rolling-origin validation; thử SBA/TSB trên nhóm thưa nếu baseline chưa đủ. Prophet tối đa 2–3 chuỗi nếu cần cho milestone, giới hạn thời gian một ngày. | Model comparison, bias, chất lượng từng h, sai số tổng 7 ngày. Chọn mô hình/default fallback bằng validation. |
| **10–12/10** | Khóa mô hình/feature/hyperparameter và Top 10; chạy final test quý IV/2025. Đồng thời thử phân bổ 30/90 ngày để phát hiện lỗi M3 sớm. | Báo cáo test không tuning tiếp trên chính test; metric của 80 chuỗi và cấp phân bổ; danh sách thất bại cụ thể. |
| **13–15/10** | Đóng gói batch forecast, metadata, kiểm tra rerun, xử lý input thiếu. Làm forecast demo lịch sử có actual hoặc forecast sau cuối dữ liệu nhưng ghi rõ chưa có actual. | Lệnh chạy pipeline, config, model artifact, forecast 80 × 7 = 560 dòng/run, phiên bản và cutoff. |
| **16–17/10** | Rà báo cáo, chạy lại từ đầu, chuẩn bị trình bày và khoảng đệm sửa lỗi. | Nộp M2: dữ liệu xử lý, code/config, benchmark, mô hình được chọn, giới hạn và bàn giao giao diện M3. |

**Split đề xuất [MỀM]:** train ban đầu 01/01/2024–30/06/2025; validation 01/07–30/09/2025 tại các origin cách 7 ngày; final test 01/10–31/12/2025. Mỗi origin chỉ chấm horizon đủ 7 ngày trong partition. Nếu mô hình có nhãn direct tương lai, chỉ đưa training row vào khi toàn bộ nhãn của row đã nằm trước cutoff. Có thể refit cuối tháng theo expanding window, nhưng lịch refit phải cố định trước test và giống dự kiến vận hành. Lag có thể lấy actual từ những ngày test đã trôi qua tại origin mới; không lấy actual nằm sau origin.

**Không dùng ngày làm dự án làm ngày dữ liệu.** Dataset kết thúc 31/12/2025, nên forecast tháng 09–10/2026 từ lag của năm 2025 không phải dự báo vận hành hợp lệ. Demo replay tại ngày lịch sử; hoặc dự báo 01–07/01/2026 sau khi mở rộng calendar và ghi rõ chưa có actual. Muốn chạy hiện tại cần dữ liệu order mới đến gần ngày chạy.

**Tiêu chí M2 hoàn thành:** pipeline không leakage có thể tái chạy; 80 chuỗi có đầu ra hoặc lý do thiếu rõ; baseline và model chấm cùng horizon/split; báo cáo MAPE với zero coverage; model phức tạp chỉ được chọn nếu validation cho lợi ích. Không thắng baseline vẫn là kết quả khoa học hợp lệ, nếu nguyên nhân được báo cáo thay vì sửa metric để “đạt”.

### D3. Kế hoạch M3: 18/10–07/11/2026

| Mốc | Việc thực hiện | Đầu ra/điều kiện hoàn thành |
|---|---|---|
| **18–20/10** | Chốt grain kho, định nghĩa usable stock/reservation/backorder, L/R/MOQ/ETA và chính sách periodic hoặc s,S. Chốt dữ liệu thật hay demo. | Contract inventory/config/receipt; snapshot và config có version, source, scenario_id. |
| **21–25/10** | Rule engine + phân bổ + projected stock theo ngày. Mở horizon đủ L+R và mục tiêu cảnh báo; hiệu chỉnh lại evaluation cho horizon mới. | Tách đúng qty đặt, rủi ro trước ETA và thiếu dữ liệu; không tạo đề xuất lặp cho đơn đã chấp nhận. |
| **26–29/10** | Mô phỏng closed-loop trên demand lịch sử với stock/lead time giả định. Chạy sensitivity và ba scenario EOL. | Báo cáo fill rate, lost units/backorders, stock trung bình/cuối kỳ, lượng nhập và cảnh báo sớm theo scenario. |
| **30/10–02/11** | Dashboard, drill-down vùng/carrier/SKU/type, giải thích rule, nguồn giả định và thời điểm dữ liệu. | Một đường chạy forecast → allocation → inventory → alert có thể trình diễn; không gắn nhãn “thực tế” cho mô phỏng. |
| **03–05/11** | Kiểm thử tình huống biên, rerun/idempotency, chuẩn bị 5–10 slide và diễn tập. | Checklist các ca kiểm thử quan trọng pass; có fallback nếu mô hình/bảng cấu hình lỗi. |
| **06–07/11** | Khoảng đệm sửa lỗi, đóng gói nộp. | Demo, README, config scenario, báo cáo kết quả và hạn chế. |

**Scenario tồn kho [MỀM]:** chọn ma trận minh họa nhỏ như L={1,3,7} ngày; R={1,7}; stock đầu kỳ bằng {3,7,14} ngày nhu cầu trung bình của **train**; MOQ demo cấu hình riêng. Đây là stress test, không phải ước lượng từ order. Khi chưa có lead time thật, không dùng activation lag để điền L. Có thể thêm nhận hàng trễ, nhu cầu tăng và không có hàng về; lưu seed nếu sinh ngẫu nhiên.

**Mô phỏng và metric:** policy chỉ nhìn thông tin đã có tại mỗi origin, order đặt hôm nay về theo ETA, bảo toàn tồn kho; lựa chọn lost-sales hay backorder phải nhất quán. Fill rate tính theo đơn vị đáp ứng/đơn vị yêu cầu. Có đủ hàng đầu kỳ không đồng nghĩa policy tốt, nên so các policy trong cùng scenario, cùng demand và cùng nguồn randomness. Đây là mô phỏng trên lượng bán quan sát được, không phải xác nhận hiệu quả với nhu cầu tiềm ẩn doanh nghiệp.

Precision/recall cảnh báo cần hai phép đo tách biệt: (1) nhánh đối chứng không đặt thêm đơn mới ngoài các receipt đã tồn tại tại origin, để đánh giá rủi ro đã cảnh báo; (2) nhánh có hành động để đo tồn kho thực hiện dưới policy. Cảnh báo làm người quản lý nhập kịp rồi không cạn không tự động là false positive. Đếm theo sự kiện, tránh đếm lặp một stockout mỗi ngày. Sai số ngày cạn chỉ tính khi cả hai bên có sự kiện trong cửa sổ; báo thêm số trường hợp không cạn/chưa quan sát đủ, không gán ngày cạn giả cho chúng.

**Các ca kiểm thử bắt buộc cho rule:** stock/config thiếu; velocity=0 nhưng forecast>0; q_raw=0 có MOQ; stock đúng ngưỡng; hàng về sau ngày cạn; stock đã giữ chỗ; forecast thiếu một ngày; share denominator=0; EOL một carrier nhưng carrier khác còn bán; successor tự trỏ/vòng; suspended quay lại active; receipt/khuyến nghị bị chạy lại. Các ca này kiểm tra lỗi nghiệp vụ thực, không cần một bộ test hạ tầng lớn.

### D4. Phân công gợi ý theo vai trò đã có

- **Nguyên:** khóa target/metric, quyết định mentor, baseline/global model và tích hợp. Cần một người hỗ trợ backtest để tránh tất cả M2 dồn vào leader.
- **Khang:** ETL/schema, khóa/version/run metadata, đối soát và giao diện dữ liệu.
- **Hiếu:** feature, baseline, đánh giá độ thưa và sai số cộng dồn; hỗ trợ mô hình.
- **Du:** supplier config, phân bổ 30/90 ngày, MOQ và override.
- **Cường:** snapshot/receipts, projected stock và mô phỏng policy.
- **Anh:** lifecycle, successor, các ca EOL và kiểm thử nghiệp vụ.

Dashboard có thể ghép vào nhánh tích hợp sau khi schema output đã ổn định. Không ưu tiên hoàn thiện đủ 12 bảng vật lý, tối ưu tài chính hay thêm model trước khi backtest và contract chạy đúng.

## (E) Danh sách rủi ro & khuyến nghị ưu tiên

| Ưu tiên | Rủi ro | Việc cần làm | Xong khi |
|---|---|---|---|
| **P0 — trước feature/model** | Target/day/timezone chưa chốt; success chưa chắc là stock consumption | Quyết định tạm có version, đối chiếu câu mentor 1–3 | Tái lập một target duy nhất và biết điều gì sẽ đổi khi mentor sửa |
| **P0 — trước công bố metric** | Leakage đa bước, Top 10 chọn bằng test, MAPE gặp zero | Origin-based features, validation/test riêng, coverage MAPE | Có forecast h=1…7 chỉ từ dữ liệu quá khứ và metric kiểm tra được |
| **P0 — trước rule M3** | Khóa bảng thiếu carrier/type; hai công thức lượng nhập | Đồng bộ ERD/schema/output và chốt L/R/IP/policy | Một stock item có một lượng stock và một quyết định truy vết được |
| **P0 — trước demo cảnh báo** | Zero velocity cho OK giả; transit không ETA; hứa cảnh báo ≥7 ngày | Projected stock theo ngày, thiếu input có trạng thái riêng, horizon thích hợp | Không có ca stock=0/forecast>0 lại “OK” chỉ vì MA7=0 |
| **P0 — trước EOL** | Suy luận ngừng vĩnh viễn từ zero; tự chuyển sai carrier/country | Xác nhận lifecycle, kiểm tra compatible successor và phần nhu cầu mất | Ngừng một offering không làm dừng/chuyển nhầm hàng khác |
| **P1 — trong M2** | Top 10 chỉ đại diện hai region; cấp con thưa 88,09% | Chấm đủ 80 chuỗi và phân bổ xuống 920 offering | Biết chất lượng sáu region còn lại và phần lỗi do allocation |
| **P1 — trước nghiệm thu KPI** | Cam kết MAPE 20% chưa có căn cứ | Trình benchmark A4 và chốt lại định nghĩa/đối tượng KPI | Mentor đồng ý cách chấm và cách xử lý khi không đạt |
| **P1 — M3** | Không có tồn kho/lead time thật; số liệu dừng 2025 | Demo replay/scenario có nhãn; xin nguồn order và kho mới nếu chạy hiện tại | Không diễn giải kết quả minh họa thành hiệu quả doanh nghiệp |
| **P1 — EOL** | eSIM coi là miễn phí; grace 15 ngày và báo trước 17 ngày coi như chắc chắn | Cấu hình theo hợp đồng; tách thời hạn bán/kích hoạt/dịch vụ | Không cam kết hoặc xả hàng vượt quyền phục vụ |
| **P2 — chỉnh báo cáo** | Cardinality, 730/731, nhãn success, đánh số/tham chiếu chéo | Sửa tập trung sau khi chốt nội dung | Một người khác đọc và tìm đúng công thức/mục tham chiếu |
| **P2 — sau baseline ổn định** | Feature và hệ số mùa vụ chưa được xác nhận | Lưu định nghĩa, nguồn calendar, ablation; sensitivity hệ số | Có bằng chứng thêm feature tốt hơn baseline, không chỉ trực giác |

**Phạm vi nên khóa:** M2 chứng minh năng lực dự báo ngoài mẫu có thể tái lập; M3 chứng minh logic quyết định bằng mô phỏng minh bạch. Chưa có dữ liệu vận hành thì không gọi kết quả là tối ưu tồn kho thật, không bảo đảm cảnh báo sớm trong mọi trường hợp, và không tự động coi các giả định của bản nháp là quy tắc doanh nghiệp.
