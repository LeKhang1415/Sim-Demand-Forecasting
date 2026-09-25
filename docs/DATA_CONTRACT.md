# Data contract v0.2 — phạm vi orders-only

**Cập nhật phạm vi ngày 25/09/2026:** chỉ có orders được cấp, các đầu vào khác nhóm tự dựng. Đề bài yêu cầu lượng kích hoạt theo tuyến; chi tiết target v0.2 dưới đây còn là **[MỀM] / [XÁC NHẬN]**. Xem [yêu cầu gốc](PROJECT_OVERVIEW.md) và [DECISIONS](DECISIONS.md). Số liệu raw và kết quả v0.1 từ review được giữ nguyên; chưa tính lại target activation hoặc benchmark tuyến.

## Phân loại nguồn bắt buộc

| Loại | Nội dung | Cách lưu/diễn giải |
|---|---|---|
| Quan sát trong orders | Thời điểm order/activation, trạng thái cuối, quantity, thuộc tính sản phẩm, tuyến, giá | Dữ liệu được cấp; raw bất biến, không sinh activation bị thiếu |
| Dẫn xuất có căn cứ | Mapping từ cột gốc; tổng quantity theo sự kiện/ngày/tuyến; lag/rolling, độ thưa, share, activation lag | Lưu công thức, version và cutoff; thống kê tương lai không được dùng tại origin |
| Lịch tự dựng | Thứ/tháng suy từ ngày; nhãn lễ/mùa từ quy tắc/nguồn lịch nhóm chọn | Không phải dữ liệu doanh nghiệp; ghi nguồn và kiểm tra sensitivity/ablation |
| Giả định scenario | Stock đầu kỳ, L/R/MOQ, service target, receipts/ETA khởi tạo, reservation/backorder, chi phí thiếu, sự kiện EOL | Nhóm được phép cấu hình để mô phỏng; ghi lý do, source, trạng thái cần mentor xác nhận cho nghiệm thu, scenario_id/version |
| Kết quả mô phỏng | Stock biến động, lượng đặt, receipt mới theo policy/ETA, stockout, fill rate | Phụ thuộc scenario và demand replay; không gọi là dữ liệu vận hành quan sát |

Không thể xác định stock ban đầu, procurement lead time, MOQ, service target hoặc lý do EOL thật chỉ từ orders. Việc giả định đã được người dùng cho phép; **giá trị giả định cụ thể chưa được xác nhận**. Config scenario khai báo rõ khác với input bị thiếu: không âm thầm thay thiếu bằng 0. Quy tắc sinh dữ liệu, seed nếu có và sensitivity phải được lưu; tham số chọn từ dữ liệu chỉ dùng train/validation.

## Schema orders nguồn

CSV là dữ liệu thô bất biến. Kiểu dưới đây là kiểu logic đọc/chuẩn hóa theo mô tả nguồn; không khẳng định dtype vật lý của CSV hoặc áp nguyên SQL schema đề xuất thành schema đã triển khai. `order_date`, `region_code`, `carrier_id` là cột suy ra/mapping ở thiết kế bảng, không phải tên cột gốc thay thế cho `region`, `carrier`.

| Cột gốc | Kiểu logic | Ràng buộc/quan sát và cách dùng |
|---|---|---|
| order_id | Text | Không rỗng, không trùng; định danh đơn |
| order_datetime | Datetime UTC | Không rỗng; có hậu tố Z; dùng suy ra order_date UTC |
| activation_datetime | Datetime UTC, nullable | Giữ NULL; không impute thành ngày đặt; không có activation trước order |
| product_type | Categorical text | eSIM hoặc physical_SIM; giữ riêng khi quản lý kho |
| destination_country | Text | Mỗi country thuộc một region trong dataset |
| region | Text | Chiều khu vực; không tự đồng nhất với kho vật lý |
| carrier | Text | Mỗi carrier thuộc một country trong dataset; chưa chứng minh carrier là NCC ký hợp đồng |
| sku | Text | Mã mẫu gói; chưa đủ nhận diện hàng thay thế được cho nhau |
| plan_type | Categorical text | fixed hoặc unlimited; cố định theo SKU |
| data_gb | Số, thuộc tính danh mục | Cố định theo SKU; chưa được tự hiểu là hard cap với unlimited |
| validity_days | Số ngày, thuộc tính danh mục | Cố định theo SKU; không đồng nhất với hạn lưu kho/kích hoạt |
| quantity | Số nguyên | Quan sát trong khoảng 1–4; không coi khoảng này là giới hạn nghiệp vụ vĩnh viễn |
| unit_price_vnd | Số nguyên VND | Dương |
| unit_cost_vnd | Số nguyên VND | Dương |
| gross_revenue_vnd | Số nguyên VND | Bằng quantity × unit_price_vnd ở mọi dòng |
| sales_channel | Categorical text | Kênh bán |
| payment_method | Categorical text | Phương thức thanh toán |
| customer_id | Text | Mã khách; bảng CUSTOMER không cần nằm trên đường chạy forecast M2 |
| customer_type | Text; loại khỏi phạm vi sử dụng | Chỉ kê tên/kiểu để phản ánh đủ schema nguồn; không dùng trong phân tích, feature hay logic |
| order_status | Categorical text | success, failed, timeout, refunded, pending; CSV chỉ lưu trạng thái cuối |

