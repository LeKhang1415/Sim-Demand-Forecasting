# Phương pháp luận

## Cấp dự báo và phạm vi diễn giải

Yêu cầu gốc là **activation theo tuyến quốc gia–nhà mạng**, theo [PROJECT_OVERVIEW](PROJECT_OVERVIEW.md). Output và KPI phải được đánh giá ở cấp đó. Region × SKU trong review là **[MỀM]** phương án v0.1 dựa trên lượng bán theo ngày order; chưa có bằng chứng nó thay thế được target/cấp tuyến của đề bài.

**[CỨNG]** Phân biệt cấp forecast, route phân tích và stock item. Không đưa một giá trị carrier đơn lẻ làm categorical feature cho dòng Region × SKU có nhiều carrier. Phân bổ xuống cấp kho phải được backtest riêng; forecast tốt ở cấp cha chưa chứng minh quyết định tốt ở cấp con.

**[MỀM]** Bắt đầu bằng chuỗi activation theo route=(country, carrier); có thể thử route × SKU rồi cộng về route, hoặc mô hình global dùng chung. Đây là điều chỉnh thiết kế để đáp ứng đề bài, chưa phải kết quả đã kiểm chứng. Không gộp khác country/carrier chỉ để đạt KPI. Chi tiết filter, đơn vị và cửa sổ quan sát theo [DATA_CONTRACT v0.2](DATA_CONTRACT.md), còn cần chốt tại [DECISIONS](DECISIONS.md).

## Baseline và mô hình ứng viên

| Phạm vi | Ứng viên đề xuất | Cách quyết định |
|---|---|---|
| Mỗi tuyến được đánh giá | Naive và moving average theo đề bài; **[MỀM]** MA28/56, seasonal naive kế thừa review | Chạy lại trên activation/tuyến; không dùng kết quả order/Region × SKU làm benchmark tuyến |
| Nhóm thưa | **[MỀM]** Thêm SBA hoặc TSB nếu kịp | Không mặc định thắng; xét MAE, bias, sai số tổng horizon và hệ quả stockout trong mô phỏng |
| Mô hình theo tuyến hoặc dùng chung | SARIMA / Prophet / LightGBM là các lựa chọn trong đề bài; **[MỀM]** thử một LightGBM global trước | Chấm từng tuyến, chọn model/fallback bằng validation; “chọn cho từng tuyến” không bắt buộc huấn luyện mô hình phức tạp riêng cho mọi tuyến |
| Kiểm tra tính ổn định | **[MỀM]** Có thể tổng hợp tuần | Không trình metric tuần như metric ngày |

Poisson loss là ứng viên cho quantity không âm trong D2; so với regression phù hợp, không giả định Poisson mô tả đúng toàn bộ phân phối. Phạm vi thử Prophet nếu cần milestone đã ghi ở [ROADMAP](ROADMAP.md), không mở rộng trước khi baseline/backtest ổn định.

Feature và ablation ở [FEATURE_SYSTEM](FEATURE_SYSTEM.md); metric, rolling-origin và benchmark chẩn đoán ở [EVALUATION_AND_BACKTEST](EVALUATION_AND_BACKTEST.md). Không chọn mô hình chỉ bằng MAE trên chuỗi thưa vì forecast toàn 0 có thể không phục vụ nhu cầu cộng dồn.

## Tham chiếu tương tự từ mục C của review

Bảng sau giữ nguyên so sánh và đường dẫn mục C của review v0.1. Các nhắc tới Region × SKU, 80 chuỗi và share là bối cảnh phương án cũ, không phải xác nhận phù hợp cho activation/tuyến; cần thực nghiệm lại. Đây là so sánh phương pháp, không khẳng định retail và SIM/eSIM có cùng cơ chế kinh doanh.

| Nguồn cụ thể | Bài học từ nguồn | Áp dụng cho SIGMA |
|---|---|---|
| [M5 — repository của ban tổ chức](https://github.com/Mcompetitions/M5-methods) | Có dữ liệu, benchmark và phương pháp dự thi cho dự báo bán hàng phân cấp. | Giữ baseline và cấu trúc SKU/địa điểm là đúng hướng. Học cách tái lập evaluation, đánh giá nhiều cấp và giữ tổng; không sao chép độ phức tạp của giải thắng hoặc cho rằng M5 đã kiểm chứng rule kho của SIGMA. |
| [Long et al., 2023 — Scalable Probabilistic Forecasting in Retail with Gradient Boosted Trees](https://arxiv.org/abs/2311.00993) | Đề xuất dự báo ở cấp gộp bớt thưa rồi phân rã xuống cấp quyết định; thử trên dữ liệu doanh nghiệp, Favorita và M5. | Là tham chiếu sát với Region × SKU → carrier/type. Hướng nhóm chọn có căn cứ, nhưng hiệu quả share 30/90 ngày vẫn phải đo trên dữ liệu SIGMA. Bài học thêm là đánh giá bất định ở cấp nhận phân bổ. |
| [Amazon, 2017 — Probabilistic demand forecasting at scale](https://www.amazon.science/publications/probabilistic-demand-forecasting-at-scale) | Hệ thống retail kết hợp chuẩn bị dữ liệu, feature, forecast xác suất, evaluation và experimentation. | Nhóm đã tách forecast và decision là hợp lý. Nên bổ sung run metadata và uncertainty; với 80 chuỗi không cần sao chép Spark/hạ tầng triệu sản phẩm. |
| [NC State — Safety Stock Analysis](https://scm.ncsu.edu/scm-articles/article/safety-stock-analysis-inventory-management-models-a-tutorial) | Safety stock nhằm bù bất định demand/lead time, với đánh đổi mức phục vụ và tồn kho. | Rule theo số ngày là baseline demo dễ hiểu. Phải chốt lead time/service target, rồi đo kết quả inventory; không gọi một hệ số ngày tùy chọn là safety stock tối ưu. |
| [FPP3 — Rolling-origin evaluation](https://otexts.com/fpp3/tscv.html) | Đánh giá tại nhiều origin chỉ dùng quá khứ và đo đúng horizon cần dự báo. | Chia theo thời gian của nhóm là đúng nhưng chưa đủ. Bổ sung validation, final test và evaluation 7 bước thực; không dùng lag actual tương lai. |

Điểm giữ lại từ bản nháp: phân biệt dữ liệu thật/giả định, target quantity, baseline trước mô hình, forecast theo SKU và xử lý thiếu stock/MOQ/ETA. Đánh giá nối tiếp **forecast → allocation → policy**, không suy từ chất lượng forecast cha sang hiệu quả kho con.

Nguồn: [Review_SIGMA_M2_M3.md](../Review_SIGMA_M2_M3.md), mục [A3, B1–B3, B5, C, D2]; cập nhật định hướng theo [đề bài người dùng cung cấp](PROJECT_OVERVIEW.md), 25/09/2026. Cách tổ chức chuỗi/mô hình mới là đề xuất, chưa có metric mới.
