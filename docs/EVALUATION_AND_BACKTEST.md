# Evaluation và backtest

## Mục tiêu đề bài và phạm vi số liệu

**M2: MAPE ≤20% ở Top 10 tuyến chủ lực; M3: cảnh báo cạn kho trước ≥7 ngày.** Đây là yêu cầu gốc trong [ảnh đề bài](PROJECT_REQUIREMENTS.png), không phải mục tiêu tùy chọn. Cần báo đạt/chưa đạt theo cách đo thống nhất; các giới hạn kỹ thuật không tự hủy KPI.

Đánh giá chính là **activation × tuyến quốc gia–nhà mạng**. Chọn Top 10 bằng train trên target/filter đã định nghĩa, khóa trước test; không dùng danh sách Top 10 Region × SKU của review. Cách xếp hạng, macro-average hay từng tuyến và xử lý zero còn cần xác nhận ở [DECISIONS](DECISIONS.md). MAPE_positive/WAPE là cách báo minh bạch, không tự trở thành phương án thay KPI được duyệt.

## Metric tối thiểu

**[MỀM]** Bộ metric từ B3 được tính cùng target/filter/split/horizon, báo từng tuyến và nhóm độ thưa; tổng hợp region nếu cần. Báo riêng Top 10 cho KPI và các tuyến còn lại để tránh bỏ sót. Target và số liệu nền ở [DATA_CONTRACT](DATA_CONTRACT.md).

| Metric | Quy ước và giới hạn |
|---|---|
| MAE | Trung bình sai số tuyệt đối; tính cả actual=0 |
| WAPE | Σ\|forecast−actual\| / Σactual; mẫu số bằng 0 thì N/A, kèm MAE/forecast excess riêng |
| Bias | Σ(forecast−actual) / Σactual; mẫu số bằng 0 thì N/A; theo dõi dự báo dư/thiếu |
| MAPE_positive | **[CỨNG]** Chỉ tính ở actual>0, luôn báo số điểm được tính/tổng điểm và tỷ lệ coverage; không chèn epsilon hoặc gọi là MAPE toàn bộ |
| RMSSE hoặc MASE | **[MỀM]** Mẫu số chuẩn hóa chỉ tính từ train để so chuỗi khác quy mô; nếu mẫu số train bằng 0 thì N/A |
| Sai số tổng horizon | Cộng actual/forecast của từng chuỗi, từng origin trước khi tính sai số; phân biệt với metric từng ngày |

**[CỨNG]** MAPE không xác định khi actual=0; vẫn giữ các điểm đó trong MAE/WAPE. Định nghĩa KPI/macro-average Top 10 còn là đề xuất cần mentor xác nhận tại câu 8 của [DECISIONS](DECISIONS.md). Không hứa trước đạt KPI.

Không chọn model chỉ vì MAE thấp ở nhóm thưa; kiểm tra bias, tổng horizon và ảnh hưởng stockout. Nếu có quantile forecast sau này, thêm pinball loss và coverage theo horizon. Đây là phương án mở rộng, chưa phải kết quả đã có.

## Rolling-origin — split D2 tham chiếu và điều chỉnh activation

Lịch sau là đề xuất cũ trên order-date. **Với activation, chỉ tái sử dụng sau khi xác định cửa sổ đủ quan sát**: không coi phần đầu/cuối thiếu mẫu orders hoặc ngày sau cuối order là các zero đầy đủ. Lưu split/cutoff mới theo target version; không khẳng định đã kiểm chứng split này cho activation.

**Split đề xuất [MỀM]:** train ban đầu 01/01/2024–30/06/2025; validation 01/07–30/09/2025 tại các origin cách 7 ngày; final test 01/10–31/12/2025. Mỗi origin chỉ chấm horizon đủ 7 ngày trong partition. Nếu mô hình có nhãn direct tương lai, chỉ đưa training row vào khi toàn bộ nhãn của row đã nằm trước cutoff. Có thể refit cuối tháng theo expanding window, nhưng lịch refit phải cố định trước test và giống dự kiến vận hành. Lag có thể lấy actual từ những ngày test đã trôi qua tại origin mới; không lấy actual nằm sau origin.

Đây là **đề xuất — cần mentor xác nhận**, không phải split đã chạy xong. **[CỨNG]** Chọn Top 10, cửa sổ phân bổ, feature và ngưỡng EOL chỉ từ train/validation tương ứng. Khóa model/feature/hyperparameter trước final test; không tuning tiếp trên chính test. Thống kê toàn kỳ trong review là EDA.

**[CỨNG]** Kiểm thử thực đủ horizon: không dự báo bước sau bằng lag actual tương lai. Direct dùng thống kê tại origin, horizon_day và lịch ngày dự báo; recursive phải thay actual chưa biết bằng forecast trong training/evaluation tương ứng. Shift trước rolling với thiết kế dự báo ngày t từ dữ liệu tới t−1; không đưa target/giá bình quân/revenue cùng ngày vào input.

Backtest hiện giả định nhãn đã đủ chín, do orders chỉ có trạng thái cuối. Lưu cutoff/timezone/target version và nêu hạn chế point-in-time theo contract. Phân bổ và policy phải được đánh giá tiếp ở cấp stock item; không chỉ chấm cấp cha.

## Benchmark chẩn đoán A4 — không phải kết quả huấn luyện M2

**Phạm vi v0.1:** quantity success theo order_date UTC, Top 10 Region × SKU. Giữ nguyên kết quả review để truy vết; chưa có benchmark activation/tuyến. Các con số này không chứng minh KPI theo tuyến đã đạt hoặc không thể đạt.