Các cột gốc ngoài activation không có giá trị rỗng theo A1. Không đưa `is_suspected_anomaly` hoặc `anomaly_note` của calendar vào logic/feature. Không dùng bảng CUSTOMER tổng hợp toàn kỳ làm feature.

## Số liệu raw và đối soát v0.1 đã kiểm chứng

Các dòng daily grid, độ thưa và target dưới đây áp dụng cho **success theo order_date UTC × Region × SKU của v0.1**. Không dùng làm kích thước/đối soát của activation × tuyến v0.2.

| Nội dung | Giá trị từ review A1 |
|---|---|
| Orders | 100.000 dòng, 20 cột; 0 order_id trùng, 0 dòng trùng |
| Khoảng order UTC | 01/01/2024 00:21:01–31/12/2025 23:36:13 |
| Ngày / region / country / carrier / SKU | 731 / 8 / 18 / 46 / 10 |
| Kênh / thanh toán / khách phân biệt | 6 / 7 / 13.794 |
| eSIM / physical_SIM | 73.092 / 26.908 dòng |
| fixed / unlimited | 72.052 / 27.948 dòng |
| quantity 1 / 2 / 3 / 4 | 81.880 / 11.152 / 4.984 / 1.984 dòng |
| Activation thiếu | 5.691 dòng, 5,691% |
| DAILY_DEMAND đầy đủ | 731 ngày × 80 chuỗi = 58.480 dòng |
| Tổng target v0.1 | 118.296 đơn vị quantity success |
| Ô bằng 0 | 31.012/58.480 = 53,0301% |
| Chuỗi thưa nhất | South Asia/UL-30D: 95,2120% ngày bằng 0 |
| Chuỗi không có ngày zero | East Asia/D5G-7D, SEA/D5G-7D, SEA/D10G-10D |

| Trạng thái | Số dòng | Tỷ lệ | Tổng quantity | Activation rỗng |
|---|---:|---:|---:|---:|
| success | 93.104 | 93,104% | 118.296 | 0 |
| failed | 2.330 | 2,330% | 2.958 | 2.330 |
| timeout | 2.214 | 2,214% | 2.814 | 2.214 |
| refunded | 1.205 | 1,205% | 1.520 | 0 |
| pending | 1.147 | 1,147% | 1.484 | 1.147 |

Missingness đã được kiểm tra từng dòng: failed/timeout/pending thiếu activation; success/refunded có activation. **[CỨNG]** Không dùng thiếu activation trên toàn bộ orders làm lý do đủ để chọn order thay activation: success không thiếu activation. Có activation cũng không chứng minh refunded đã trả hàng vào kho.

## Target v0.2 theo yêu cầu gốc — đề xuất triển khai

Yêu cầu đã rõ: dự báo **lượng kích hoạt theo ngày, theo tuyến quốc gia–nhà mạng**. Đề xuất kỹ thuật **[MỀM] / [XÁC NHẬN]** để bắt đầu, chưa phải quyết định mentor:

```text
activation_date = phần ngày của activation_datetime sau khi parse UTC
route = (destination_country, carrier)
y_activation[activation_date, route] = SUM(quantity của các dòng được chọn)
```

- Dùng quantity để đếm SIM/gói thay vì số đơn là đề xuất kế thừa review; giả định activation_datetime của dòng áp dụng cho quantity của dòng đó cần nêu rõ.
- **Chưa chốt filter:** success-only giữ tính so sánh với v0.1; success+refunded có activation là sensitivity cần xem xét vì refunded không phủ nhận sự kiện kích hoạt đã ghi. Không tự tuyên bố một filter là toàn bộ kích hoạt thật; cần chốt định nghĩa đo với mentor.
- NULL activation không được gán bằng order_date hoặc tạo ngày kích hoạt giả. Country/carrier là khóa tuyến đề xuất theo ảnh; SKU/product_type có thể là cấp con, không tự thêm vào định nghĩa Top 10 tuyến đã nghiệm thu.
- Giữ UTC cho các ngày sự kiện để thống nhất giữa module. Không lấy ngày order thay ngày activation rồi đặt cùng tên target.
- Giữ toàn bộ activation hiện có, kể cả ngoài khoảng order; không dùng mặc định lưới 731 ngày cho activation. Nguồn được lấy theo khoảng order nên đầu/cuối chuỗi activation có lệch mẫu; activation cuối quan sát không chứng minh dữ liệu kích hoạt đầy đủ đến ngày đó. Chốt cửa sổ đủ quan sát trước split/evaluation.
- Chưa có số dòng, độ thưa, Top 10 hoặc metric activation × tuyến được tính lại. Không tái dùng các số kiểm chứng của v0.1 cho v0.2.

## Target v0.1 giữ làm tham chiếu — không thay yêu cầu activation

**[MỀM] / [XÁC NHẬN]** Target cũ: **lượng bán thành công quan sát được theo ngày đặt**. Giữ để tái lập review hoặc thử nghiệm phụ; không gọi là target chính đã đáp ứng đề bài. Nội dung default gốc còn trong câu 1–3 ở [DECISIONS](DECISIONS.md).

```text
order_date = phần ngày của order_datetime sau khi parse UTC
target[order_date, region, sku] = SUM(quantity WHERE order_status = 'success')
```

Đơn vị là số SIM/gói, không phải số đơn. Lưới ngày là 01/01/2024–31/12/2025, gồm ngày nhuận. Khóa DAILY_DEMAND: ngày × region × SKU.

**[CỨNG]** Chỉ điền ngày không có bản ghi bằng 0 dưới giả định dữ liệu đã nạp đủ và mặt hàng đang được bán. Khi có dữ liệu vận hành, phân biệt zero thật, chưa mở bán, tạm dừng, thiếu dữ liệu và stockout. Không nội suy zero thật thành nhu cầu dương. CSV thiếu availability/stockout nên không thể hiệu chỉnh nhu cầu bị che khuất hoặc kết luận zero là không có nhu cầu.

**[XÁC NHẬN]** Trong target v0.1, refunded không vào chuỗi chính; sensitivity riêng với success + refunded. Không gộp sensitivity với hàng thực trả lại, gross consumption hoặc lượng trừ kho. Filter của activation v0.2 vẫn cần quyết định riêng.

## UTC, cutoff và version

- **[CỨNG]** Khóa UTC cho order_date, activation_date và phép ghép ngày; không tự đổi giữa các module. Khi đổi timezone/filter/grain/cửa sổ quan sát thì version hóa contract/target và tái lập các bước phụ thuộc.
- Lưu `data_cutoff`, timezone, phiên bản target, event_date_basis, bộ lọc trạng thái, series/grain và cửa sổ quan sát ở metadata dataset; `run_id`, model_version và cutoff ở metadata forecast. Lưu checksum nguồn khi dựng pipeline; contract này chưa có checksum đã tính.
- **[CỨNG]** CSV chỉ có trạng thái cuối, không có lịch sử chuyển trạng thái. Backtest giả định nhãn đủ chín tại thời điểm dùng; không thể chứng minh pending/refunded đã được biết ngay lúc đặt. Công bố giới hạn point-in-time; không dùng trạng thái/activation tương lai làm feature.
- Chỉ dùng thông tin đã có tại origin. Direct training row chỉ được dùng khi toàn bộ nhãn tương lai của row đã nằm trước cutoff; quy tắc split ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md).
- Calendar cần nguồn/phiên bản được duyệt và phủ mọi ngày forecast. Kho/config demo cần source, scenario_id và phiên bản; không gắn nhãn dữ liệu thật.
- Không dùng ngày làm dự án làm ngày dữ liệu. Phạm vi hiện tại là replay dữ liệu lịch sử được cấp và mô phỏng; không chờ order mới hoặc gọi đó là dự báo vận hành hiện tại. Với activation, chỉ gọi “forecast tương lai chưa có actual” sau khi xác định cửa sổ quan sát phù hợp.

## Các điểm A2 đã sửa trong tài liệu này

“Đã sửa” là sửa cách mô tả/định nghĩa; các vấn đề chưa xác nhận vẫn giữ nguyên trạng thái, không phải đã xác nhận nghiệp vụ.