Đã chạy thêm benchmark chẩn đoán, không phải huấn luyện đầy đủ M2: chọn Top 10 bằng dữ liệu **đến 30/06/2025**; 13 forecast origin cách nhau 7 ngày từ 30/06 đến 22/09/2025; mỗi origin dự báo một lần đủ 7 ngày, chỉ dùng dữ liệu đã có đến origin. Actual được chấm từ 01/07 đến 29/09/2025, tổng 910 điểm. Chưa dùng quý IV để chọn mô hình.

| Baseline | MAE, đơn vị/ngày/chuỗi | WAPE ngày | MAPE trên actual > 0 | WAPE tổng 7 ngày |
|---|---:|---:|---:|---:|
| Naive: lặp giá trị ngày cuối | 4,824 | 45,84% | 62,07% | 35,30% |
| Seasonal naive: lặp tuần cuối | 4,998 | 47,49% | 66,58% | 20,95% |
| MA7: giữ trung bình 7 ngày cho cả horizon | 3,980 | 37,82% | 57,53% | 20,95% |
| MA28 | 3,970 | 37,73% | 60,19% | 20,10% |

MAPE ở đây chỉ bao phủ **905/910 điểm, 99,45%**; năm điểm zero vẫn được tính trong MAE/WAPE. “WAPE tổng 7 ngày” tính sai số sau khi cộng bảy actual và bảy forecast của từng chuỗi, từng origin; không tương đương metric theo ngày. Các con số này không chứng minh ML không thể đạt 20%; chúng chứng minh **chưa có căn cứ cam kết KPI đó**, kể cả cho nhóm chuỗi dày.

## Tiêu chí hoàn thành M2

**Hoàn thành kỹ thuật M2:** pipeline activation/tuyến có thể tái chạy, có target/filter/cửa sổ quan sát/version rõ; output hoặc lý do thiếu cho mỗi tuyến trong phạm vi; baseline naive/moving average và model được chấm cùng horizon/split, có kết quả lựa chọn/fallback theo tuyến. Báo MAPE với coverage cùng metric bổ sung; khóa Top 10 và model trước test.

**Nghiệm thu KPI tách riêng:** báo kết quả so với ngưỡng đề bài theo cách tính được thống nhất. Nếu chưa đạt hoặc định nghĩa MAPE còn chưa thống nhất, ghi rõ và trao đổi mentor; không ghi “đạt M2” chỉ vì pipeline chạy được. Không thắng baseline vẫn có giá trị báo cáo nhưng không tự chứng minh đạt KPI.

Lịch đóng gói code/config, dữ liệu xử lý, metadata/model artifact và bàn giao M3 ở [ROADMAP](ROADMAP.md). Mục tiêu là kết quả kiểm tra được, không sửa metric để đạt KPI.

## Đánh giá mô phỏng M3

Scenario minh họa và trạng thái chưa xác nhận ở [ROADMAP](ROADMAP.md); công thức policy/horizon ở [ARCHITECTURE](ARCHITECTURE.md).

**Mô phỏng và metric:** stock đầu kỳ/L/R/MOQ/ETA do nhóm cấu hình; trạng thái sau đó sinh từ policy và sự kiện mô phỏng. Policy chỉ thấy thông tin có tại origin, hàng đặt về theo ETA, bảo toàn kho và nhất quán lost-sales/backorder. Khai báo quan hệ target activation với tiêu thụ kho; có thể giữ nhánh order-date riêng để sensitivity, không trộn hai target. Fill rate tính theo đơn vị đáp ứng/đơn vị yêu cầu. So policy trong cùng scenario, demand và randomness; không diễn giải thành hiệu quả nhu cầu tiềm ẩn của doanh nghiệp.

Precision/recall cảnh báo cần hai phép đo tách biệt: (1) nhánh đối chứng không đặt thêm đơn mới ngoài các receipt đã tồn tại tại origin, để đánh giá rủi ro đã cảnh báo; (2) nhánh có hành động để đo tồn kho thực hiện dưới policy. Cảnh báo làm người quản lý nhập kịp rồi không cạn không tự động là false positive. Đếm theo sự kiện, tránh đếm lặp một stockout mỗi ngày. Sai số ngày cạn chỉ tính khi cả hai bên có sự kiện trong cửa sổ; báo thêm số trường hợp không cạn/chưa quan sát đủ, không gán ngày cạn giả cho chúng.

**[MỀM] Cách đo mục tiêu cảnh báo ≥7 ngày:** với sự kiện thiếu hàng ở nhánh đối chứng, tính ngày thiếu − ngày cảnh báo đầu tiên tương ứng. Báo số sự kiện được cảnh báo đủ sớm, cảnh báo muộn và bị bỏ sót trên toàn bộ sự kiện đủ cửa sổ quan sát; báo riêng số chưa đủ quan sát và cảnh báo không có sự kiện đối ứng. Không loại ca khó để tăng tỷ lệ, không đặt ngày cạn giả, không nhầm ngày cạn dự báo với sự kiện đối chứng. Quy tắc ghép sự kiện/tổng hợp là thiết kế nghiệm thu cần thống nhất.

Mở và backtest horizon phù hợp trước khi chấm mục tiêu; forecast chỉ 7 ngày không bảo đảm luôn có cảnh báo sớm 7 ngày. Nếu không đạt, báo nguyên nhân và kết quả từng scenario. Các ca kiểm thử rule ở [AGENTS](../AGENTS.md).

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [A4, B1–B3, B5–B6, D1–D3]; yêu cầu KPI theo [đề bài](PROJECT_OVERVIEW.md), 25/09/2026. Cách đo trên activation/scenario là đề xuất cập nhật, chưa có kết quả mới.