| Mục | Cách viết đã sửa |
|---|---|
| A2.1 **[CỨNG]** | 730 → **731 ngày**, thống nhất lưới và mẫu số ngày |
| A2.2 **[CỨNG]** | **Country 1–n Carrier; Region 1–n Country**. Có 10 country với 3 carrier, 8 country với 2 carrier; phụ thuộc một chiều, không phải song ánh hoặc cam kết vận hành tương lai |
| A2.3 **[CỨNG]** | Cột số liệu gốc của bảng SKU là **số dòng toàn bộ trạng thái**, không phải “số đơn thành công”; bảng phân biệt nằm bên dưới |
| A2.4 **[XÁC NHẬN]** | Calendar đủ ngày, cấu trúc khớp; đã có nhãn Tết Nguyên Đán. Chưa được xác nhận là lịch chính thức/được mentor duyệt |
| A2.5 | Không biến zero-run thành kết luận EOL. “Phần còn lại tầng A” chưa tái lập duy nhất vì thiếu định nghĩa/danh sách; số SIM chưa kích hoạt là trạng thái biến động, không phải luôn cố định |
| A2.6 **[CỨNG]** | Hệ số mùa vụ công bố chưa tái lập được do thiếu công thức/cửa sổ/mẫu số/trọng số/xử lý xu hướng; không dùng hệ số như đã chứng nhận. Các tỷ số kiểm tra độ nhạy trong review không thay hệ số chính thức |

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

Calendar có 40 ngày gắn lễ, 18 ngày trước lễ, 12 ngày sau lễ, 184 ngày mùa hè; thứ 1–7, tên thứ, tháng, cờ mùa hè tháng 6–8 và nhãn lễ khớp cấu trúc ngày. Các con số này không xác nhận tác động nghiệp vụ của lịch.

## Quan sát cần giữ khi diễn giải dữ liệu

Các thống kê toàn kỳ sau đây là EDA từ A2–A3, **không dùng làm lựa chọn trên test**:

| Quan sát | Giá trị/giới hạn từ review |
|---|---|
| Top 10 toàn kỳ | Chỉ thuộc SEA/East Asia, chiếm 54,0390% quantity success; hai region chiếm khoảng 80,41% |
| Cấp carrier × SKU × product_type | 920 tổ hợp có success; 88,0888% ô zero, zero-run tối đa 458 ngày; 336/920 không bán success trong bảy ngày cuối; không nhân thêm số region vì carrier đã xác định region |
| Cấp carrier × SKU | 460 cặp; zero-run trung bình 36,7174, tối đa 243 ngày; 78,1830% ngày zero, top 50 có khoảng trống tới 17 ngày |
| Khoảng trống chưa chứng minh EOL | South Asia/UL-30D: 46 đơn vị, 35 ngày bán, zero-run 71 ngày; Mideast/UL-30D: zero-run 80 ngày |
| SKU toàn hệ thống | Cả 10 có success trong 12/2025; zero-run tối đa 1 ngày, 6/10 không có zero. Top 10 Region × SKU theo tổng quantity success toàn kỳ có zero-run tối đa 1 ngày |
| Tăng trưởng giữa hai năm | 53.290 → 65.006 quantity success, khoảng 21,99%; tránh nhầm xu hướng với mùa vụ |
| Activation ngoài phạm vi order | Muộn nhất 14/01/2026 02:12:19 UTC; đổi target sang activation không được âm thầm cắt ở cuối lịch order, cần xét lệch mẫu đầu/cuối |
| Tác động timezone | 49.601/100.000 dòng đổi ngày nếu đổi UTC sang Asia/Ho_Chi_Minh; không tự chứng minh nên đổi timezone |
| Product type | Cả eSIM và physical_SIM xuất hiện trong mọi Region × SKU; chưa chứng minh cơ chế tồn kho giống nhau |
| Đơn chưa kích hoạt | Với quantity success có order_datetime < cutoff ≤ activation_datetime, tại cuối ngày 01/02/2024–01/12/2025: trung bình 1.007,1, nhỏ nhất 600, lớn nhất 1.632; không viết “luôn khoảng 980” |
| Activation lag | Trên 94.309 dòng có activation: TB 6,1474; P90 10,5417; tối đa 14,9583 ngày; không phải procurement lead time hoặc bảo đảm grace hợp đồng |
| Tỷ lệ phục vụ kiểm tra EOL | failed + timeout = 4,544%; tất cả non-success = 6,896%; pending chưa chắc là lỗi. Phải định nghĩa tử số, mẫu số, cửa sổ và số đơn tối thiểu trước khi áp ngưỡng |

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [A1–A3, B1–B4, B7–B8, D1–D2]; schema từ PDF mục IV.2, VII.3; phạm vi mới theo [đề bài và xác nhận của người dùng](PROJECT_OVERVIEW.md), 25/09/2026. Target v0.2 là đề xuất kỹ thuật, chưa có kết quả kiểm chứng mới.
